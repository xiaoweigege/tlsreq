"""Chrome 152 用 PyPI 上的 xutls（import 名仍是 utls）。不要装官方 utls。"""
from __future__ import annotations

from typing import Any

from .errors import BackendNotInstalled, UnknownFingerprint

XUTLS_DIST = "xutls"
UTLS_RELEASE = "2026.9.7"
UTLS_RELEASE_PAGE = "https://pypi.org/project/xutls/"

_INSTALL_HINT = (
    f"Chrome 152 需要 PyPI 包 {XUTLS_DIST}>={UTLS_RELEASE}（import 仍是 utls）。\n"
    f"不要装官方 utls，也不要和 xutls 装在同一个环境。\n"
    f"  pip install '{XUTLS_DIST}>={UTLS_RELEASE}'\n"
    f"或: python -m tlsreq.install_utls\n"
    f"见 {UTLS_RELEASE_PAGE}"
)


def _version_tuple(version: str) -> tuple[int, ...]:
    parts = []
    for item in version.split("."):
        digits = "".join(ch for ch in item if ch.isdigit())
        parts.append(int(digits) if digits else 0)
    return tuple(parts)


def utls_version() -> str:
    from importlib.metadata import PackageNotFoundError, version

    for name in (XUTLS_DIST, "utls"):
        try:
            return version(name)
        except PackageNotFoundError:
            continue
    import utls

    return str(getattr(utls, "__version__", "0"))


def fingerprint_from_preset(utls: Any, profile: str) -> Any:
    version = utls_version()
    if _version_tuple(version) < _version_tuple(UTLS_RELEASE):
        raise BackendNotInstalled(
            f"当前 TLS 库 {version} 太旧，Chrome 152 需要 {XUTLS_DIST}>={UTLS_RELEASE}。"
            f"\n{_INSTALL_HINT}"
        )
    try:
        return utls.Fingerprint.from_preset(profile)
    except ValueError as exc:
        raise UnknownFingerprint(
            f"当前 {XUTLS_DIST}/{version} 没有指纹 {profile!r}。\n{_INSTALL_HINT}\n原始错误: {exc}"
        ) from exc
