from __future__ import annotations

from .errors import UnknownFingerprint


def normalize(name: str) -> str:
    s = name.strip().lower()
    for ch in ("_", "-", " ", ":"):
        s = s.replace(ch, "")
    return s


def _keys(mapping: dict[str, str]) -> dict[str, str]:
    return {normalize(key): value for key, value in mapping.items()}


# curl_cffi BrowserTypeLiteral，加上 tlsreq 自己的别名。键是用户会写的写法。
_CURL_PAIRS: tuple[tuple[str, str], ...] = (
    ("chrome99", "chrome99"),
    ("chrome100", "chrome100"),
    ("chrome101", "chrome101"),
    ("chrome104", "chrome104"),
    ("chrome107", "chrome107"),
    ("chrome110", "chrome110"),
    ("chrome116", "chrome116"),
    ("chrome119", "chrome119"),
    ("chrome120", "chrome120"),
    ("chrome123", "chrome123"),
    ("chrome124", "chrome124"),
    ("chrome131", "chrome131"),
    ("chrome133a", "chrome133a"),
    ("chrome136", "chrome136"),
    ("chrome142", "chrome142"),
    ("chrome145", "chrome145"),
    ("chrome146", "chrome146"),
    ("chrome150", "chrome150"),
    ("chrome99_android", "chrome99_android"),
    ("chrome131_android", "chrome131_android"),
    ("chrome_android", "chrome131_android"),
    ("chromeandroid", "chrome131_android"),
    ("edge99", "edge99"),
    ("edge101", "edge101"),
    ("edge", "edge101"),
    ("safari153", "safari153"),
    ("safari155", "safari155"),
    ("safari170", "safari170"),
    ("safari172_ios", "safari172_ios"),
    ("safari180", "safari180"),
    ("safari180_ios", "safari180_ios"),
    ("safari184", "safari184"),
    ("safari184_ios", "safari184_ios"),
    ("safari260", "safari260"),
    ("safari2601", "safari2601"),
    ("safari260_ios", "safari260_ios"),
    ("safari", "safari2601"),
    ("safari_ios", "safari260_ios"),
    ("safari_beta", "safari2601"),
    ("safari_ios_beta", "safari260_ios"),
    ("safari15_3", "safari15_3"),
    ("safari15_5", "safari15_5"),
    ("safari17_0", "safari17_0"),
    ("safari17_2_ios", "safari17_2_ios"),
    ("safari18_0", "safari18_0"),
    ("safari18_0_ios", "safari18_0_ios"),
    ("safari18_4", "safari18_4"),
    ("safari18_4_ios", "safari18_4_ios"),
    ("firefox133", "firefox133"),
    ("firefox135", "firefox135"),
    ("firefox144", "firefox144"),
    ("firefox147", "firefox147"),
    ("firefox", "firefox147"),
    ("tor145", "tor145"),
    ("tor", "tor145"),
    ("chrome", "chrome150"),
    ("chromestable", "chrome150"),
)

CURL_PUBLIC: tuple[str, ...] = tuple(key for key, _ in _CURL_PAIRS)
CURL_CFFI = _keys(dict(_CURL_PAIRS))

