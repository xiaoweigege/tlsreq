from typing import Generic, Literal, TypeVar, Union

_Imp = TypeVar("_Imp")

BackendName = Literal[
    "httpx",
    "niquests",
    "wreq",
    "curl_cffi",
    "curl",
    "cffi",
    "nirequest",
    "nirequests",
    "nio",
]

WreqImpersonate = Literal[
    "chrome100",
    "chrome101",
    "chrome104",
    "chrome105",
    "chrome106",
    "chrome107",
    "chrome108",
    "chrome109",
    "chrome110",
    "chrome114",
    "chrome116",
    "chrome117",
    "chrome118",
    "chrome119",
    "chrome120",
    "chrome123",
    "chrome124",
    "chrome126",
    "chrome127",
    "chrome128",
    "chrome129",
    "chrome130",
    "chrome131",
    "chrome132",
    "chrome133",
    "chrome134",
    "chrome135",
    "chrome136",
    "chrome137",
    "chrome138",
    "chrome139",
    "chrome140",
    "chrome141",
    "chrome142",
    "chrome143",
    "chrome144",
    "chrome145",
    "chrome146",
    "chrome147",
    "chrome148",
    "chrome149",
    "chrome150",
    "chrome151",
    "chrome152",
    "chrome153",
    "chrome154",
    "edge101",
    "edge122",
    "edge127",
    "edge131",
    "edge134",
    "edge135",
    "edge136",
    "edge137",
    "edge138",
    "edge139",
    "edge140",
    "edge141",
    "edge142",
    "edge143",
    "edge144",
    "edge145",
    "edge146",
    "edge147",
    "edge148",
    "firefox109",
    "firefox117",
    "firefox128",
    "firefox133",
    "firefox135",
    "firefoxprivate135",
    "firefoxandroid135",
    "firefox136",
    "firefoxprivate136",
    "firefox139",
    "firefox142",
    "firefox143",
    "firefox144",
    "firefox145",
    "firefox146",
    "firefox147",
    "firefox148",
    "firefox149",
    "firefox150",
    "firefox151",
    "firefox152",
    "safariios17_2",
    "safariios17_4_1",
    "safariios16_5",
    "safari15_3",
    "safari15_5",
    "safari15_6_1",
    "safari16",
    "safari16_5",
    "safari17_0",
    "safari17_2_1",
    "safari17_4_1",
    "safari17_5",
    "safari17_6",
    "safari18",
    "safariipad18",
    "safari18_2",
    "safari18_3",
    "safari18_3_1",
    "safariios18_1_1",
    "safari18_5",
    "safari26",
    "safari26_1",
    "safari26_2",
    "safari26_3",
    "safari26_4",
    "safariios26",
    "safariios26_2",
    "safariipad26",
    "safariipad26_2",
    "okhttp3_9",
    "okhttp3_11",
    "okhttp3_13",
    "okhttp3_14",
    "okhttp4_9",
    "okhttp4_10",
    "okhttp4_12",
    "okhttp5",
    "opera116",
    "opera117",
    "opera118",
    "opera119",
    "opera120",
    "opera121",
    "opera122",
    "opera123",
    "opera124",
    "opera125",
    "opera126",
    "opera127",
    "opera128",
    "opera129",
    "opera130",
    "opera131",
    "chrome",
    "chromestable",
    "edge",
    "firefox",
    "safari",
    "opera",
    "okhttp",
]

CurlCffiImpersonate = Literal[
    "chrome99",
    "chrome100",
    "chrome101",
    "chrome104",
    "chrome107",
    "chrome110",
    "chrome116",
    "chrome119",
    "chrome120",
    "chrome123",
    "chrome124",
    "chrome131",
    "chrome133a",
    "chrome136",
    "chrome142",
    "chrome145",
    "chrome146",
    "chrome150",
    "chrome99_android",
    "chrome131_android",
    "chrome_android",
    "chromeandroid",
    "edge99",
    "edge101",
    "edge",
    "safari153",
    "safari155",
    "safari170",
    "safari172_ios",
    "safari180",
    "safari180_ios",
    "safari184",
    "safari184_ios",
    "safari260",
    "safari2601",
    "safari260_ios",
    "safari",
    "safari_ios",
    "safari_beta",
    "safari_ios_beta",
    "safari15_3",
    "safari15_5",
    "safari17_0",
    "safari17_2_ios",
    "safari18_0",
    "safari18_0_ios",
    "safari18_4",
    "safari18_4_ios",
    "firefox133",
    "firefox135",
    "firefox144",
    "firefox147",
    "firefox",
    "tor145",
    "tor",
    "chrome",
    "chromestable",
]

