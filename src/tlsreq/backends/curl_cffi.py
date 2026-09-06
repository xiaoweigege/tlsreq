from __future__ import annotations

from typing import Any, Optional

from ..errors import BackendNotInstalled
from ..fingerprints import resolve
from ..response import Response, cookies_to_dict, headers_to_dict, http_version_of, status_code_of
from .base import AsyncBackend, SyncBackend, merge_extra


def _import_curl_cffi():
    try:
        from curl_cffi import requests
    except ImportError as exc:
        raise BackendNotInstalled(
            "curl_cffi backend 需要: pip install 'tlsreq[curl_cffi]'"
        ) from exc
    return requests


def _wrap(resp: Any) -> Response:
    content = resp.content if isinstance(getattr(resp, "content", None), (bytes, bytearray)) else b""
    cookies = cookies_to_dict(getattr(resp, "cookies", None))
    return Response(
        status_code=status_code_of(resp),
        content=content,
        headers=headers_to_dict(resp.headers),
        url=str(resp.url),
        cookies=cookies,
        http_version=http_version_of(resp),
        raw=resp,
    )


def _request_kwargs(kwargs: dict[str, Any]) -> dict[str, Any]:
    extra = dict(kwargs.pop("extra", None) or {})
    kwargs.pop("header_order", None)
    mapped = {
        "headers": kwargs.get("headers"),
        "params": kwargs.get("params"),
        "data": kwargs.get("data"),
        "json": kwargs.get("json"),
        "cookies": kwargs.get("cookies"),
        "timeout": kwargs.get("timeout"),
        "allow_redirects": kwargs.get("allow_redirects"),
    }
    mapped = {k: v for k, v in mapped.items() if v is not None}
    return merge_extra(mapped, extra)


def _session_kwargs(
    impersonate: Optional[str],
    proxy: Optional[str],
    timeout: float,
    verify: bool,
    headers: Optional[dict],
    cookies: Optional[dict],
    allow_redirects: bool,
    extra: Optional[dict[str, Any]],
) -> dict[str, Any]:
    mapped = {
        "impersonate": resolve("curl_cffi", impersonate),
        "proxy": proxy,
        "timeout": timeout,
        "verify": verify,
        "headers": headers,
        "cookies": cookies,
        "allow_redirects": allow_redirects,
    }
    mapped = {k: v for k, v in mapped.items() if v is not None}
    return merge_extra(mapped, extra)


class CurlCffiSync(SyncBackend):
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
        requests = _import_curl_cffi()
        self._session = requests.Session(
            **_session_kwargs(impersonate, proxy, timeout, verify, headers, cookies, allow_redirects, extra)
        )

    def request(self, method: str, url: str, **kwargs: Any) -> Response:
        return _wrap(self._session.request(method, url, **_request_kwargs(kwargs)))

    def close(self) -> None:
        self._session.close()

    def get_cookies(self) -> dict[str, str]:
        jar = self._session.cookies
        if hasattr(jar, "get_dict"):
            return dict(jar.get_dict())
        return cookies_to_dict(jar)

    def set_cookies(self, cookies: dict[str, str], url: Optional[str] = None) -> None:
        for name, value in cookies.items():
            self._session.cookies.set(name, value)

    @property
    def raw(self) -> Any:
        return self._session


class CurlCffiAsync(AsyncBackend):
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
        requests = _import_curl_cffi()
        self._session = requests.AsyncSession(
            **_session_kwargs(impersonate, proxy, timeout, verify, headers, cookies, allow_redirects, extra)
        )

    async def request(self, method: str, url: str, **kwargs: Any) -> Response:
        return _wrap(await self._session.request(method, url, **_request_kwargs(kwargs)))

    async def aclose(self) -> None:
        await self._session.close()

    def get_cookies(self) -> dict[str, str]:
        jar = self._session.cookies
        if hasattr(jar, "get_dict"):
            return dict(jar.get_dict())
        return cookies_to_dict(jar)

    def set_cookies(self, cookies: dict[str, str], url: Optional[str] = None) -> None:
        for name, value in cookies.items():
            self._session.cookies.set(name, value)

    @property
    def raw(self) -> Any:
        return self._session
