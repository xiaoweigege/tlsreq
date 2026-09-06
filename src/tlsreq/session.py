from __future__ import annotations

from typing import Any, Optional

from .backends import create_async_backend, create_sync_backend
from .response import Response

class Session:
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
        self.backend = backend
        self.impersonate = impersonate
        self._impl = create_sync_backend(
            backend,
            impersonate=impersonate,
            proxy=proxy,
            timeout=timeout,
            verify=verify,
            headers=headers,
            cookies=cookies,
            allow_redirects=allow_redirects,
            extra=extra,
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

    def get(self, url: str, **kwargs: Any) -> Response:
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs: Any) -> Response:
        return self.request("POST", url, **kwargs)

    def put(self, url: str, **kwargs: Any) -> Response:
        return self.request("PUT", url, **kwargs)

    def patch(self, url: str, **kwargs: Any) -> Response:
        return self.request("PATCH", url, **kwargs)

    def delete(self, url: str, **kwargs: Any) -> Response:
        return self.request("DELETE", url, **kwargs)

    def head(self, url: str, **kwargs: Any) -> Response:
        return self.request("HEAD", url, **kwargs)

    def options(self, url: str, **kwargs: Any) -> Response:
        return self.request("OPTIONS", url, **kwargs)

    @property
    def cookies(self) -> dict[str, str]:
        return self._impl.get_cookies()

    def set_cookies(self, cookies: dict[str, str], url: Optional[str] = None) -> None:
        self._impl.set_cookies(cookies, url=url)

    @property
    def raw(self) -> Any:
        return self._impl.raw

    def close(self) -> None:
        self._impl.close()

    def __enter__(self) -> "Session":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()


class AsyncSession:
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
        self.backend = backend
        self.impersonate = impersonate
        self._impl = create_async_backend(
            backend,
            impersonate=impersonate,
            proxy=proxy,
            timeout=timeout,
            verify=verify,
            headers=headers,
            cookies=cookies,
            allow_redirects=allow_redirects,
            extra=extra,
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

    async def get(self, url: str, **kwargs: Any) -> Response:
        return await self.request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs: Any) -> Response:
        return await self.request("POST", url, **kwargs)

    async def put(self, url: str, **kwargs: Any) -> Response:
        return await self.request("PUT", url, **kwargs)

    async def patch(self, url: str, **kwargs: Any) -> Response:
        return await self.request("PATCH", url, **kwargs)

    async def delete(self, url: str, **kwargs: Any) -> Response:
        return await self.request("DELETE", url, **kwargs)

    async def head(self, url: str, **kwargs: Any) -> Response:
        return await self.request("HEAD", url, **kwargs)

    async def options(self, url: str, **kwargs: Any) -> Response:
        return await self.request("OPTIONS", url, **kwargs)

    @property
    def cookies(self) -> dict[str, str]:
        return self._impl.get_cookies()

    def set_cookies(self, cookies: dict[str, str], url: Optional[str] = None) -> None:
        self._impl.set_cookies(cookies, url=url)

    @property
    def raw(self) -> Any:
        return self._impl.raw

    async def close(self) -> None:
        await self._impl.aclose()

    async def __aenter__(self) -> "AsyncSession":
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self.close()
