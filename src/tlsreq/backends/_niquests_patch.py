"""niquests HTTP/2 帧序 / HTTP/1 头与写合并，对齐 Chrome。"""
from __future__ import annotations

import inspect
from typing import Any

_H2_PATCHED = False
_H1_PATCHED = False

_HTTP1_KEEP_LOWER = frozenset({
    b"sec-ch-ua",
    b"sec-ch-ua-mobile",
    b"sec-ch-ua-platform",
    b"sec-fetch-site",
    b"sec-fetch-mode",
    b"sec-fetch-dest",
    b"sec-fetch-user",
    b"dnt",
    b"priority",
})

_H2_FRAME_HEADER = 9
_H2_HEADERS = 0x01
_H2_SETTINGS = 0x04
_H2_ACK = 0x01


def _import_module(name: str) -> Any:
    import sys

    mod = sys.modules.get(name)
    if mod is not None:
        return mod
    try:
        __import__(name)
    except ImportError:
        return None
    return sys.modules.get(name)


def _should_skip_h2_settings_wait(self: Any, event_type: Any) -> bool:
    names = (
        (getattr(event_type, "__name__", ""),)
        if not isinstance(event_type, tuple)
        else tuple(getattr(t, "__name__", "") for t in event_type)
    )
    svn = getattr(self._svn, "name", None) or getattr(self._svn, "value", self._svn)
    return "HandshakeCompleted" in names and svn in {"h2", "HTTP/2.0"}


def _wrap_exchange_until(orig: Any) -> Any:
    if inspect.iscoroutinefunction(orig):
        async def __exchange_until(self: Any, event_type: Any, *args: Any, _orig: Any = orig, **kwargs: Any) -> Any:
            if _should_skip_h2_settings_wait(self, event_type):
                return []
            return await _orig(self, event_type, *args, **kwargs)

        return __exchange_until

    def __exchange_until(self: Any, event_type: Any, *args: Any, _orig: Any = orig, **kwargs: Any) -> Any:
        if _should_skip_h2_settings_wait(self, event_type):
            return []
        return _orig(self, event_type, *args, **kwargs)

    return __exchange_until


def _iter_h2_frames(data: bytes) -> tuple[list[bytes], bytes]:
    frames: list[bytes] = []
    i = 0
    n = len(data)
    while i + _H2_FRAME_HEADER <= n:
        length = int.from_bytes(data[i:i + 3], "big")
        end = i + _H2_FRAME_HEADER + length
        if end > n:
            break
        frames.append(data[i:end])
        i = end
    return frames, data[i:]


def _park_settings_ack(protocol: Any, data: bytes) -> bytes:
    frames, rest = _iter_h2_frames(data)
    kept: list[bytes] = []
    pending = getattr(protocol, "_tlsreq_pending_ack", b"")
    for frame in frames:
        if frame[3] == _H2_SETTINGS and frame[4] & _H2_ACK:
            pending += frame
            continue
        if frame[3] == _H2_HEADERS:
            protocol._tlsreq_headers_sent = True
        kept.append(frame)
    protocol._tlsreq_pending_ack = pending
    return b"".join(kept) + rest


def _wrap_bytes_received(orig: Any) -> Any:
    def bytes_received(self: Any, data: bytes, _orig: Any = orig) -> None:
        _orig(self, data)
        buf = getattr(self._connection, "_data_to_send", None)
        if buf:
            self._connection._data_to_send = bytearray(_park_settings_ack(self, bytes(buf)))

    return bytes_received


def _swap_python_hpack(connection: Any) -> None:
    from jh2.hpack.hpack import Encoder as PyHpackEncoder

    if type(connection.encoder).__module__ == "jh2.hpack.hpack":
        return
    connection.encoder = PyHpackEncoder()


def _wrap_protocol_init(orig: Any) -> Any:
    def __init__(self: Any, *args: Any, _orig: Any = orig, **kwargs: Any) -> None:
        _orig(self, *args, **kwargs)
        _swap_python_hpack(self._connection)

    return __init__


