# 贡献指南 / Contributing

感谢你为 **BaseForge** 做出贡献！本仓库遵循 [Conventional Commits](https://www.conventionalcommits.org/) 提交规范。

## 开发环境 / Development setup

```bash
git clone https://github.com/gitstq/BaseForge.git
cd BaseForge
python3 -m pip install -e .
python3 -m unittest discover -s tests   # 运行测试 / run tests
```

## 提交规范 / Commit convention

- `feat:` 新增功能
- `fix:` 修复问题
- `docs:` 文档更新
- `refactor:` 代码重构
- `test:` 测试相关
- `chore:` 构建/工程配置

## 提交 PR 前 / Before opening a PR

1. 确保所有单元测试通过 / ensure `python3 -m unittest discover -s tests` passes
2. 保持零依赖（仅标准库）/ keep zero third-party dependencies (stdlib only)
3. 若新增算法，请补充对应测试向量（含已知值）/ add test vectors for new algorithms

## Issue 反馈 / Issue reporting

请在 [Issues](https://github.com/gitstq/BaseForge/issues) 中提供：算法类型、输入、期望与实际输出、Python 版本。
