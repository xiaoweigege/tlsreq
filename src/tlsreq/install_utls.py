"""安装 GitHub Release 上带 Chrome 152 的 utls wheel。"""
from __future__ import annotations

import subprocess
import sys

from .utls_release import UTLS_RELEASE, wheel_url


def main(argv: list[str] | None = None) -> int:
    url = wheel_url()
    cmd = [sys.executable, "-m", "pip", "install", "--force-reinstall", url]
    print("installing utls", UTLS_RELEASE)
    print(" ", " ".join(cmd))
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
