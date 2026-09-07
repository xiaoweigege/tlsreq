from __future__ import annotations

import ssl
from typing import Any, Optional

from ..chrome_h2 import chrome_http1_header_name
from ..errors import BackendNotInstalled
from ..fingerprints import resolve
from ..response import Response, cookies_to_dict, headers_to_dict, http_version_of, status_code_of
from ..utls_release import fingerprint_from_preset
from .base import AsyncBackend, SyncBackend, merge_extra, split_data


def _import_httpx():
    try:
        import httpx
        import utls
    except ImportError as exc:
        raise BackendNotInstalled(
            "httpx backend 需要: pip install 'tlsreq[httpx]' "
            "（会装 xutls，import 名仍是 utls）"
        ) from exc
    return httpx, utls


def _fill_sslerror_strerror(exc: BaseException) -> None:
    """utls 的 SSLError 常只有 message、strerror=None。

    anyio 会执行 ``"UNEXPECTED_EOF_WHILE_READING" in exc.strerror``，
    strerror 为 None 时变成 ``argument of type 'NoneType' is not iterable``。
    close_notify 再补上这个标记，漏网的 SSLZeroReturnError 也会被当成 EOF。
    """
    if not isinstance(exc, ssl.SSLError):
        return
    message = exc.strerror
    if message is None:
        message = exc.args[-1] if exc.args else str(exc)
    if not isinstance(message, str):
        message = str(exc)
    if (
        isinstance(exc, ssl.SSLZeroReturnError)
        and "UNEXPECTED_EOF_WHILE_READING" not in message
    ):
        message = f"UNEXPECTED_EOF_WHILE_READING: {message}"
    if exc.strerror == message:
        return
    try:
        exc.strerror = message
    except Exception:
        return


class _SSLObjectAdapter:
    def __init__(self, inner: Any) -> None:
        self._inner = inner

    def __getattr__(self, name: str) -> Any:
        attr = getattr(self._inner, name)
        if not callable(attr):
            return attr

        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return attr(*args, **kwargs)
            except ssl.SSLError as exc:
                _fill_sslerror_strerror(exc)
                raise

        return wrapper

    def read(self, n: int = 1024, buffer: Any = None) -> Any:
        # utls wrap_socket 把 close_notify 收成空读；wrap_bio 会抛 SSLZeroReturnError。
        # anyio 只把 SSLEOFError / UNEXPECTED_EOF_WHILE_READING 当 EOF，
        # 这里对齐 stdlib：干净关闭返回 b''，h11 才能解析已经解密的响应。
        try:
            if buffer is None:
                return self._inner.read(n)
            return self._inner.read(n, buffer)
        except ssl.SSLZeroReturnError:
            return b"" if buffer is None else 0
        except ssl.SSLError as exc:
            _fill_sslerror_strerror(exc)
            raise

    def get_channel_binding(self, cb_type: str = "tls-unique") -> None:
        return None

    @property
    def server_side(self) -> bool:
        return self._inner.context.server_side

    def shared_ciphers(self) -> None:
        return None


def _make_context(profile: str, verify: bool):
    httpx, utls = _import_httpx()

    class HTTPXUTLSContext(utls.SSLContext):
        def set_alpn_protocols(self, protocols):
            if self.fingerprint is None:
                super().set_alpn_protocols(protocols)

        def wrap_bio(self, *args, **kwargs):
            args = list(args)
            if len(args) >= 4 and isinstance(args[3], (bytes, bytearray)):
                args[3] = args[3].decode("ascii")
            host = kwargs.get("server_hostname")
            if isinstance(host, (bytes, bytearray)):
                kwargs["server_hostname"] = host.decode("ascii")
            return _SSLObjectAdapter(super().wrap_bio(*args, **kwargs))

    fp = fingerprint_from_preset(utls, profile)
    ctx = HTTPXUTLSContext(utls.PROTOCOL_TLS_CLIENT)
    ctx.load_default_certs()
    ctx.set_fingerprint(fp)
    if not verify:
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    return ctx


def _apply_header_order(headers: Any, order: Optional[list[str]]) -> Any:
    httpx, _utls = _import_httpx()
    items = [
        (key.decode("latin-1"), value.decode("latin-1"))
        for key, value in headers.raw
    ]
    by_lower: dict[str, list[str]] = {}
    for key, value in items:
        by_lower.setdefault(key.lower(), []).append(value)
    if "connection" not in by_lower:
        by_lower["connection"] = ["keep-alive"]

    seen: list[str] = []
    full_order: list[str] = []
    for key in ("host", "connection"):
        if key not in seen:
            full_order.append(key)
            seen.append(key)
    for key in order or ():
        key = key.lower()
        if key not in seen:
            full_order.append(key)
            seen.append(key)
    for key, _value in items:
        lower = key.lower()
        if lower not in seen:
            full_order.append(lower)
            seen.append(lower)

    result = []
    for key in full_order:
        values = by_lower.get(key)
        if not values:
            continue
        name = chrome_http1_header_name(key)
        for value in values:
            result.append((name, value))
    return httpx.Headers(result)


