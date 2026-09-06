class TlsReqError(Exception):
    """tlsreq 公共异常。"""


class UnknownBackend(TlsReqError):
    """backend 名无法识别。"""


class BackendNotInstalled(TlsReqError):
    """对应 extra 未安装。"""


class UnknownFingerprint(TlsReqError):
    """当前 backend 没有这个 impersonate。"""
