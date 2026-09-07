from __future__ import annotations

from typing import Any, Optional

from ..errors import BackendNotInstalled
from ..fingerprints import resolve
from ..response import Response, cookies_to_dict, headers_to_dict, http_version_of, status_code_of
from ..utls_release import fingerprint_from_preset
from .base import AsyncBackend, SyncBackend, merge_extra


def _import_niquests():
    try:
        import niquests
        import utls
        from niquests.extensions.tls import TLSConfiguration
    except ImportError as exc:
        raise BackendNotInstalled(
            "niquests backend 需要: pip install 'tlsreq[niquests]' "
            "（会装 xutls，import 名仍是 utls）"
        ) from exc
    return niquests, utls, TLSConfiguration


def _make_ssl_context(profile: str, verify: bool):
    niquests, utls, _tls = _import_niquests()
    ctx = utls.create_default_context()
    fp = fingerprint_from_preset(utls, profile)
    fp._http_headers = {}
    ctx.set_fingerprint(fp)
    if not verify:
        import ssl
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
    return ctx


def _pin_proxy_disabled_svn(manager: Any) -> None:
    from urllib3 import HttpVersion

    kw = getattr(manager, "connection_pool_kw", None)
    if kw is None:
        return
    disabled = set(kw.get("disabled_svn") or set())
    disabled.add(HttpVersion.h3)
    kw["disabled_svn"] = disabled


def _attach_ssl_context(session: Any, ctx: Any) -> None:
    adapter = session.adapters["https://"]
    adapter.poolmanager.connection_pool_kw["ssl_context"] = ctx
    orig = adapter.proxy_manager_for

    def proxy_manager_for(proxy: str, **kwargs: Any) -> Any:
        kwargs.setdefault("ssl_context", ctx)
        manager = orig(proxy, **kwargs)
        _pin_proxy_disabled_svn(manager)
        return manager

    adapter.proxy_manager_for = proxy_manager_for


def _apply_patches(h2_patch: bool, h1_patch: bool) -> None:
    from ._niquests_patch import patch_http1_chrome_headers, patch_http2_chrome_frames

    if h2_patch:
        patch_http2_chrome_frames()
    if h1_patch:
        patch_http1_chrome_headers()


def _wrap(resp: Any) -> Response:
    content = resp.content if isinstance(resp.content, (bytes, bytearray)) else bytes(resp.content or b"")
    return Response(
        status_code=status_code_of(resp),
        content=content,
        headers=headers_to_dict(resp.headers),
        url=str(resp.url),
        cookies=cookies_to_dict(getattr(resp, "cookies", None)),
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


def _new_session(
    is_async: bool,
    impersonate: Optional[str],
    *,
    proxy: Optional[str],
    timeout: float,
    verify: bool,
    headers: Optional[dict],
    cookies: Optional[dict],
    extra: Optional[dict[str, Any]],
) -> Any:
    niquests, _utls, TLSConfiguration = _import_niquests()
    extra = dict(extra or {})
    _apply_patches(extra.pop("h2_patch", True), extra.pop("h1_patch", True))
    profile = resolve("niquests", impersonate)
    mapped = {
        "timeout": timeout,
        "verify": verify,
        "disable_http3": True,
        "pool_maxsize": 1,
        "tls_configuration": TLSConfiguration(backend="utls"),
        "headers": headers,
        "cookies": cookies,
    }
    mapped = {k: v for k, v in mapped.items() if v is not None}
    cls = niquests.AsyncSession if is_async else niquests.Session
    session = cls(**merge_extra(mapped, extra))
    if proxy:
        session.proxies = {"all": proxy}
    _attach_ssl_context(session, _make_ssl_context(profile, verify))
    return session


class NiquestsSync(SyncBackend):
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
        self._follow = allow_redirects
        self._session = _new_session(
            False,
            impersonate,
            proxy=proxy,
            timeout=timeout,
            verify=verify,
            headers=headers,
            cookies=cookies,
            extra=extra,
        )

    def request(self, method: str, url: str, **kwargs: Any) -> Response:
        req = _request_kwargs(kwargs)
        req.setdefault("allow_redirects", self._follow)
        return _wrap(self._session.request(method, url, **req))

    def close(self) -> None:
        self._session.close()

    def get_cookies(self) -> dict[str, str]:
        return cookies_to_dict(self._session.cookies)

    def set_cookies(self, cookies: dict[str, str], url: Optional[str] = None) -> None:
        self._session.cookies.update(cookies)

    @property
    def raw(self) -> Any:
        return self._session


class NiquestsAsync(AsyncBackend):
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
        self._follow = allow_redirects
        self._session = _new_session(
            True,
            impersonate,
            proxy=proxy,
            timeout=timeout,
            verify=verify,
            headers=headers,
            cookies=cookies,
            extra=extra,
        )

    async def request(self, method: str, url: str, **kwargs: Any) -> Response:
        req = _request_kwargs(kwargs)
        req.setdefault("allow_redirects", self._follow)
        resp = await self._session.request(method, url, **req)
        return _wrap(resp)

    async def aclose(self) -> None:
        await self._session.close()

    def get_cookies(self) -> dict[str, str]:
        return cookies_to_dict(self._session.cookies)

    def set_cookies(self, cookies: dict[str, str], url: Optional[str] = None) -> None:
        self._session.cookies.update(cookies)

    @property
    def raw(self) -> Any:
        return self._session
