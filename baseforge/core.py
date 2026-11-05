"""BaseForge —— 零依赖的 Base 编码工具箱。

Zero-dependency base-encoding toolkit: Base16 / Base32 / Base58 / Base62 /
Base64 / Base85 (ascii85 & RFC1924) plus a cryptographically-random short-id
generator. Base58 and Base62 are implemented from scratch (not in the stdlib);
the rest wrap the standard library.

纯 Python 标准库实现，无第三方依赖，可离线运行。
Pure Python standard library only — no third-party dependencies, fully offline.
"""
from __future__ import annotations

import base64
import os
import secrets
from typing import Dict, List

__all__ = [
    "BASE16", "BASE32", "BASE58_BTC", "BASE62", "BASE64", "BASE85_RFC1924",
    "ALGOS", "encode", "decode", "shortid", "b58encode", "b58decode",
    "b62encode", "b62decode", "BaseForgeError",
]

# ---------------------------------------------------------------------------
# 字母表 / Alphabets
# ---------------------------------------------------------------------------

BASE16 = "0123456789ABCDEF"
BASE32 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"          # RFC 4648
BASE58_BTC = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"  # Bitcoin
BASE62 = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
BASE64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
BASE85_RFC1924 = ("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                  "abcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~")

_ALGO_ALPHABETS: Dict[str, str] = {
    "base16": BASE16,
    "base32": BASE32,
    "base58": BASE58_BTC,
    "base62": BASE62,
    "base64": BASE64,
    "base85": BASE85_RFC1924,
}
ALGOS: List[str] = sorted(_ALGO_ALPHABETS)


class BaseForgeError(ValueError):
    """BaseForge 编解码错误 / Raised on invalid algorithm or payload."""


# ---------------------------------------------------------------------------
# 大整数编解码（Base58 / Base62 自研）/ Big-int codec (Base58/62 from scratch)
# ---------------------------------------------------------------------------

def _bytes_to_int(data: bytes) -> int:
    return int.from_bytes(data, "big")


def _int_to_bytes(n: int) -> bytes:
    if n == 0:
        return b"\x00"
    length = (n.bit_length() + 7) // 8
    return n.to_bytes(length, "big")


def _leading_zero_count(data: bytes) -> int:
    count = 0
    for b in data:
        if b == 0:
            count += 1
        else:
            break
    return count


def b58encode(data: bytes, alphabet: str = BASE58_BTC) -> str:
    """Base58 编码（Bitcoin 字母表，原始无校验和）/ Encode bytes to Base58."""
    if alphabet != BASE58_BTC and len(alphabet) != 58:
        raise BaseForgeError("Base58 字母表必须恰好 58 个字符 / Base58 needs 58 chars")
    n = _bytes_to_int(data)
    out = ""
    while n > 0:
        n, rem = divmod(n, 58)
        out = alphabet[rem] + out
    return alphabet[0] * _leading_zero_count(data) + out


def b58decode(text: str, alphabet: str = BASE58_BTC) -> bytes:
    """Base58 解码 / Decode a Base58 string back to bytes."""
    if alphabet != BASE58_BTC and len(alphabet) != 58:
        raise BaseForgeError("Base58 字母表必须恰好 58 个字符 / Base58 needs 58 chars")
    rev = {c: i for i, c in enumerate(alphabet)}
    pad = 0
    for ch in text:
        if ch == alphabet[0]:
            pad += 1
        else:
            break
    rest = text[pad:]
    if not rest:
        return b"\x00" * pad
    n = 0
    for ch in rest:
        if ch not in rev:
            raise BaseForgeError(f"非法 Base58 字符: {ch!r} / invalid Base58 char")
        n = n * 58 + rev[ch]
    return b"\x00" * pad + _int_to_bytes(n)


def b62encode(data: bytes, alphabet: str = BASE62) -> str:
    """Base62 编码 / Encode bytes to Base62 (0-9A-Za-z)."""
    if len(alphabet) != 62:
        raise BaseForgeError("Base62 字母表必须恰好 62 个字符 / Base62 needs 62 chars")
    if not data:
        return ""
    n = _bytes_to_int(data)
    out = ""
    while n > 0:
        n, rem = divmod(n, 62)
        out = alphabet[rem] + out
    return alphabet[0] * _leading_zero_count(data) + out


def b62decode(text: str, alphabet: str = BASE62) -> bytes:
    """Base62 解码 / Decode a Base62 string back to bytes."""
    if len(alphabet) != 62:
        raise BaseForgeError("Base62 字母表必须恰好 62 个字符 / Base62 needs 62 chars")
    if not text:
        return b""
    rev = {c: i for i, c in enumerate(alphabet)}
    pad = 0
    for ch in text:
        if ch == alphabet[0]:
            pad += 1
        else:
            break
    rest = text[pad:]
    if not rest:
        return b"\x00" * pad
    n = 0
    for ch in rest:
        if ch not in rev:
            raise BaseForgeError(f"非法 Base62 字符: {ch!r} / invalid Base62 char")
        n = n * 62 + rev[ch]
    return b"\x00" * pad + _int_to_bytes(n)


# ---------------------------------------------------------------------------
# 统一接口 / Unified API (stdlib-backed)
# ---------------------------------------------------------------------------

def encode(data: bytes, algo: str) -> str:
    """将字节编码为指定 Base 字符串 / Encode bytes with the given algorithm."""
    algo = algo.lower()
    if algo == "base16":
        return base64.b16encode(data).decode("ascii")
    if algo == "base32":
        return base64.b32encode(data).decode("ascii")
    if algo == "base58":
        return b58encode(data)
    if algo == "base62":
        return b62encode(data)
    if algo == "base64":
        return base64.b64encode(data).decode("ascii")
    if algo == "base85":
        # RFC 1924 base85 (zero-padded to multiples of 4 bytes)
        padded = data + b"\x00" * ((4 - len(data) % 4) % 4)
        chunks = []
        for i in range(0, len(padded), 4):
            v = int.from_bytes(padded[i:i + 4], "big")
            s = ""
            for _ in range(5):
                v, rem = divmod(v, 85)
                s = BASE85_RFC1924[rem] + s
            chunks.append(s)
        return "".join(chunks)
    raise BaseForgeError(f"不支持的算法: {algo!r} / unsupported algorithm: {algo!r}")


def decode(text: str, algo: str) -> bytes:
    """将 Base 字符串解码为字节 / Decode a string with the given algorithm."""
    algo = algo.lower()
    if algo == "base16":
        return base64.b16decode(text.strip())
    if algo == "base32":
        return base64.b32decode(text.strip())
    if algo == "base58":
        return b58decode(text.strip())
    if algo == "base62":
        return b62decode(text.strip())
    if algo == "base64":
        return base64.b64decode(text.strip())
    if algo == "base85":
        rev = {c: i for i, c in enumerate(BASE85_RFC1924)}
        text = text.strip()
        if len(text) % 5 != 0:
            raise BaseForgeError("Base85 长度必须是 5 的倍数 / Base85 length must be a multiple of 5")
        out = b""
        for i in range(0, len(text), 5):
            v = 0
            for ch in text[i:i + 5]:
                if ch not in rev:
                    raise BaseForgeError(f"非法 Base85 字符: {ch!r}")
                v = v * 85 + rev[ch]
            out += v.to_bytes(4, "big")
        return out.rstrip(b"\x00")
    raise BaseForgeError(f"不支持的算法: {algo!r} / unsupported algorithm: {algo!r}")


def shortid(length: int = 12, alphabet: str = BASE62) -> str:
    """生成密码学随机短 ID（默认 Base62）/ Generate a random short id.

    Uses `secrets` for cryptographic randomness — suitable for URLs, tokens
    and primary-key surrogates (not for security secrets).
    """
    if length < 1:
        raise BaseForgeError("长度必须 >= 1 / length must be >= 1")
    return "".join(secrets.choice(alphabet) for _ in range(length))