def _wrap_bytes_to_send(orig: Any) -> Any:
    def bytes_to_send(self: Any, _orig: Any = orig) -> bytes:
        already_flushed = getattr(self, "_tlsreq_headers_flushed", False)
        data = _park_settings_ack(self, _orig(self))
        if getattr(self, "_tlsreq_headers_sent", False):
            self._tlsreq_headers_flushed = True
        if already_flushed:
            writes = getattr(self, "_tlsreq_post_headers_writes", 0) + 1
            self._tlsreq_post_headers_writes = writes
            pending = getattr(self, "_tlsreq_pending_ack", b"")
            if pending and writes >= 2:
                self._tlsreq_pending_ack = b""
                return data + pending
        return data

    return bytes_to_send


def patch_http2_chrome_frames() -> None:
    global _H2_PATCHED
    if _H2_PATCHED:
        return

    priority_ok = False
    for name in (
        "niquests.packages.urllib3.contrib.hface.protocols.http2._h2",
        "urllib3_future.contrib.hface.protocols.http2._h2",
        "urllib3.contrib.hface.protocols.http2._h2",
    ):
        mod = _import_module(name)
        cls = getattr(mod, "HTTP2ProtocolHyperImpl", None) if mod else None
        if cls is None:
            continue
        if getattr(cls, "_tlsreq_h2_patched", False) or getattr(cls, "_chrome151_ack_held", False):
            priority_ok = True
            continue

        def submit_headers(self: Any, stream_id: int, headers: Any, end_stream: bool = False) -> None:
            self._connection.send_headers(
                stream_id,
                headers,
                end_stream,
                priority_weight=256,
                priority_depends_on=0,
                priority_exclusive=True,
            )
            self._open_stream_count += 1

        cls.submit_headers = submit_headers
        cls.bytes_received = _wrap_bytes_received(cls.bytes_received)
        cls.bytes_to_send = _wrap_bytes_to_send(cls.bytes_to_send)
        cls.__init__ = _wrap_protocol_init(cls.__init__)
        cls._tlsreq_h2_patched = True
        priority_ok = True

    preface_ok = False
    for name, cls_name, mangled in (
        ("niquests.packages.urllib3.backend.hface", "HfaceBackend", "_HfaceBackend__exchange_until"),
        ("urllib3_future.backend.hface", "HfaceBackend", "_HfaceBackend__exchange_until"),
        ("urllib3.backend.hface", "HfaceBackend", "_HfaceBackend__exchange_until"),
        ("niquests.packages.urllib3.backend._async.hface", "AsyncHfaceBackend", "_AsyncHfaceBackend__exchange_until"),
        ("urllib3_future.backend._async.hface", "AsyncHfaceBackend", "_AsyncHfaceBackend__exchange_until"),
        ("urllib3.backend._async.hface", "AsyncHfaceBackend", "_AsyncHfaceBackend__exchange_until"),
    ):
        mod = _import_module(name)
        cls = getattr(mod, cls_name, None) if mod else None
        if cls is None:
            continue
        if getattr(cls, "_tlsreq_skip_h2_settings_wait", False) or getattr(cls, "_chrome151_skip_h2_settings_wait", False):
            preface_ok = True
            continue
        orig = getattr(cls, mangled, None)
        if orig is None:
            continue
        setattr(cls, mangled, _wrap_exchange_until(orig))
        cls._tlsreq_skip_h2_settings_wait = True
        preface_ok = True

    if not priority_ok or not preface_ok:
        raise RuntimeError("could not patch niquests HTTP/2 to match Chrome frame order")
    _H2_PATCHED = True


def _chrome_http1_header_name(name: bytes) -> bytes:
    lower = name.lower().replace(b"_", b"-")
    if lower in _HTTP1_KEEP_LOWER or lower.startswith(b"sec-"):
        return lower
    return b"-".join(part.capitalize() for part in lower.split(b"-"))


