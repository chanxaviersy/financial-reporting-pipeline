# 贡献指南

感谢你对本项目的兴趣！以下是如何参与贡献。

## 报告问题

- 使用 [GitHub Issues](https://github.com/chanxaviersy/financial-reporting-pipeline/issues)
- 描述清楚：复现步骤、预期结果、实际结果、环境信息

## 提交代码

1. Fork 本仓库
2. 创建 feature 分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'feat: Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 代码规范

- 遵循 PEP 8
- 使用 type hints
- 关键函数写 docstring
- 提交前跑 `pytest tests/` 与 `flake8 src/`

## Commit 规范

遵循 [Conventional Commits](https://www.conventionalcommits.org/)：

- `feat:` 新功能
- `fix:` 修 bug
- `docs:` 文档
- `style:` 格式调整
- `refactor:` 重构
- `test:` 测试
- `chore:` 杂项
