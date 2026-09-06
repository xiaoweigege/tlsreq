"""httpcore/h2：Chrome 152 SETTINGS、连接窗口、HEADERS Priority。"""
from __future__ import annotations

import collections
from typing import Any

import h2.settings

from ..chrome_h2 import (
    CONNECTION_WINDOW_INCREMENT,
    ENABLE_PUSH,
    H2_HOP_BY_HOP,
    HEADER_TABLE_SIZE,
    INITIAL_WINDOW_SIZE,
    MAX_HEADER_LIST_SIZE,
    PRIORITY_DEPENDS_ON,
    PRIORITY_EXCLUSIVE,
    PRIORITY_WEIGHT,
)

_PATCHED = False


def _chrome_local_settings() -> h2.settings.Settings:
    settings = h2.settings.Settings(
        client=True,
        initial_values={
            h2.settings.SettingCodes.HEADER_TABLE_SIZE: HEADER_TABLE_SIZE,
            h2.settings.SettingCodes.ENABLE_PUSH: ENABLE_PUSH,
            h2.settings.SettingCodes.INITIAL_WINDOW_SIZE: INITIAL_WINDOW_SIZE,
            h2.settings.SettingCodes.MAX_HEADER_LIST_SIZE: MAX_HEADER_LIST_SIZE,
            h2.settings.SettingCodes.MAX_CONCURRENT_STREAMS: 100,
        },
    )
    del settings[h2.settings.SettingCodes.MAX_FRAME_SIZE]
    del settings[h2.settings.SettingCodes.ENABLE_CONNECT_PROTOCOL]
    del settings[h2.settings.SettingCodes.MAX_CONCURRENT_STREAMS]
    return settings


def _restore_local_only(settings: h2.settings.Settings) -> None:
    """SETTINGS 帧发出后再补回 h2/httpcore 内部会读的项，避免再发一帧。"""
    codes = h2.settings.SettingCodes
    settings._settings.setdefault(codes.MAX_CONCURRENT_STREAMS, collections.deque([100]))
    settings._settings.setdefault(codes.MAX_FRAME_SIZE, collections.deque([16384]))


def patch_httpcore_chrome_h2() -> None:
    global _PATCHED
    if _PATCHED:
        return

    from httpcore._async.http2 import AsyncHTTP2Connection
    from httpcore._async.http2 import has_body_headers as async_has_body_headers
    from httpcore._sync.http2 import HTTP2Connection
    from httpcore._sync.http2 import has_body_headers as sync_has_body_headers

    async def async_send_connection_init(self: Any, request: Any) -> None:
        self._h2_state.local_settings = _chrome_local_settings()
        self._h2_state.initiate_connection()
        _restore_local_only(self._h2_state.local_settings)
        self._h2_state.increment_flow_control_window(CONNECTION_WINDOW_INCREMENT)
        await self._write_outgoing_data(request)

    def sync_send_connection_init(self: Any, request: Any) -> None:
        self._h2_state.local_settings = _chrome_local_settings()
        self._h2_state.initiate_connection()
        _restore_local_only(self._h2_state.local_settings)
        self._h2_state.increment_flow_control_window(CONNECTION_WINDOW_INCREMENT)
        self._write_outgoing_data(request)

    async def async_send_request_headers(self: Any, request: Any, stream_id: int) -> None:
        end_stream = not async_has_body_headers(request)
        authority = [value for key, value in request.headers if key.lower() == b"host"][0]
        headers = [
            (b":method", request.method),
            (b":authority", authority),
            (b":scheme", request.url.scheme),
            (b":path", request.url.target),
        ] + [
            (key.lower(), value)
            for key, value in request.headers
            if key.lower() not in H2_HOP_BY_HOP
        ]
        self._h2_state.send_headers(
            stream_id,
            headers,
            end_stream=end_stream,
            priority_weight=PRIORITY_WEIGHT,
            priority_depends_on=PRIORITY_DEPENDS_ON,
            priority_exclusive=PRIORITY_EXCLUSIVE,
        )
        await self._write_outgoing_data(request)

    def sync_send_request_headers(self: Any, request: Any, stream_id: int) -> None:
        end_stream = not sync_has_body_headers(request)
        authority = [value for key, value in request.headers if key.lower() == b"host"][0]
        headers = [
            (b":method", request.method),
            (b":authority", authority),
            (b":scheme", request.url.scheme),
            (b":path", request.url.target),
        ] + [
            (key.lower(), value)
            for key, value in request.headers
            if key.lower() not in H2_HOP_BY_HOP
        ]
        self._h2_state.send_headers(
            stream_id,
            headers,
            end_stream=end_stream,
            priority_weight=PRIORITY_WEIGHT,
            priority_depends_on=PRIORITY_DEPENDS_ON,
            priority_exclusive=PRIORITY_EXCLUSIVE,
        )
        self._write_outgoing_data(request)

    AsyncHTTP2Connection._send_connection_init = async_send_connection_init
    AsyncHTTP2Connection._send_request_headers = async_send_request_headers
    HTTP2Connection._send_connection_init = sync_send_connection_init
    HTTP2Connection._send_request_headers = sync_send_request_headers
    _PATCHED = True
