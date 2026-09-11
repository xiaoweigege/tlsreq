from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from .backends import create_async_backend, create_sync_backend
from .backends.base import AsyncBackend, SyncBackend
from .response import Response
from .types import BackendName, ImpersonateName


class Session:
    def __init__(
        self,
        backend: BackendName = "httpx",
        impersonate: ImpersonateName | None = None,
        *,
        proxy: str | None = None,
        timeout: float = 30,
        verify: bool = True,
        headers: Mapping[str, str] | None = None,
        cookies: Mapping[str, str] | None = None,
        allow_redirects: bool = True,
        extra: dict[str, Any] | None = None,
    ) -> None:
        self.backend = backend
        self.impersonate = impersonate
        self._impl: SyncBackend = create_sync_backend(
            backend,
            impersonate=impersonate,
            proxy=proxy,
            timeout=timeout,
            verify=verify,
            headers=dict(headers) if headers is not None else None,
            cookies=dict(cookies) if cookies is not None else None,
            allow_redirects=allow_redirects,
            extra=extra,
        )

    @property
    def cookies(self) -> dict[str, str]:
        return self._impl.get_cookies()

    def set_cookies(self, cookies: Mapping[str, str], url: str | None = None) -> None:
        self._impl.set_cookies(dict(cookies), url=url)

    @property
    def raw(self) -> Any:
        return self._impl.raw

    def request(
        self,
        method: str,
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        data: Any = None,
        json: Any = None,
        cookies: Mapping[str, str] | None = None,
        timeout: float | None = None,
        allow_redirects: bool | None = None,
        header_order: list[str] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> Response:
        return self._impl.request(
            method.upper(),
            url,
            headers=dict(headers) if headers is not None else None,
            params=dict(params) if params is not None else None,
            data=data,
            json=json,
            cookies=dict(cookies) if cookies is not None else None,
            timeout=timeout,
            allow_redirects=allow_redirects,
            header_order=header_order,
            extra=extra,
        )

    def get(
        self,
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        cookies: Mapping[str, str] | None = None,
        timeout: float | None = None,
        allow_redirects: bool | None = None,
        header_order: list[str] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> Response:
        return self.request(
            "GET",
            url,
            headers=headers,
            params=params,
            cookies=cookies,
            timeout=timeout,
            allow_redirects=allow_redirects,
            header_order=header_order,
            extra=extra,
        )

    def post(
        self,
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        data: Any = None,
        json: Any = None,
        cookies: Mapping[str, str] | None = None,
        timeout: float | None = None,
        allow_redirects: bool | None = None,
        header_order: list[str] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> Response:
        return self.request(
            "POST",
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

    def put(
        self,
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        data: Any = None,
        json: Any = None,
        cookies: Mapping[str, str] | None = None,
        timeout: float | None = None,
        allow_redirects: bool | None = None,
        header_order: list[str] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> Response:
        return self.request(
            "PUT",
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

    def patch(
        self,
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        data: Any = None,
        json: Any = None,
        cookies: Mapping[str, str] | None = None,
        timeout: float | None = None,
        allow_redirects: bool | None = None,
        header_order: list[str] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> Response:
        return self.request(
            "PATCH",
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

    def delete(
        self,
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        data: Any = None,
        json: Any = None,
        cookies: Mapping[str, str] | None = None,
        timeout: float | None = None,
        allow_redirects: bool | None = None,
        header_order: list[str] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> Response:
        return self.request(
            "DELETE",
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

    def head(
        self,
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        cookies: Mapping[str, str] | None = None,
        timeout: float | None = None,
        allow_redirects: bool | None = None,
        header_order: list[str] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> Response:
        return self.request(
            "HEAD",
            url,
            headers=headers,
            params=params,
            cookies=cookies,
            timeout=timeout,
            allow_redirects=allow_redirects,
            header_order=header_order,
            extra=extra,
        )

    def options(
        self,
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        cookies: Mapping[str, str] | None = None,
        timeout: float | None = None,
        allow_redirects: bool | None = None,
        header_order: list[str] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> Response:
        return self.request(
            "OPTIONS",
            url,
            headers=headers,
            params=params,
            cookies=cookies,
            timeout=timeout,
            allow_redirects=allow_redirects,
            header_order=header_order,
            extra=extra,
        )

    def close(self) -> None:
        self._impl.close()

    def __enter__(self) -> Session:
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()


class AsyncSession:
    def __init__(
        self,
        backend: BackendName = "httpx",
        impersonate: ImpersonateName | None = None,
        *,
        proxy: str | None = None,
        timeout: float = 30,
        verify: bool = True,
        headers: Mapping[str, str] | None = None,
        cookies: Mapping[str, str] | None = None,
        allow_redirects: bool = True,
        extra: dict[str, Any] | None = None,
    ) -> None:
        self.backend = backend
        self.impersonate = impersonate
        self._impl: AsyncBackend = create_async_backend(
            backend,
            impersonate=impersonate,
            proxy=proxy,
            timeout=timeout,
            verify=verify,
            headers=dict(headers) if headers is not None else None,
            cookies=dict(cookies) if cookies is not None else None,
            allow_redirects=allow_redirects,
            extra=extra,
        )

    @property
    def cookies(self) -> dict[str, str]:
        return self._impl.get_cookies()

    def set_cookies(self, cookies: Mapping[str, str], url: str | None = None) -> None:
        self._impl.set_cookies(dict(cookies), url=url)

    @property
    def raw(self) -> Any:
        return self._impl.raw

    async def request(
        self,
        method: str,
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        data: Any = None,
        json: Any = None,
        cookies: Mapping[str, str] | None = None,
        timeout: float | None = None,
        allow_redirects: bool | None = None,
        header_order: list[str] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> Response:
        return await self._impl.request(
            method.upper(),
            url,
            headers=dict(headers) if headers is not None else None,
            params=dict(params) if params is not None else None,
            data=data,
            json=json,
            cookies=dict(cookies) if cookies is not None else None,
            timeout=timeout,
            allow_redirects=allow_redirects,
            header_order=header_order,
            extra=extra,
        )

    async def get(
        self,
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        cookies: Mapping[str, str] | None = None,
        timeout: float | None = None,
        allow_redirects: bool | None = None,
        header_order: list[str] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> Response:
        return await self.request(
            "GET",
            url,
            headers=headers,
            params=params,
            cookies=cookies,
            timeout=timeout,
            allow_redirects=allow_redirects,
            header_order=header_order,
            extra=extra,
        )

    async def post(
        self,
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        data: Any = None,
        json: Any = None,
        cookies: Mapping[str, str] | None = None,
        timeout: float | None = None,
        allow_redirects: bool | None = None,
        header_order: list[str] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> Response:
        return await self.request(
            "POST",
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

    async def put(
        self,
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        data: Any = None,
        json: Any = None,
        cookies: Mapping[str, str] | None = None,
        timeout: float | None = None,
        allow_redirects: bool | None = None,
        header_order: list[str] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> Response:
        return await self.request(
            "PUT",
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

    async def patch(
        self,
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        data: Any = None,
        json: Any = None,
        cookies: Mapping[str, str] | None = None,
        timeout: float | None = None,
        allow_redirects: bool | None = None,
        header_order: list[str] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> Response:
        return await self.request(
            "PATCH",
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

    async def delete(
        self,
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        data: Any = None,
        json: Any = None,
        cookies: Mapping[str, str] | None = None,
        timeout: float | None = None,
        allow_redirects: bool | None = None,
        header_order: list[str] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> Response:
        return await self.request(
            "DELETE",
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

    async def head(
        self,
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        cookies: Mapping[str, str] | None = None,
        timeout: float | None = None,
        allow_redirects: bool | None = None,
        header_order: list[str] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> Response:
        return await self.request(
            "HEAD",
            url,
            headers=headers,
            params=params,
            cookies=cookies,
            timeout=timeout,
            allow_redirects=allow_redirects,
            header_order=header_order,
            extra=extra,
        )

    async def options(
        self,
        url: str,
        *,
        headers: Mapping[str, str] | None = None,
        params: Mapping[str, Any] | None = None,
        cookies: Mapping[str, str] | None = None,
        timeout: float | None = None,
        allow_redirects: bool | None = None,
        header_order: list[str] | None = None,
        extra: dict[str, Any] | None = None,
    ) -> Response:
        return await self.request(
            "OPTIONS",
            url,
            headers=headers,
            params=params,
            cookies=cookies,
            timeout=timeout,
            allow_redirects=allow_redirects,
            header_order=header_order,
            extra=extra,
        )

    async def close(self) -> None:
        await self._impl.aclose()

    async def __aenter__(self) -> AsyncSession:
        return self

    async def __aexit__(self, *exc: Any) -> None:
        await self.close()
