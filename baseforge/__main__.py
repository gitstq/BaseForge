"""BaseForge CLI —— 零依赖 Base 编码命令行工具。

Usage:
    python -m baseforge encode --algo base58 --data "hello world"
    python -m baseforge decode --algo base58 --data "StV1DL6CwTryKyV"
    python -m baseforge shortid --len 12
    python -m baseforge list
"""
from __future__ import annotations

import argparse
import sys
from typing import List, Optional

from .core import ALGOS, BaseForgeError, decode, encode, shortid


def _cmd_encode(args: argparse.Namespace) -> int:
    try:
        result = encode(args.data.encode("utf-8"), args.algo)
    except BaseForgeError as e:
        print(f"编码失败 / encode error: {e}", file=sys.stderr)
        return 2
    print(result)
    return 0


def _cmd_decode(args: argparse.Namespace) -> int:
    try:
        raw = decode(args.data, args.algo)
    except BaseForgeError as e:
        print(f"解码失败 / decode error: {e}", file=sys.stderr)
        return 2
    try:
        print(raw.decode("utf-8"))
    except UnicodeDecodeError:
        print(raw.hex())
    return 0


def _cmd_shortid(args: argparse.Namespace) -> int:
    try:
        sid = shortid(args.len)
    except BaseForgeError as e:
        print(f"生成失败 / generate error: {e}", file=sys.stderr)
        return 2
    print(sid)
    return 0


def _cmd_list(args: argparse.Namespace) -> int:
    print("支持的算法 / supported algorithms:")
    for a in ALGOS:
        print(f"  - {a}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="baseforge",
        description="BaseForge — 零依赖 Base 编码工具箱 / zero-dependency base-encoding toolkit")
    sub = p.add_subparsers(dest="command", required=True)

    se = sub.add_parser("encode", help="编码 / encode")
    se.add_argument("--algo", "-a", required=True, choices=ALGOS)
    se.add_argument("--data", "-d", required=True, help="待编码文本 / text to encode")
    se.set_defaults(func=_cmd_encode)

    sd = sub.add_parser("decode", help="解码 / decode")
    sd.add_argument("--algo", "-a", required=True, choices=ALGOS)
    sd.add_argument("--data", "-d", required=True, help="待解码文本 / text to decode")
    sd.set_defaults(func=_cmd_decode)

    ss = sub.add_parser("shortid", help="生成随机短 ID / generate random short id")
    ss.add_argument("--len", "-n", type=int, default=12, help="长度 / length (default 12)")
    ss.set_defaults(func=_cmd_shortid)

    sl = sub.add_parser("list", help="列出算法 / list algorithms")
    sl.set_defaults(func=_cmd_list)

    return p


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
