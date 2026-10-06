import unittest
from typing import get_args

from tlsreq.errors import UnknownFingerprint
from tlsreq.fingerprints import (
    CURL_PUBLIC,
    UTLS_PUBLIC,
    WREQ_PUBLIC,
    normalize,
    resolve,
)
from tlsreq.types import CurlCffiImpersonate, UtlsImpersonate, WreqImpersonate


class FingerprintTests(unittest.TestCase):
    def test_normalize(self):
        self.assertEqual(normalize("Chrome:152"), "chrome152")
        self.assertEqual(normalize("chrome_150"), "chrome150")
        self.assertEqual(normalize("chrome-stable"), "chromestable")

    def test_resolve_utls(self):
        self.assertEqual(resolve("httpx", "chrome152"), "chrome:152")
        self.assertEqual(resolve("niquests", "chrome:stable"), "chrome:stable")
        self.assertEqual(resolve("httpx", None), "chrome:152")

    def test_resolve_wreq_and_curl(self):
        self.assertEqual(resolve("wreq", None), "Chrome154")
        self.assertEqual(resolve("wreq", "chrome154"), "Chrome154")
        self.assertEqual(resolve("wreq", "Chrome154"), "Chrome154")
        self.assertEqual(resolve("wreq", "chrome152"), "Chrome152")
        self.assertEqual(resolve("wreq", "chrome149"), "Chrome149")
        self.assertEqual(resolve("wreq", "chrome120"), "Chrome120")
        self.assertEqual(resolve("wreq", "chrome"), "Chrome154")
        self.assertEqual(resolve("wreq", "chromestable"), "Chrome154")
        self.assertEqual(resolve("wreq", "firefox"), "Firefox152")
        self.assertEqual(resolve("wreq", "firefox152"), "Firefox152")
        self.assertEqual(resolve("wreq", "safari"), "Safari26_4")
        self.assertEqual(resolve("wreq", "safari26_4"), "Safari26_4")
        self.assertEqual(resolve("wreq", "edge148"), "Edge148")
        self.assertEqual(resolve("wreq", "OkHttp5"), "OkHttp5")
        self.assertEqual(resolve("curl_cffi", "chrome150"), "chrome150")
        self.assertEqual(resolve("curl_cffi", "safari"), "safari2601")
        self.assertEqual(resolve("curl_cffi", "firefox"), "firefox147")
        self.assertEqual(resolve("curl_cffi", "chrome_android"), "chrome131_android")

    def test_wreq_gap_versions_are_absent(self):
        with self.assertRaises(UnknownFingerprint):
            resolve("wreq", "chrome102")
        with self.assertRaises(UnknownFingerprint):
            resolve("wreq", "chrome125")

    def test_impersonate_literals_match_libraries(self):
        self.assertEqual(set(get_args(WreqImpersonate)), set(WREQ_PUBLIC))
        self.assertEqual(set(get_args(CurlCffiImpersonate)), set(CURL_PUBLIC))
        self.assertEqual(set(get_args(UtlsImpersonate)), set(UTLS_PUBLIC))
        for name in get_args(WreqImpersonate):
            resolve("wreq", name)
        for name in get_args(CurlCffiImpersonate):
            resolve("curl_cffi", name)
        for name in get_args(UtlsImpersonate):
            resolve("httpx", name)

    def test_unknown_fingerprint(self):
        with self.assertRaises(UnknownFingerprint):
            resolve("httpx", "chrome149")


if __name__ == "__main__":
    unittest.main()