UtlsImpersonate = Literal[
    "chrome131",
    "chrome142",
    "chrome146",
    "chrome148",
    "chrome150",
    "chrome152",
    "chromestable",
    "chrome",
]

ImpersonateName = Union[WreqImpersonate, CurlCffiImpersonate, UtlsImpersonate]


class Backend(Generic[_Imp]):
    __slots__ = ("name",)

    def __init__(self, name: str) -> None:
        self.name = name

    def __repr__(self) -> str:
        return f"Backend({self.name!r})"


class Wreq(Backend[WreqImpersonate]):
    __slots__ = ()
    chrome100: Literal["chrome100"] = "chrome100"
    chrome101: Literal["chrome101"] = "chrome101"
    chrome104: Literal["chrome104"] = "chrome104"
    chrome105: Literal["chrome105"] = "chrome105"
    chrome106: Literal["chrome106"] = "chrome106"
    chrome107: Literal["chrome107"] = "chrome107"
    chrome108: Literal["chrome108"] = "chrome108"
    chrome109: Literal["chrome109"] = "chrome109"
    chrome110: Literal["chrome110"] = "chrome110"
    chrome114: Literal["chrome114"] = "chrome114"
    chrome116: Literal["chrome116"] = "chrome116"
    chrome117: Literal["chrome117"] = "chrome117"
    chrome118: Literal["chrome118"] = "chrome118"
    chrome119: Literal["chrome119"] = "chrome119"
    chrome120: Literal["chrome120"] = "chrome120"
    chrome123: Literal["chrome123"] = "chrome123"
    chrome124: Literal["chrome124"] = "chrome124"
    chrome126: Literal["chrome126"] = "chrome126"
    chrome127: Literal["chrome127"] = "chrome127"
    chrome128: Literal["chrome128"] = "chrome128"
    chrome129: Literal["chrome129"] = "chrome129"
    chrome130: Literal["chrome130"] = "chrome130"
    chrome131: Literal["chrome131"] = "chrome131"
    chrome132: Literal["chrome132"] = "chrome132"
    chrome133: Literal["chrome133"] = "chrome133"
    chrome134: Literal["chrome134"] = "chrome134"
    chrome135: Literal["chrome135"] = "chrome135"
    chrome136: Literal["chrome136"] = "chrome136"
    chrome137: Literal["chrome137"] = "chrome137"
    chrome138: Literal["chrome138"] = "chrome138"
    chrome139: Literal["chrome139"] = "chrome139"
    chrome140: Literal["chrome140"] = "chrome140"
    chrome141: Literal["chrome141"] = "chrome141"
    chrome142: Literal["chrome142"] = "chrome142"
    chrome143: Literal["chrome143"] = "chrome143"
    chrome144: Literal["chrome144"] = "chrome144"
    chrome145: Literal["chrome145"] = "chrome145"
    chrome146: Literal["chrome146"] = "chrome146"
    chrome147: Literal["chrome147"] = "chrome147"
    chrome148: Literal["chrome148"] = "chrome148"
    chrome149: Literal["chrome149"] = "chrome149"
    chrome150: Literal["chrome150"] = "chrome150"
    chrome151: Literal["chrome151"] = "chrome151"
    chrome152: Literal["chrome152"] = "chrome152"
    chrome153: Literal["chrome153"] = "chrome153"
    chrome154: Literal["chrome154"] = "chrome154"
    edge101: Literal["edge101"] = "edge101"
    edge122: Literal["edge122"] = "edge122"
    edge127: Literal["edge127"] = "edge127"
    edge131: Literal["edge131"] = "edge131"
    edge134: Literal["edge134"] = "edge134"
    edge135: Literal["edge135"] = "edge135"
    edge136: Literal["edge136"] = "edge136"
    edge137: Literal["edge137"] = "edge137"
    edge138: Literal["edge138"] = "edge138"
    edge139: Literal["edge139"] = "edge139"
    edge140: Literal["edge140"] = "edge140"
    edge141: Literal["edge141"] = "edge141"
    edge142: Literal["edge142"] = "edge142"
    edge143: Literal["edge143"] = "edge143"
    edge144: Literal["edge144"] = "edge144"
    edge145: Literal["edge145"] = "edge145"
    edge146: Literal["edge146"] = "edge146"
    edge147: Literal["edge147"] = "edge147"
    edge148: Literal["edge148"] = "edge148"
    firefox109: Literal["firefox109"] = "firefox109"
    firefox117: Literal["firefox117"] = "firefox117"
    firefox128: Literal["firefox128"] = "firefox128"
    firefox133: Literal["firefox133"] = "firefox133"
    firefox135: Literal["firefox135"] = "firefox135"
    firefoxprivate135: Literal["firefoxprivate135"] = "firefoxprivate135"
    firefoxandroid135: Literal["firefoxandroid135"] = "firefoxandroid135"
    firefox136: Literal["firefox136"] = "firefox136"
    firefoxprivate136: Literal["firefoxprivate136"] = "firefoxprivate136"
    firefox139: Literal["firefox139"] = "firefox139"
    firefox142: Literal["firefox142"] = "firefox142"
    firefox143: Literal["firefox143"] = "firefox143"
    firefox144: Literal["firefox144"] = "firefox144"
    firefox145: Literal["firefox145"] = "firefox145"
    firefox146: Literal["firefox146"] = "firefox146"
    firefox147: Literal["firefox147"] = "firefox147"
    firefox148: Literal["firefox148"] = "firefox148"
    firefox149: Literal["firefox149"] = "firefox149"
    firefox150: Literal["firefox150"] = "firefox150"
    firefox151: Literal["firefox151"] = "firefox151"
    firefox152: Literal["firefox152"] = "firefox152"
    safariios17_2: Literal["safariios17_2"] = "safariios17_2"
    safariios17_4_1: Literal["safariios17_4_1"] = "safariios17_4_1"
    safariios16_5: Literal["safariios16_5"] = "safariios16_5"
    safari15_3: Literal["safari15_3"] = "safari15_3"
    safari15_5: Literal["safari15_5"] = "safari15_5"
    safari15_6_1: Literal["safari15_6_1"] = "safari15_6_1"
    safari16: Literal["safari16"] = "safari16"
    safari16_5: Literal["safari16_5"] = "safari16_5"
    safari17_0: Literal["safari17_0"] = "safari17_0"
    safari17_2_1: Literal["safari17_2_1"] = "safari17_2_1"
    safari17_4_1: Literal["safari17_4_1"] = "safari17_4_1"
    safari17_5: Literal["safari17_5"] = "safari17_5"
    safari17_6: Literal["safari17_6"] = "safari17_6"
    safari18: Literal["safari18"] = "safari18"
    safariipad18: Literal["safariipad18"] = "safariipad18"
    safari18_2: Literal["safari18_2"] = "safari18_2"
    safari18_3: Literal["safari18_3"] = "safari18_3"
    safari18_3_1: Literal["safari18_3_1"] = "safari18_3_1"
    safariios18_1_1: Literal["safariios18_1_1"] = "safariios18_1_1"
    safari18_5: Literal["safari18_5"] = "safari18_5"
    safari26: Literal["safari26"] = "safari26"
    safari26_1: Literal["safari26_1"] = "safari26_1"
    safari26_2: Literal["safari26_2"] = "safari26_2"
    safari26_3: Literal["safari26_3"] = "safari26_3"
    safari26_4: Literal["safari26_4"] = "safari26_4"
    safariios26: Literal["safariios26"] = "safariios26"
    safariios26_2: Literal["safariios26_2"] = "safariios26_2"
    safariipad26: Literal["safariipad26"] = "safariipad26"
    safariipad26_2: Literal["safariipad26_2"] = "safariipad26_2"
    okhttp3_9: Literal["okhttp3_9"] = "okhttp3_9"
    okhttp3_11: Literal["okhttp3_11"] = "okhttp3_11"
    okhttp3_13: Literal["okhttp3_13"] = "okhttp3_13"
    okhttp3_14: Literal["okhttp3_14"] = "okhttp3_14"
    okhttp4_9: Literal["okhttp4_9"] = "okhttp4_9"
    okhttp4_10: Literal["okhttp4_10"] = "okhttp4_10"
    okhttp4_12: Literal["okhttp4_12"] = "okhttp4_12"
    okhttp5: Literal["okhttp5"] = "okhttp5"
    opera116: Literal["opera116"] = "opera116"
    opera117: Literal["opera117"] = "opera117"
    opera118: Literal["opera118"] = "opera118"
    opera119: Literal["opera119"] = "opera119"
    opera120: Literal["opera120"] = "opera120"
    opera121: Literal["opera121"] = "opera121"
    opera122: Literal["opera122"] = "opera122"
    opera123: Literal["opera123"] = "opera123"
    opera124: Literal["opera124"] = "opera124"
    opera125: Literal["opera125"] = "opera125"
    opera126: Literal["opera126"] = "opera126"
    opera127: Literal["opera127"] = "opera127"
    opera128: Literal["opera128"] = "opera128"
    opera129: Literal["opera129"] = "opera129"
    opera130: Literal["opera130"] = "opera130"
    opera131: Literal["opera131"] = "opera131"
    chrome: Literal["chrome"] = "chrome"
    chromestable: Literal["chromestable"] = "chromestable"
    edge: Literal["edge"] = "edge"
    firefox: Literal["firefox"] = "firefox"
    safari: Literal["safari"] = "safari"
    opera: Literal["opera"] = "opera"
    okhttp: Literal["okhttp"] = "okhttp"


