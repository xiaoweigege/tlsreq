"""非 PyPI 的 utls：Chrome 152 只在 GitHub Release 2026.9.4。"""
from __future__ import annotations

import platform
import sys
from typing import Any, Optional

from .errors import BackendNotInstalled, UnknownFingerprint

UTLS_RELEASE = "2026.9.4"
UTLS_RELEASE_PAGE = f"https://github.com/xiaoweigege/utls/releases/tag/{UTLS_RELEASE}"
UTLS_DOWNLOAD = f"https://github.com/xiaoweigege/utls/releases/download/{UTLS_RELEASE}"

_WHEELS = {
    "darwin": f"utls-{UTLS_RELEASE}-cp37-abi3-macosx_10_15_x86_64.macosx_11_0_arm64.macosx_10_15_universal2.whl",
    "linux-x86_64": f"utls-{UTLS_RELEASE}-cp37-abi3-manylinux_2_17_x86_64.manylinux2014_x86_64.whl",
    "linux-aarch64": f"utls-{UTLS_RELEASE}-cp37-abi3-manylinux_2_28_aarch64.whl",
    "linux-musl-x86_64": f"utls-{UTLS_RELEASE}-cp37-abi3-musllinux_1_1_x86_64.whl",
    "linux-musl-aarch64": f"utls-{UTLS_RELEASE}-cp37-abi3-musllinux_1_1_aarch64.whl",
    "win-amd64": f"utls-{UTLS_RELEASE}-cp37-abi3-win_amd64.whl",
    "win32": f"utls-{UTLS_RELEASE}-cp37-abi3-win32.whl",
    "win-arm64": f"utls-{UTLS_RELEASE}-cp37-abi3-win_arm64.whl",
}

_INSTALL_HINT = (
    f"PyPI 官方 utls 没有 Chrome 152。请安装 {UTLS_RELEASE_PAGE}：\n"
    "  python -m tlsreq.install_utls"
)


def _is_musl() -> bool:
    try:
        import sysconfig
        return "musl" in (sysconfig.get_config_var("HOST_GNU_TYPE") or "")
    except Exception:
        return False


def wheel_filename() -> str:
    system = sys.platform
    machine = platform.machine().lower()
    if system == "darwin":
        return _WHEELS["darwin"]
    if system.startswith("linux"):
        musl = _is_musl()
        arm = machine in {"aarch64", "arm64"}
        if musl and arm:
            return _WHEELS["linux-musl-aarch64"]
        if musl:
            return _WHEELS["linux-musl-x86_64"]
        if arm:
            return _WHEELS["linux-aarch64"]
        return _WHEELS["linux-x86_64"]
    if system == "win32":
        if machine in {"arm64", "aarch64"}:
            return _WHEELS["win-arm64"]
        if machine in {"x86", "i386", "i686"}:
            return _WHEELS["win32"]
        return _WHEELS["win-amd64"]
    raise BackendNotInstalled(
        f"没有为 {system}/{machine} 预编译的 utls {UTLS_RELEASE} wheel。见 {UTLS_RELEASE_PAGE}"
    )


def wheel_url() -> str:
    return f"{UTLS_DOWNLOAD}/{wheel_filename()}"


def _version_tuple(version: str) -> tuple[int, ...]:
    parts = []
    for item in version.split("."):
        digits = "".join(ch for ch in item if ch.isdigit())
        parts.append(int(digits) if digits else 0)
    return tuple(parts)


def utls_version() -> str:
    try:
        from importlib.metadata import version
        return version("utls")
    except Exception:
        import utls
        return str(getattr(utls, "__version__", "0"))


def fingerprint_from_preset(utls: Any, profile: str) -> Any:
    version = utls_version()
    if _version_tuple(version) < _version_tuple(UTLS_RELEASE):
        raise BackendNotInstalled(
            f"当前 utls {version} 太旧，Chrome 152 需要 {UTLS_RELEASE}。"
            f"不要用 PyPI 的 utls。\n{_INSTALL_HINT}"
        )
    try:
        return utls.Fingerprint.from_preset(profile)
    except ValueError as exc:
        raise UnknownFingerprint(
            f"当前 utls {version} 没有指纹 {profile!r}。\n{_INSTALL_HINT}\n原始错误: {exc}"
        ) from exc
