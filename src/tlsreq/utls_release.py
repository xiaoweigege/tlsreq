"""Chrome 152 用 PyPI 上的 xutls（import 名仍是 utls）。不要装官方 utls。"""
from __future__ import annotations

from typing import Any

from .errors import UnknownFingerprint

XUTLS_DIST = "xutls"
UTLS_RELEASE = "2026.9.7"
UTLS_RELEASE_PAGE = "https://pypi.org/project/xutls/"

_INSTALL_HINT = (
    f"Chrome 152 需要 PyPI 包 {XUTLS_DIST}>={UTLS_RELEASE}（import 仍是 utls）。\n"
    f"不要装官方 utls，也不要和 xutls 装在同一个环境。\n"
    f"  pip install '{XUTLS_DIST}>={UTLS_RELEASE}'\n"
    f"见 {UTLS_RELEASE_PAGE}"
)


def fingerprint_from_preset(utls: Any, profile: str) -> Any:
    try:
        return utls.Fingerprint.from_preset(profile)
    except ValueError as exc:
        raise UnknownFingerprint(
            f"当前 utls 没有指纹 {profile!r}。\n{_INSTALL_HINT}\n原始错误: {exc}"
        ) from exc
