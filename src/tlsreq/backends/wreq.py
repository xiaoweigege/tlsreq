from __future__ import annotations

from datetime import timedelta
from typing import Any, Optional

from ..errors import BackendNotInstalled, UnknownFingerprint
from ..fingerprints import resolve
from ..response import Response, cookies_to_dict, headers_to_dict
from .base import AsyncBackend, SyncBackend, merge_extra


def _import_wreq():
    try:
        import wreq
    except ImportError as exc:
        raise BackendNotInstalled(
            "wreq backend 需要: pip install 'tlsreq[wreq]'"
        ) from exc
    return wreq


def _method(wreq: Any, method: str) -> Any:
    name = method.upper()
    value = getattr(wreq.Method, name, None)
    if value is None:
        raise ValueError(f"wreq 不支持 method {method!r}")
    return value


def _emulation(wreq: Any, impersonate: Optional[str]) -> Any:
    name = resolve("wreq", impersonate)
    emu = getattr(wreq.Emulation, name, None)
    if emu is None:
        available = [item for item in dir(wreq.Emulation) if item.startswith("Chrome") or item.startswith("Firefox") or item.startswith("Safari")]
        raise UnknownFingerprint(f"wreq 没有指纹 {name!r}。可用: {available}")
    return emu


def _as_timeout(value: Any) -> Any:
    if value is None or isinstance(value, timedelta):
        return value
    return timedelta(seconds=float(value))


def _redirect(wreq: Any, allow_redirects: bool) -> Any:
    if allow_redirects:
        return wreq.redirect.Policy.limited(5)
    return wreq.redirect.Policy.none()


def _status(resp: Any) -> int:
    value = getattr(resp, "status", 0)
    try:
        return int(value)
    except (TypeError, ValueError):
        as_int = getattr(value, "as_int", None) or getattr(value, "as_u16", None)
        if callable(as_int):
            return int(as_int())
        return int(getattr(value, "value", 0) or 0)


def _wrap_sync(resp: Any) -> Response:
    content = resp.bytes() if callable(getattr(resp, "bytes", None)) else b""
    if not isinstance(content, (bytes, bytearray)):
        content = bytes(content or b"")
    return Response(
        status_code=_status(resp),
        content=content,
        headers=headers_to_dict(resp.headers),
        url=str(resp.url),
        cookies=cookies_to_dict(getattr(resp, "cookies", None)),
        http_version=str(getattr(resp, "version", "") or "") or None,
        raw=resp,
    )


async def _wrap_async(resp: Any) -> Response:
    content = await resp.bytes()
    if not isinstance(content, (bytes, bytearray)):
        content = bytes(content or b"")
    return Response(
        status_code=_status(resp),
        content=content,
        headers=headers_to_dict(resp.headers),
        url=str(resp.url),
        cookies=cookies_to_dict(getattr(resp, "cookies", None)),
        http_version=str(getattr(resp, "version", "") or "") or None,
        raw=resp,
    )


def _request_kwargs(wreq: Any, kwargs: dict[str, Any]) -> dict[str, Any]:
    extra = dict(kwargs.pop("extra", None) or {})
    header_order = kwargs.pop("header_order", None)
    mapped: dict[str, Any] = {
        "headers": kwargs.get("headers"),
        "query": kwargs.get("params"),
        "json": kwargs.get("json"),
        "cookies": kwargs.get("cookies"),
    }
    data = kwargs.get("data")
    if data is not None:
        mapped["body"] = data
    timeout = kwargs.get("timeout")
    if timeout is not None:
        mapped["timeout"] = _as_timeout(timeout)
    allow_redirects = kwargs.get("allow_redirects")
    if allow_redirects is not None:
        mapped["redirect"] = _redirect(wreq, bool(allow_redirects))
    mapped = {k: v for k, v in mapped.items() if v is not None}
    if header_order is not None:
        mapped["orig_headers"] = header_order
    return merge_extra(mapped, extra)


def _client_kwargs(
    wreq: Any,
    impersonate: Optional[str],
    proxy: Optional[str],
    timeout: float,
    verify: bool,
    headers: Optional[dict],
    allow_redirects: bool,
    extra: Optional[dict[str, Any]],
) -> dict[str, Any]:
    mapped: dict[str, Any] = {
        "emulation": _emulation(wreq, impersonate),
        "cookie_store": True,
        "tls_verify": verify,
        "timeout": _as_timeout(timeout),
        "redirect": _redirect(wreq, allow_redirects),
        "headers": headers,
    }
    if proxy:
        mapped["proxies"] = [wreq.Proxy.all(proxy)]
    mapped = {k: v for k, v in mapped.items() if v is not None}
    return merge_extra(mapped, extra)


class WreqSync(SyncBackend):
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
        wreq = _import_wreq()
        self._wreq = wreq
        self._client = wreq.blocking.Client(
            **_client_kwargs(wreq, impersonate, proxy, timeout, verify, headers, allow_redirects, extra)
        )
        if cookies:
            self.set_cookies(cookies)

    def request(self, method: str, url: str, **kwargs: Any) -> Response:
        resp = self._client.request(
            _method(self._wreq, method), url, **_request_kwargs(self._wreq, kwargs)
        )
        return _wrap_sync(resp)

    def close(self) -> None:
        self._client.close()

    def get_cookies(self) -> dict[str, str]:
        jar = getattr(self._client, "cookie_jar", None)
        if jar is None:
            return {}
        return {cookie.name: cookie.value for cookie in jar.get_all()}

    def set_cookies(self, cookies: dict[str, str], url: Optional[str] = None) -> None:
        jar = getattr(self._client, "cookie_jar", None)
        if jar is None:
            return
        if not url:
            raise ValueError("wreq set_cookies 需要 url")
        for name, value in cookies.items():
            jar.add(self._wreq.Cookie(name=name, value=value), url=url)

    @property
    def raw(self) -> Any:
        return self._client


class WreqAsync(AsyncBackend):
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
        wreq = _import_wreq()
        self._wreq = wreq
        self._client = wreq.Client(
            **_client_kwargs(wreq, impersonate, proxy, timeout, verify, headers, allow_redirects, extra)
        )
        self._pending_cookies = dict(cookies or {})

    async def request(self, method: str, url: str, **kwargs: Any) -> Response:
        if self._pending_cookies:
            self.set_cookies(self._pending_cookies, url=url)
            self._pending_cookies = {}
        resp = await self._client.request(
            _method(self._wreq, method), url, **_request_kwargs(self._wreq, kwargs)
        )
        return await _wrap_async(resp)

    async def aclose(self) -> None:
        self._client.close()

    def get_cookies(self) -> dict[str, str]:
        jar = getattr(self._client, "cookie_jar", None)
        if jar is None:
            return {}
        return {cookie.name: cookie.value for cookie in jar.get_all()}

    def set_cookies(self, cookies: dict[str, str], url: Optional[str] = None) -> None:
        jar = getattr(self._client, "cookie_jar", None)
        if jar is None:
            self._pending_cookies.update(cookies)
            return
        if not url:
            self._pending_cookies.update(cookies)
            return
        for name, value in cookies.items():
            jar.add(self._wreq.Cookie(name=name, value=value), url=url)

    @property
    def raw(self) -> Any:
        return self._client
