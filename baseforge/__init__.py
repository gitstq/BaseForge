"""BaseForge —— 零依赖的 Base 编码工具箱。

Zero-dependency base-encoding toolkit: Base16/32/58/62/64/85 plus a random
short-id generator. Base58 & Base62 are implemented from scratch; the rest wrap
the Python standard library. Pure stdlib, no third-party dependencies.
"""
from __future__ import annotations

from .core import (
    ALGOS, BASE16, BASE32, BASE58_BTC, BASE62, BASE64, BASE85_RFC1924,
    BaseForgeError, b58decode, b58encode, b62decode, b62encode, decode,
    encode, shortid,
)

__version__ = "1.0.0"
__all__ = [
    "ALGOS", "BASE16", "BASE32", "BASE58_BTC", "BASE62", "BASE64",
    "BASE85_RFC1924", "BaseForgeError", "b58encode", "b58decode",
    "b62encode", "b62decode", "encode", "decode", "shortid", "__version__",
]
