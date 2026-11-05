#!/usr/bin/env bash
# BaseForge 一键校验脚本 / One-shot verification script
set -euo pipefail

echo "==> 运行单元测试 / Running unit tests"
python3 -m unittest discover -s tests -v

echo "==> 版本 / Version"
python3 -c "import baseforge; print('baseforge', baseforge.__version__)"

echo "==> CLI 冒烟测试 / CLI smoke test"
python3 -m baseforge encode --algo base58 --data "hello world"
python3 -m baseforge shortid --len 12

echo "OK"
