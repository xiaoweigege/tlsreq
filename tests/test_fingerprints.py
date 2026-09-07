import unittest

from tlsreq.errors import UnknownFingerprint
from tlsreq.fingerprints import normalize, resolve


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
        self.assertEqual(resolve("wreq", "chrome149"), "Chrome149")
        self.assertEqual(resolve("wreq", "chrome120"), "Chrome120")
        self.assertEqual(resolve("wreq", "chrome"), "Chrome149")
        self.assertEqual(resolve("wreq", "firefox"), "Firefox151")
        self.assertEqual(resolve("wreq", "safari"), "Safari26_4")
        self.assertEqual(resolve("wreq", "edge148"), "Edge148")
        self.assertEqual(resolve("wreq", "OkHttp5"), "OkHttp5")
        self.assertEqual(resolve("curl_cffi", "chrome150"), "chrome150")
        self.assertEqual(resolve("curl_cffi", "safari"), "safari2601")
        self.assertEqual(resolve("curl_cffi", "firefox"), "firefox147")
        self.assertEqual(resolve("curl_cffi", "chrome_android"), "chrome131_android")

    def test_unknown_fingerprint(self):
        with self.assertRaises(UnknownFingerprint):
            resolve("httpx", "chrome149")


if __name__ == "__main__":
    unittest.main()