def _wrap_http1_bytes_to_send(orig: Any) -> Any:
    def bytes_to_send(self: Any, _orig: Any = orig) -> bytes:
        if getattr(self, "_tlsreq_hold", False):
            return b""
        return _orig(self)

    return bytes_to_send


def _wrap_http1_submit_data(orig: Any) -> Any:
    def submit_data(self: Any, stream_id: int, data: bytes, end_stream: bool = False, _orig: Any = orig) -> None:
        _orig(self, stream_id, data, end_stream)
        if end_stream:
            self._tlsreq_hold = False

    return submit_data


def _wrap_async_endheaders(orig: Any) -> Any:
    async def endheaders(
        self: Any,
        message_body: Any = None,
        *,
        encode_chunked: bool = False,
        expect_body_afterward: bool = False,
        _orig: Any = orig,
    ) -> Any:
        from urllib3 import HttpVersion

        proto = getattr(self, "_protocol", None)
        if expect_body_afterward and getattr(self, "_svn", None) == HttpVersion.h11 and proto is not None:
            proto._tlsreq_hold = True
        return await _orig(
            self,
            message_body,
            encode_chunked=encode_chunked,
            expect_body_afterward=expect_body_afterward,
        )

    return endheaders


def patch_http1_chrome_headers() -> None:
    global _H1_PATCHED
    if _H1_PATCHED:
        return

    import h11

    header_ok = False
    for name in (
        "niquests.packages.urllib3.contrib.hface.protocols.http1._h11",
        "urllib3_future.contrib.hface.protocols.http1._h11",
        "urllib3.contrib.hface.protocols.http1._h11",
    ):
        mod = _import_module(name)
        if mod is None:
            continue
        cls = getattr(mod, "HTTP1ProtocolHyperImpl", None)
        if cls is not None and not getattr(cls, "_tlsreq_h11_hold", False) and not getattr(cls, "_chrome151_h11_hold", False):
            cls.bytes_to_send = _wrap_http1_bytes_to_send(cls.bytes_to_send)
            cls.submit_data = _wrap_http1_submit_data(cls.submit_data)
            cls._tlsreq_h11_hold = True
        if getattr(mod, "_tlsreq_http1_headers", False) or getattr(mod, "_chrome151_http1_headers", False):
            header_ok = True
            continue

        orig_headers_to_request = mod.headers_to_request

        def headers_to_request(headers: Any, _orig: Any = orig_headers_to_request) -> Any:
            request = _orig(headers)
            present = {key.lower() for key, _value in request.headers}
            if b"connection" in present:
                return request
            rewritten = list(request.headers)
            insert_at = 0
            for index, (key, _value) in enumerate(rewritten):
                if key.lower() == b"host":
                    insert_at = index + 1
                    break
            rewritten.insert(insert_at, (b"Connection", b"keep-alive"))
            return h11.Request(
                method=request.method,
                headers=rewritten,
                target=request.target,
            )

        def capitalize_header_name(header: bytes) -> bytes:
            return _chrome_http1_header_name(header)

        mod.capitalize_header_name = capitalize_header_name
        mod.headers_to_request = headers_to_request
        mod._tlsreq_http1_headers = True
        header_ok = True

    coalesce_ok = False
    for name, cls_name in (
        ("niquests.packages.urllib3.backend._async.hface", "AsyncHfaceBackend"),
        ("urllib3_future.backend._async.hface", "AsyncHfaceBackend"),
        ("urllib3.backend._async.hface", "AsyncHfaceBackend"),
    ):
        mod = _import_module(name)
        cls = getattr(mod, cls_name, None) if mod else None
        if cls is None:
            continue
        if getattr(cls, "_tlsreq_h11_coalesce", False) or getattr(cls, "_chrome151_h11_coalesce", False):
            coalesce_ok = True
            continue
        cls.endheaders = _wrap_async_endheaders(cls.endheaders)
        cls._tlsreq_h11_coalesce = True
        coalesce_ok = True

    if not header_ok or not coalesce_ok:
        raise RuntimeError("could not patch niquests HTTP/1 to match Chrome request write")
    _H1_PATCHED = True
