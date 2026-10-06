from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeVar

from .backends import create_async_backend, create_sync_backend
from .backends.base import AsyncBackend, SyncBackend
from .response import Response
from .types import Backend, httpx

_Imp = TypeVar("_Imp", bound=str)


def _copy_map(mapping: Mapping[str, str] | None) -> dict[str, str] | None:
    if mapping is None:
        return None
    return dict(mapping)


def _bind_sync(
    session: Session,
    backend: str,
    impersonate: str | None,
    *,
    proxy: str | None,
    timeout: float,
    verify: bool,
    headers: Mapping[str, str] | None,
    cookies: Mapping[str, str] | None,
    allow_redirects: bool,
    extra: dict[str, Any] | None,
) -> None:
    session.backend = backend
    session.impersonate = impersonate
    session._impl = create_sync_backend(
        backend,
        impersonate=impersonate,
        proxy=proxy,
        timeout=timeout,
        verify=verify,
        headers=_copy_map(headers),
        cookies=_copy_map(cookies),
        allow_redirects=allow_redirects,
        extra=extra,
    )


def _bind_async(
    session: AsyncSession,
    backend: str,
    impersonate: str | None,
    *,
    proxy: str | None,
    timeout: float,
    verify: bool,
    headers: Mapping[str, str] | None,
    cookies: Mapping[str, str] | None,
    allow_redirects: bool,
    extra: dict[str, Any] | None,
) -> None:
    session.backend = backend
    session.impersonate = impersonate
    session._impl = create_async_backend(
        backend,
        impersonate=impersonate,
        proxy=proxy,
        timeout=timeout,
        verify=verify,
        headers=_copy_map(headers),
        cookies=_copy_map(cookies),
        allow_redirects=allow_redirects,
        extra=extra,
    )


def _backend_name(backend: Backend[Any] | str) -> str:
    if isinstance(backend, Backend):
        return backend.name
    if isinstance(backend, str):
        return backend
    raise TypeError(f"backend 必须是 Backend 或 str，收到 {type(backend).__name__}")


class Session:
    backend: str
    impersonate: str | None
    _impl: SyncBackend

    def __init__(
        self,
        backend: Backend[_Imp] | str = httpx,
        impersonate: _Imp | None = None,
        *,
        proxy: str | None = None,
        timeout: float = 30,
        verify: bool = True,
        headers: Mapping[str, str] | None = None,
        cookies: Mapping[str, str] | None = None,
        allow_redirects: bool = True,
        extra: dict[str, Any] | None = None,
    ) -> None:
        _bind_sync(
            self,
            _backend_name(backend),
            impersonate,
            proxy=proxy,
            timeout=timeout,
            verify=verify,
            headers=headers,
            cookies=cookies,
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
    backend: str
    impersonate: str | None
    _impl: AsyncBackend

    def __init__(
        self,
        backend: Backend[_Imp] | str = httpx,
        impersonate: _Imp | None = None,
        *,
        proxy: str | None = None,
        timeout: float = 30,
        verify: bool = True,
        headers: Mapping[str, str] | None = None,
        cookies: Mapping[str, str] | None = None,
        allow_redirects: bool = True,
        extra: dict[str, Any] | None = None,
    ) -> None:
        _bind_async(
            self,
            _backend_name(backend),
            impersonate,
            proxy=proxy,
            timeout=timeout,
            verify=verify,
            headers=headers,
            cookies=cookies,
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
