from __future__ import annotations

from typing import Any, Optional

from .backends import create_async_backend, create_sync_backend
from .response import Response

_HTTP_METHODS = ("get", "post", "put", "patch", "delete", "head", "options")


class _Facade:
    def __init__(self, backend: str, impersonate: Optional[str], impl: Any) -> None:
        self.backend = backend
        self.impersonate = impersonate
        self._impl = impl

    @property
    def cookies(self) -> dict[str, str]:
        return self._impl.get_cookies()

    def set_cookies(self, cookies: dict[str, str], url: Optional[str] = None) -> None:
        self._impl.set_cookies(cookies, url=url)

    @property
    def raw(self) -> Any:
        return self._impl.raw


class Session(_Facade):
    def __init__(
        self,
        backend: str,
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
        super().__init__(
            backend,
            impersonate,
            create_sync_backend(
                backend,
                impersonate=impersonate,
                proxy=proxy,
                timeout=timeout,
                verify=verify,
                headers=headers,
                cookies=cookies,
                allow_redirects=allow_redirects,
                extra=extra,
            ),
        )

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        data: Any = None,
        json: Any = None,
        cookies: Optional[dict] = None,
        timeout: Any = None,
        allow_redirects: Optional[bool] = None,
        header_order: Optional[list[str]] = None,
        extra: Optional[dict[str, Any]] = None,
    ) -> Response:
        return self._impl.request(
            method.upper(),
            url,
            headers=headers,
            params=params,
            data=data,
            json=json,
            cookies=cookies,
            timeout=timeout,
            allow_redirects=allow_redirects,
            header_order=header_order,
            extra=extra,
        )

    def close(self) -> None:
        self._impl.close()

    def __enter__(self) -> "Session":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()


class AsyncSession(_Facade):
    def __init__(
        self,
        backend: str,
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
        super().__init__(
            backend,
            impersonate,
            create_async_backend(
                backend,
                impersonate=impersonate,
                proxy=proxy,
                timeout=timeout,
                verify=verify,
                headers=headers,
                cookies=cookies,
                allow_redirects=allow_redirects,
                extra=extra,
            ),
        )

    async def request(
        self,
        method: str,
        url: str,
        *,
        headers: Optional[dict] = None,
        params: Optional[dict] = None,
        data: Any = None,
        json: Any = None,
        cookies: Optional[dict] = None,
        timeout: Any = None,
        allow_redirects: Optional[bool] = None,
        header_order: Optional[list[str]] = None,
        extra: Optional[dict[str, Any]] = None,
    ) -> Response:
        return await self._impl.request(
            method.upper(),
            url,
            headers=headers,
            params=params,
            data=data,
            json=json,
            cookies=cookies,
            timeout=timeout,
            allow_redirects=allow_redirects,
            header_order=header_order,
            extra=extra,
        )

    async def close(self) -> None:
        await self._impl.aclose()

    async def __aenter__(self) -> "AsyncSession":
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self.close()


def _sync_http(verb: str):
    def method(self: Session, url: str, **kwargs: Any) -> Response:
        return self.request(verb, url, **kwargs)

    method.__name__ = verb.lower()
    method.__qualname__ = f"Session.{verb.lower()}"
    return method


def _async_http(verb: str):
    async def method(self: AsyncSession, url: str, **kwargs: Any) -> Response:
        return await self.request(verb, url, **kwargs)

    method.__name__ = verb.lower()
    method.__qualname__ = f"AsyncSession.{verb.lower()}"
    return method


for _verb in _HTTP_METHODS:
    setattr(Session, _verb, _sync_http(_verb.upper()))
    setattr(AsyncSession, _verb, _async_http(_verb.upper()))