# wreq 0.13.0 的 Profile / Emulation 成员。不是连续版本号。
WREQ_PROFILES: tuple[str, ...] = (
    "Chrome100",
    "Chrome101",
    "Chrome104",
    "Chrome105",
    "Chrome106",
    "Chrome107",
    "Chrome108",
    "Chrome109",
    "Chrome110",
    "Chrome114",
    "Chrome116",
    "Chrome117",
    "Chrome118",
    "Chrome119",
    "Chrome120",
    "Chrome123",
    "Chrome124",
    "Chrome126",
    "Chrome127",
    "Chrome128",
    "Chrome129",
    "Chrome130",
    "Chrome131",
    "Chrome132",
    "Chrome133",
    "Chrome134",
    "Chrome135",
    "Chrome136",
    "Chrome137",
    "Chrome138",
    "Chrome139",
    "Chrome140",
    "Chrome141",
    "Chrome142",
    "Chrome143",
    "Chrome144",
    "Chrome145",
    "Chrome146",
    "Chrome147",
    "Chrome148",
    "Chrome149",
    "Chrome150",
    "Chrome151",
    "Chrome152",
    "Chrome153",
    "Chrome154",
    "Edge101",
    "Edge122",
    "Edge127",
    "Edge131",
    "Edge134",
    "Edge135",
    "Edge136",
    "Edge137",
    "Edge138",
    "Edge139",
    "Edge140",
    "Edge141",
    "Edge142",
    "Edge143",
    "Edge144",
    "Edge145",
    "Edge146",
    "Edge147",
    "Edge148",
    "Firefox109",
    "Firefox117",
    "Firefox128",
    "Firefox133",
    "Firefox135",
    "FirefoxPrivate135",
    "FirefoxAndroid135",
    "Firefox136",
    "FirefoxPrivate136",
    "Firefox139",
    "Firefox142",
    "Firefox143",
    "Firefox144",
    "Firefox145",
    "Firefox146",
    "Firefox147",
    "Firefox148",
    "Firefox149",
    "Firefox150",
    "Firefox151",
    "Firefox152",
    "SafariIos17_2",
    "SafariIos17_4_1",
    "SafariIos16_5",
    "Safari15_3",
    "Safari15_5",
    "Safari15_6_1",
    "Safari16",
    "Safari16_5",
    "Safari17_0",
    "Safari17_2_1",
    "Safari17_4_1",
    "Safari17_5",
    "Safari17_6",
    "Safari18",
    "SafariIPad18",
    "Safari18_2",
    "Safari18_3",
    "Safari18_3_1",
    "SafariIos18_1_1",
    "Safari18_5",
    "Safari26",
    "Safari26_1",
    "Safari26_2",
    "Safari26_3",
    "Safari26_4",
    "SafariIos26",
    "SafariIos26_2",
    "SafariIPad26",
    "SafariIpad26_2",
    "OkHttp3_9",
    "OkHttp3_11",
    "OkHttp3_13",
    "OkHttp3_14",
    "OkHttp4_9",
    "OkHttp4_10",
    "OkHttp4_12",
    "OkHttp5",
    "Opera116",
    "Opera117",
    "Opera118",
    "Opera119",
    "Opera120",
    "Opera121",
    "Opera122",
    "Opera123",
    "Opera124",
    "Opera125",
    "Opera126",
    "Opera127",
    "Opera128",
    "Opera129",
    "Opera130",
    "Opera131",
)

# 家族别名指向该家族在 WREQ_PROFILES 里的最新成员。
WREQ_ALIASES: dict[str, str] = {
    "chrome": "Chrome154",
    "chromestable": "Chrome154",
    "edge": "Edge148",
    "firefox": "Firefox152",
    "safari": "Safari26_4",
    "opera": "Opera131",
    "okhttp": "OkHttp5",
}

WREQ_PUBLIC: tuple[str, ...] = tuple(name.lower() for name in WREQ_PROFILES) + tuple(WREQ_ALIASES)


def _wreq_table() -> dict[str, str]:
    table = {normalize(name): name for name in WREQ_PROFILES}
    for alias, target in WREQ_ALIASES.items():
        table[normalize(alias)] = target
    return table


WREQ = _wreq_table()

# niquests / httpx。名字来自 xutls presets()。chrome152 需要 xutls>=2026.9.7。
_UTLS_PAIRS: tuple[tuple[str, str], ...] = (
    ("chrome131", "chrome:131"),
    ("chrome142", "chrome:142"),
    ("chrome146", "chrome:146"),
    ("chrome148", "chrome:148"),
    ("chrome150", "chrome:150"),
    ("chrome152", "chrome:152"),
    ("chromestable", "chrome:stable"),
    ("chrome", "chrome:stable"),
)

UTLS_PUBLIC: tuple[str, ...] = tuple(key for key, _ in _UTLS_PAIRS)
UTLS = _keys(dict(_UTLS_PAIRS))

TABLES = {
    "curl_cffi": CURL_CFFI,
    "wreq": WREQ,
    "niquests": UTLS,
    "httpx": UTLS,
}

DEFAULTS = {
    "curl_cffi": "chrome150",
    "wreq": "Chrome154",
    "niquests": "chrome:152",
    "httpx": "chrome:152",
}


def _wreq_profile_names() -> list[str] | None:
    try:
        import wreq
    except ImportError:
        return None
    names = [
        name
        for name in dir(wreq.Emulation)
        if name[:1].isupper() and not name.startswith("_")
    ]
    return names or None


def _wreq_native(key: str) -> str | None:
    names = _wreq_profile_names()
    if not names:
        return None
    for name in names:
        if normalize(name) == key:
            return name
    return None


def _available(backend: str, table: dict[str, str]) -> list[str]:
    if backend == "wreq":
        live = _wreq_profile_names()
        if live:
            return sorted(set(live))
    return sorted(set(table.values()))


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
    available = _available(backend, table)
    raise UnknownFingerprint(
        f"{backend} 没有指纹 {impersonate!r}。可用: {available}"
    )
