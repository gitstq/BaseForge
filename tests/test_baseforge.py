"""BaseForge 单元测试 / Unit tests for BaseForge.

运行 / Run:
    python3 -m unittest discover -s tests
    # 或 / or
    python3 -m pytest tests/ -q
"""
from __future__ import annotations

import os
import secrets
import unittest

from baseforge import (
    ALGOS, BaseForgeError, b58decode, b58encode, b62decode, b62encode,
    decode, encode, shortid,
)


class TestStdlibBacked(unittest.TestCase):
    def test_base64_vector(self):
        self.assertEqual(encode(b"hello", "base64"), "aGVsbG8=")
        self.assertEqual(decode("aGVsbG8=", "base64"), b"hello")

    def test_base32_vector(self):
        self.assertEqual(encode(b"hello", "base32"), "NBSWY3DP")
        self.assertEqual(decode("NBSWY3DP", "base32"), b"hello")

    def test_base16_vector(self):
        self.assertEqual(encode(b"\x01\x02\xff", "base16"), "0102FF")
        self.assertEqual(decode("0102FF", "base16"), b"\x01\x02\xff")


class TestBase58(unittest.TestCase):
    def test_vector(self):
        self.assertEqual(b58encode(b"hello world"), "StV1DL6CwTryKyV")
        self.assertEqual(b58decode("StV1DL6CwTryKyV"), b"hello world")

    def test_leading_zeros(self):
        self.assertEqual(b58encode(b"\x00\x00"), "11")
        self.assertEqual(b58decode("11"), b"\x00\x00")

    def test_roundtrip(self):
        for _ in range(300):
            d = os.urandom(secrets.randbelow(40) + 1)
            self.assertEqual(b58decode(b58encode(d)), d)


class TestBase62(unittest.TestCase):
    def test_roundtrip(self):
        for _ in range(300):
            d = os.urandom(secrets.randbelow(40) + 1)
            self.assertEqual(b62decode(b62encode(d)), d)

    def test_empty(self):
        self.assertEqual(b62encode(b""), "")
        self.assertEqual(b62decode(""), b"")

    def test_leading_zero(self):
        self.assertEqual(b62encode(b"\x00\x00\x01"), "00" + b62encode(b"\x01"))
        self.assertEqual(b62decode("001"), b"\x00\x00\x01")


class TestUnified(unittest.TestCase):
    def test_roundtrip_all(self):
        for algo in ALGOS:
            if algo == "base85":
                # base85 会去除尾部零字节，故用无尾部零的数据 / base85 strips trailing zeros
                data = b"\x01\x02\x03\x04\x05\x06"
            else:
                data = b"\x00\x10hello\x00\x01world"
            self.assertEqual(decode(encode(data, algo), algo), data)

    def test_unknown_algo(self):
        with self.assertRaises(BaseForgeError):
            encode(b"x", "base99")
        with self.assertRaises(BaseForgeError):
            decode("x", "base99")


class TestShortid(unittest.TestCase):
    def test_length(self):
        for n in (1, 8, 12, 32):
            self.assertEqual(len(shortid(n)), n)

    def test_charset(self):
        sid = shortid(128)
        allowed = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        self.assertTrue(all(c in allowed for c in sid))

    def test_uniqueness(self):
        ids = {shortid(16) for _ in range(200)}
        self.assertEqual(len(ids), 200)


if __name__ == "__main__":
    unittest.main()
