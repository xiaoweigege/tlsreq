"""安装 PyPI 上带 Chrome 152 的 xutls（import 名仍是 utls）。"""
from __future__ import annotations

import subprocess
import sys

from .utls_release import UTLS_RELEASE, XUTLS_DIST


def main(argv: list[str] | None = None) -> int:
    spec = f"{XUTLS_DIST}>={UTLS_RELEASE}"
    cmd = [sys.executable, "-m", "pip", "install", "--upgrade", spec]
    print("installing", spec)
    print(" ", " ".join(cmd))
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