class CurlCffi(Backend[CurlCffiImpersonate]):
    __slots__ = ()
    chrome99: Literal["chrome99"] = "chrome99"
    chrome100: Literal["chrome100"] = "chrome100"
    chrome101: Literal["chrome101"] = "chrome101"
    chrome104: Literal["chrome104"] = "chrome104"
    chrome107: Literal["chrome107"] = "chrome107"
    chrome110: Literal["chrome110"] = "chrome110"
    chrome116: Literal["chrome116"] = "chrome116"
    chrome119: Literal["chrome119"] = "chrome119"
    chrome120: Literal["chrome120"] = "chrome120"
    chrome123: Literal["chrome123"] = "chrome123"
    chrome124: Literal["chrome124"] = "chrome124"
    chrome131: Literal["chrome131"] = "chrome131"
    chrome133a: Literal["chrome133a"] = "chrome133a"
    chrome136: Literal["chrome136"] = "chrome136"
    chrome142: Literal["chrome142"] = "chrome142"
    chrome145: Literal["chrome145"] = "chrome145"
    chrome146: Literal["chrome146"] = "chrome146"
    chrome150: Literal["chrome150"] = "chrome150"
    chrome99_android: Literal["chrome99_android"] = "chrome99_android"
    chrome131_android: Literal["chrome131_android"] = "chrome131_android"
    chrome_android: Literal["chrome_android"] = "chrome_android"
    chromeandroid: Literal["chromeandroid"] = "chromeandroid"
    edge99: Literal["edge99"] = "edge99"
    edge101: Literal["edge101"] = "edge101"
    edge: Literal["edge"] = "edge"
    safari153: Literal["safari153"] = "safari153"
    safari155: Literal["safari155"] = "safari155"
    safari170: Literal["safari170"] = "safari170"
    safari172_ios: Literal["safari172_ios"] = "safari172_ios"
    safari180: Literal["safari180"] = "safari180"
    safari180_ios: Literal["safari180_ios"] = "safari180_ios"
    safari184: Literal["safari184"] = "safari184"
    safari184_ios: Literal["safari184_ios"] = "safari184_ios"
    safari260: Literal["safari260"] = "safari260"
    safari2601: Literal["safari2601"] = "safari2601"
    safari260_ios: Literal["safari260_ios"] = "safari260_ios"
    safari: Literal["safari"] = "safari"
    safari_ios: Literal["safari_ios"] = "safari_ios"
    safari_beta: Literal["safari_beta"] = "safari_beta"
    safari_ios_beta: Literal["safari_ios_beta"] = "safari_ios_beta"
    safari15_3: Literal["safari15_3"] = "safari15_3"
    safari15_5: Literal["safari15_5"] = "safari15_5"
    safari17_0: Literal["safari17_0"] = "safari17_0"
    safari17_2_ios: Literal["safari17_2_ios"] = "safari17_2_ios"
    safari18_0: Literal["safari18_0"] = "safari18_0"
    safari18_0_ios: Literal["safari18_0_ios"] = "safari18_0_ios"
    safari18_4: Literal["safari18_4"] = "safari18_4"
    safari18_4_ios: Literal["safari18_4_ios"] = "safari18_4_ios"
    firefox133: Literal["firefox133"] = "firefox133"
    firefox135: Literal["firefox135"] = "firefox135"
    firefox144: Literal["firefox144"] = "firefox144"
    firefox147: Literal["firefox147"] = "firefox147"
    firefox: Literal["firefox"] = "firefox"
    tor145: Literal["tor145"] = "tor145"
    tor: Literal["tor"] = "tor"
    chrome: Literal["chrome"] = "chrome"
    chromestable: Literal["chromestable"] = "chromestable"


class Utls(Backend[UtlsImpersonate]):
    __slots__ = ()
    chrome131: Literal["chrome131"] = "chrome131"
    chrome142: Literal["chrome142"] = "chrome142"
    chrome146: Literal["chrome146"] = "chrome146"
    chrome148: Literal["chrome148"] = "chrome148"
    chrome150: Literal["chrome150"] = "chrome150"
    chrome152: Literal["chrome152"] = "chrome152"
    chromestable: Literal["chromestable"] = "chromestable"
    chrome: Literal["chrome"] = "chrome"


wreq = Wreq("wreq")
curl_cffi = CurlCffi("curl_cffi")
curl = CurlCffi("curl")
cffi = CurlCffi("cffi")
httpx = Utls("httpx")
niquests = Utls("niquests")
nirequest = Utls("nirequest")
nirequests = Utls("nirequests")
nio = Utls("nio")
