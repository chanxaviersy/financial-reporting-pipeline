<!-- 徽章 -->
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![CI](https://github.com/chanxaviersy/financial-reporting-pipeline/actions/workflows/test.yml/badge.svg)](https://github.com/chanxaviersy/financial-reporting-pipeline/actions)
[![Last Commit](https://img.shields.io/github/last-commit/chanxaviersy/financial-reporting-pipeline)](https://github.com/chanxaviersy/financial-reporting-pipeline)

---

# 金融数据自动化报表管道

> 自动化 SQL/Python 报表工作流 + 数据治理 + 风险监控

本项目源自简历中 UBS（2025.11 - 2026.7）的 Data Analyst 岗位经历。
将业务场景抽象为可复用的金融数据处理流水线，包含：

- 多源数据接入与对账
- 严格的数据质量校验
- 自动化报表生成（Excel + HTML 邮件）
- 风险指标实时监控
- 审计日志与合规追踪

## 项目目标

- 替代重复手工的 Excel 数据整合工作
- 标准化数据治理流程，确保合规性
- 为业务部门提供自助式分析视图
- 减少 40% 以上的人工运营周转时间

## 技术栈

- **数据**：Python (Pandas/NumPy), SQL, PostgreSQL/SQLite
- **报表**：openpyxl（Excel 自动化）, Jinja2（HTML 邮件模板）
- **调度**：Python 脚本（生产可换 Airflow/Prefect）
- **可视化**：Matplotlib（趋势图）
- **测试**：pytest

## 目录结构

```
04-financial-reporting-pipeline/
├── README.md
├── requirements.txt
├── config/
│   └── pipeline_config.yaml        # 管道配置
├── sql/
│   ├── reconciliation.sql          # 对账查询
│   └── risk_metrics.sql            # 风险指标查询
├── src/
│   ├── ingestion.py                # 数据接入（多源）
│   ├── governance.py               # 数据治理（校验 / 审计日志）
│   ├── reconciliation.py           # 多源数据对账
│   ├── reporting.py                # 报表生成（Excel + HTML）
│   ├── alerts.py                   # 异常告警
│   └── pipeline.py                 # 编排（主入口）
├── tests/
│   ├── test_governance.py
│   └── test_reconciliation.py
├── reports/                        # 报表输出目录
└── run_demo.py                     # 一键 Demo
```

## 快速开始

```bash
pip install -r requirements.txt
python run_demo.py
```

执行后会：

1. 生成 3 个数据源（交易系统、风控系统、客户主数据）的模拟数据
2. 执行对账、治理校验、风险指标计算
3. 在 `reports/` 下生成 Excel 报表 + HTML 邮件草稿
4. 输出审计日志到 `reports/audit_log.csv`

## 核心功能

### 1. 多源数据接入（ingestion）

模拟金融业务常见的多系统数据源：

- **Trading System**：交易明细
- **Risk System**：风险敞口
- **CRM**：客户主数据

### 2. 数据治理（governance）

按照 UBS 内部标准实施：

- **完整性校验**：必填字段检查
- **唯一性校验**：主键重复检查
- **范围校验**：金额、日期等业务字段范围
- **一致性校验**：跨表外键完整性
- **审计日志**：所有操作记录到 `audit_log`

### 3. 数据对账（reconciliation）

对交易系统、风控系统、客户主数据进行三方对账，找出：

- 金额不一致的记录
- 状态不一致的记录
- 客户信息不一致的记录

### 4. 报表生成（reporting）

- **Excel 多 Sheet 报表**：每日运营报表，包含 KPI、明细、异常
- **HTML 邮件草稿**：Jinja2 渲染，CC 给利益相关方

### 5. 风险监控（alerts）

对关键风险指标设置阈值：

- 单笔交易金额异常
- 客户集中度风险
- 当日 P&L 异常波动

## 配置

`config/pipeline_config.yaml` 支持自定义：

- 数据源连接信息
- 报表输出格式
- 邮件收件人
- 告警阈值

## 后续可扩展方向

- 接入真实 PostgreSQL + BI 工具
- 用 Airflow 实现生产级调度
- 加入 Slack/邮件自动推送
- 接入 Bloomberg/Reuters 行情数据
- 数据血缘追踪（lineage）

## License

MIT
## 📚 更多文档

- [项目架构](docs/architecture.md)
- [使用指南](docs/usage.md)
- [开发笔记](docs/dev-notes.md)
