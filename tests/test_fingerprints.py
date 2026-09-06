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
        self.assertEqual(resolve("curl_cffi", "chrome150"), "chrome150")

    def test_unknown_fingerprint(self):
        with self.assertRaises(UnknownFingerprint):
            resolve("httpx", "chrome149")


if __name__ == "__main__":
    unittest.main()