def _on_request(request: Any) -> None:
    order = (request.extensions or {}).get("header_order")
    request.headers = _apply_header_order(request.headers, order)


async def _on_request_async(request: Any) -> None:
    _on_request(request)


def _wrap(resp: Any) -> Response:
    return Response(
        status_code=status_code_of(resp),
        content=resp.content or b"",
        headers=headers_to_dict(resp.headers),
        url=str(resp.url),
        cookies=cookies_to_dict(resp.cookies),
        http_version=http_version_of(resp),
        raw=resp,
    )


def _request_kwargs(kwargs: dict[str, Any]) -> dict[str, Any]:
    extra = dict(kwargs.pop("extra", None) or {})
    header_order = kwargs.pop("header_order", None)
    mapped: dict[str, Any] = {
        "headers": kwargs.get("headers"),
        "params": kwargs.get("params"),
        "json": kwargs.get("json"),
        "cookies": kwargs.get("cookies"),
        "timeout": kwargs.get("timeout"),
    }
    if kwargs.get("allow_redirects") is not None:
        mapped["follow_redirects"] = kwargs["allow_redirects"]
    mapped.update(split_data(kwargs.get("data")))
    mapped = {k: v for k, v in mapped.items() if v is not None}
    if header_order is not None:
        extensions = dict(mapped.get("extensions") or extra.get("extensions") or {})
        extensions["header_order"] = header_order
        mapped["extensions"] = extensions
    return merge_extra(mapped, extra)


class HttpxSync(SyncBackend):
    def __init__(
        self,
        impersonate: Optional[str] = None,
        *,
        proxy: Optional[str] = None,
        timeout: float = 30,
        verify: bool = True,
        headers: Optional[dict] = None,
        cookies: Optional[dict] = None,
        allow_redirects: bool = True,
        extra: Optional[dict[str, Any]] = None,
    ) -> None:
        httpx, _utls = _import_httpx()
        extra = dict(extra or {})
        h2_patch = extra.pop("h2_patch", True)
        if h2_patch:
            from ._httpx_patch import patch_httpcore_chrome_h2
            patch_httpcore_chrome_h2()
        profile = resolve("httpx", impersonate)
        ctx = _make_context(profile, verify)
        transport = extra.pop("transport", None) or httpx.HTTPTransport(
            verify=ctx, http2=True, proxy=proxy,
        )
        mapped = {
            "transport": transport,
            "timeout": timeout,
            "trust_env": False,
            "verify": False,
            "follow_redirects": allow_redirects,
            "headers": headers,
            "cookies": cookies,
            "event_hooks": {"request": [_on_request]},
        }
        mapped = {k: v for k, v in mapped.items() if v is not None}
        kwargs = merge_extra(mapped, extra)
        self._client = httpx.Client(**kwargs)
        self._client._headers = httpx.Headers([])

    def request(self, method: str, url: str, **kwargs: Any) -> Response:
        return _wrap(self._client.request(method, url, **_request_kwargs(kwargs)))

    def close(self) -> None:
        self._client.close()

    def get_cookies(self) -> dict[str, str]:
        return cookies_to_dict(self._client.cookies)

    def set_cookies(self, cookies: dict[str, str], url: Optional[str] = None) -> None:
        self._client.cookies.update(cookies)

    @property
    def raw(self) -> Any:
        return self._client


class HttpxAsync(AsyncBackend):
    def __init__(
        self,
        impersonate: Optional[str] = None,
        *,
        proxy: Optional[str] = None,
        timeout: float = 30,
        verify: bool = True,
        headers: Optional[dict] = None,
        cookies: Optional[dict] = None,
        allow_redirects: bool = True,
        extra: Optional[dict[str, Any]] = None,
    ) -> None:
        httpx, _utls = _import_httpx()
        extra = dict(extra or {})
        h2_patch = extra.pop("h2_patch", True)
        if h2_patch:
            from ._httpx_patch import patch_httpcore_chrome_h2
            patch_httpcore_chrome_h2()
        profile = resolve("httpx", impersonate)
        ctx = _make_context(profile, verify)
        transport = extra.pop("transport", None) or httpx.AsyncHTTPTransport(
            verify=ctx, http2=True, proxy=proxy,
        )
        mapped = {
            "transport": transport,
            "timeout": timeout,
            "trust_env": False,
            "verify": False,
            "follow_redirects": allow_redirects,
            "headers": headers,
            "cookies": cookies,
            "event_hooks": {"request": [_on_request_async]},
        }
        mapped = {k: v for k, v in mapped.items() if v is not None}
        kwargs = merge_extra(mapped, extra)
        self._client = httpx.AsyncClient(**kwargs)
        self._client._headers = httpx.Headers([])

    async def request(self, method: str, url: str, **kwargs: Any) -> Response:
        return _wrap(await self._client.request(method, url, **_request_kwargs(kwargs)))

    async def aclose(self) -> None:
        await self._client.aclose()

    def get_cookies(self) -> dict[str, str]:
        return cookies_to_dict(self._client.cookies)

    def set_cookies(self, cookies: dict[str, str], url: Optional[str] = None) -> None:
        self._client.cookies.update(cookies)

    @property
    def raw(self) -> Any:
        return self._client
