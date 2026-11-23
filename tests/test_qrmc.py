"""Tests for the experimental QRMC sketch and the optional AES-GCM wrapper."""

import importlib
import unittest

from qrmc import ExperimentalCipher, ExperimentalThreshold, combine_shares, split_secret


class TestExperimentalRoundTrip(unittest.TestCase):
    def test_empty_and_varied_lengths(self):
        box = ExperimentalCipher()
        for msg in (b"", b"a", b"hello", b"x" * 1024, bytes(range(256))):
            self.assertEqual(box.decrypt(box.encrypt(msg)), msg)

    def test_different_sessions_differ(self):
        box = ExperimentalCipher()
        msg = b"same message"
        self.assertNotEqual(box.encrypt(msg), box.encrypt(msg))

    def test_wrong_key_fails(self):
        a = ExperimentalCipher()
        b = ExperimentalCipher()
        ct = a.encrypt(b"secret")
        with self.assertRaises(ValueError):
            b.decrypt(ct)

    def test_tamper_fails(self):
        box = ExperimentalCipher()
        ct = bytearray(box.encrypt(b"secret"))
        ct[-1] ^= 0x01
        with self.assertRaises(ValueError):
            box.decrypt(bytes(ct))

    def test_rejects_short_or_bad_magic(self):
        box = ExperimentalCipher()
        with self.assertRaises(ValueError):
            box.decrypt(b"nope")
        with self.assertRaises(ValueError):
            box.decrypt(b"XXXXXX" + b"\x00" * 64)

    def test_rejects_short_secret(self):
        with self.assertRaises(ValueError):
            ExperimentalCipher(b"short")


class TestShamir(unittest.TestCase):
    def test_split_and_combine(self):
        secret = b"threshold-secret-value!!"
        shares = split_secret(secret, n=5, t=3)
        self.assertEqual(len(shares), 5)
        self.assertEqual(combine_shares(shares[:3]), secret)
        self.assertEqual(combine_shares(shares[2:]), secret)
        self.assertEqual(combine_shares(shares), secret)

    def test_two_shares_of_t3_do_not_suffice_via_threshold_api(self):
        box = ExperimentalThreshold(n=5, t=3)
        ct = box.encrypt(b"hello")
        recovered = box.decrypt_with_shares(box.shares[:3], ct)
        self.assertEqual(recovered, b"hello")
        with self.assertRaises(ValueError):
            box.decrypt_with_shares(box.shares[:2], ct)


class TestAesGcmOptional(unittest.TestCase):
    def test_round_trip_if_available(self):
        try:
            from qrmc.aead import AesGcmBox
        except ImportError:
            self.skipTest("cryptography not installed")
        box = AesGcmBox()
        msg = b"classical AEAD demo"
        token = box.encrypt(msg, associated_data=b"aad")
        self.assertEqual(box.decrypt(token, associated_data=b"aad"), msg)
        with self.assertRaises(Exception):
            box.decrypt(token, associated_data=b"wrong")

    def test_lazy_export(self):
        try:
            importlib.import_module("cryptography")
        except ImportError:
            self.skipTest("cryptography not installed")
        from qrmc import AesGcmBox

        box = AesGcmBox()
        self.assertEqual(box.decrypt(box.encrypt(b"z")), b"z")


if __name__ == "__main__":
    unittest.main()
