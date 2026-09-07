from __future__ import annotations

from .errors import UnknownFingerprint


def normalize(name: str) -> str:
    s = name.strip().lower()
    for ch in ("_", "-", " ", ":"):
        s = s.replace(ch, "")
    return s


def _keys(mapping: dict[str, str]) -> dict[str, str]:
    return {normalize(key): value for key, value in mapping.items()}


# curl_cffi BrowserType + official aliases. Keys are matched after normalize().
CURL_CFFI = _keys({
    "chrome99": "chrome99",
    "chrome100": "chrome100",
    "chrome101": "chrome101",
    "chrome104": "chrome104",
    "chrome107": "chrome107",
    "chrome110": "chrome110",
    "chrome116": "chrome116",
    "chrome119": "chrome119",
    "chrome120": "chrome120",
    "chrome123": "chrome123",
    "chrome124": "chrome124",
    "chrome131": "chrome131",
    "chrome133a": "chrome133a",
    "chrome136": "chrome136",
    "chrome142": "chrome142",
    "chrome145": "chrome145",
    "chrome146": "chrome146",
    "chrome150": "chrome150",
    "chrome99_android": "chrome99_android",
    "chrome131_android": "chrome131_android",
    "chrome_android": "chrome131_android",
    "chromeandroid": "chrome131_android",
    "edge99": "edge99",
    "edge101": "edge101",
    "edge": "edge101",
    "safari153": "safari153",
    "safari155": "safari155",
    "safari170": "safari170",
    "safari172_ios": "safari172_ios",
    "safari180": "safari180",
    "safari180_ios": "safari180_ios",
    "safari184": "safari184",
    "safari184_ios": "safari184_ios",
    "safari260": "safari260",
    "safari2601": "safari2601",
    "safari260_ios": "safari260_ios",
    "safari": "safari2601",
    "safari_ios": "safari260_ios",
    "safari_beta": "safari2601",
    "safari_ios_beta": "safari260_ios",
    "safari15_3": "safari15_3",
    "safari15_5": "safari15_5",
    "safari17_0": "safari17_0",
    "safari17_2_ios": "safari17_2_ios",
    "safari18_0": "safari18_0",
    "safari18_0_ios": "safari18_0_ios",
    "safari18_4": "safari18_4",
    "safari18_4_ios": "safari18_4_ios",
    "firefox133": "firefox133",
    "firefox135": "firefox135",
    "firefox144": "firefox144",
    "firefox147": "firefox147",
    "firefox": "firefox147",
    "tor145": "tor145",
    "tor": "tor145",
    "chrome": "chrome150",
    "chromestable": "chrome150",
})

WREQ = _keys({
    **{f"chrome{n}": f"Chrome{n}" for n in range(100, 150)},
    "chrome": "Chrome149",
    "chromestable": "Chrome149",
    "edge": "Edge148",
    "firefox": "Firefox151",
    "safari": "Safari26_4",
    "opera": "Opera131",
    "okhttp": "OkHttp5",
})

# niquests / httpx。chrome152 需要 PyPI xutls>=2026.9.7。
UTLS = _keys({
    "chrome131": "chrome:131",
    "chrome142": "chrome:142",
    "chrome146": "chrome:146",
    "chrome148": "chrome:148",
    "chrome150": "chrome:150",
    "chrome152": "chrome:152",
    "chromestable": "chrome:stable",
    "chrome": "chrome:stable",
})

TABLES = {
    "curl_cffi": CURL_CFFI,
    "wreq": WREQ,
    "niquests": UTLS,
    "httpx": UTLS,
}

DEFAULTS = {
    "curl_cffi": "chrome150",
    "wreq": "Chrome149",
    "niquests": "chrome:152",
    "httpx": "chrome:152",
}


def _wreq_native(key: str) -> str | None:
    try:
        import wreq
    except ImportError:
        return None
    for name in dir(wreq.Emulation):
        if name.startswith("_"):
            continue
        if normalize(name) == key:
            return name
    return None


def resolve(backend: str, impersonate: str | None) -> str:
    table = TABLES[backend]
    if impersonate is None:
        return DEFAULTS[backend]
    key = normalize(impersonate)
    if key in table:
        return table[key]
    native = {normalize(value): value for value in table.values()}
    if key in native:
        return native[key]
    if backend == "wreq":
        found = _wreq_native(key)
        if found is not None:
            return found
    available = sorted(set(table.values()))
    raise UnknownFingerprint(
        f"{backend} 没有指纹 {impersonate!r}。可用: {available}"
    )
