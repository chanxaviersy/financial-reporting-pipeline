<!-- ============= 顶部徽章 ============= -->
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/PostgreSQL-15%2B-336791?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL"/>
  <img src="https://img.shields.io/badge/pytest-8.0%2B-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" alt="pytest"/>
  <img src="https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge" alt="License"/>
</p>

<p align="center">
  <a href="https://github.com/chanxaviersy/financial-reporting-pipeline/actions/workflows/test.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/chanxaviersy/financial-reporting-pipeline/test.yml?label=CI&style=flat-square" alt="CI"/>
  </a>
  <a href="https://github.com/chanxaviersy/financial-reporting-pipeline">
    <img src="https://img.shields.io/github/last-commit/chanxaviersy/financial-reporting-pipeline?style=flat-square" alt="Last Commit"/>
  </a>
  <a href="https://github.com/chanxaviersy/financial-reporting-pipeline/stargazers">
    <img src="https://img.shields.io/github/stars/chanxaviersy/financial-reporting-pipeline?style=flat-square" alt="Stars"/>
  </a>
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square" alt="PRs Welcome"/>
</p>

<!-- ============= 标题区 ============= -->
<br/>
<div align="center">

# 💰 金融数据自动化报表管道

### 多源对账 · 数据治理 · 风险监控 · Excel/HTML 报表

[🚀 快速开始](#-快速开始) · [📖 文档](docs/architecture.md) · [🐛 报告 Bug](https://github.com/chanxaviersy/financial-reporting-pipeline/issues) · [💡 提出新特性](https://github.com/chanxaviersy/financial-reporting-pipeline/issues)

</div>

<!-- ============= 项目亮点卡片 ============= -->
<p align="center">
  <table>
    <tr>
      <td align="center" width="200">
        <h3>🔄</h3>
        <b>3 源对账</b><br/>
        <sub><code>交易 / 风控 / CRM</code></sub>
      </td>
      <td align="center" width="200">
        <h3>🛡</h3>
        <b>5 项治理</b><br/>
        <sub><code>完整/唯一/范围/一致/审计</code></sub>
      </td>
      <td align="center" width="200">
        <h3>📋</h3>
        <b>Excel + HTML</b><br/>
        <sub><code>Jinja2 邮件模板</code></sub>
      </td>
      <td align="center" width="200">
        <h3>⚠️</h3>
        <b>实时告警</b><br/>
        <sub><code>风险阈值 + 邮件</code></sub>
      </td>
    </tr>
  </table>
</p>

---

<!-- ============= 目录 ============= -->
## 📑 目录

- [🎯 项目目标](#-项目目标)
- [🛠 技术栈](#-技术栈)
- [📂 目录结构](#-目录结构)
- [🚀 快速开始](#-快速开始)
- [✨ 核心功能](#-核心功能)
- [⚙️ 配置](#️-配置)
- [🚀 后续可扩展方向](#-后续可扩展方向)
- [📚 更多文档](#-更多文档)
- [📄 License](#-license)

---

## 🎯 项目目标

- 替代重复手工的 Excel 数据整合工作
- 标准化数据治理流程，确保合规性
- 为业务部门提供自助式分析视图
- 减少 **40%+** 的人工运营周转时间

> 本项目源自简历中 UBS（2025.11 - 2026.7）的 Data Analyst 岗位经历。将业务场景抽象为可复用的金融数据处理流水线。

---

## 🛠 技术栈

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,pandas,numpy,postgres,sqlite,git,github,vscode" alt="Tech Stack"/>
</p>

| 类别       | 技术                                                  |
| ---------- | ----------------------------------------------------- |
| **数据**   | Python（Pandas/NumPy）、SQL、PostgreSQL/SQLite        |
| **报表**   | openpyxl（Excel 自动化）、Jinja2（HTML 邮件模板）     |
| **调度**   | Python 脚本（生产可换 Airflow/Prefect）               |
| **可视化** | Matplotlib（趋势图）                                  |
| **测试**   | pytest                                                |

---

## 📂 目录结构

```
04-financial-reporting-pipeline/
├── 📄 README.md
├── 📋 requirements.txt
├── ⚙️ config/
│   └── pipeline_config.yaml        # 管道配置
├── 📂 sql/
│   ├── reconciliation.sql          # 对账查询
│   └── risk_metrics.sql            # 风险指标查询
├── 🐍 src/
│   ├── ingestion.py                # 数据接入（多源）
│   ├── governance.py               # 数据治理（校验 / 审计日志）
│   ├── reconciliation.py           # 多源数据对账
│   ├── reporting.py                # 报表生成（Excel + HTML）
│   ├── alerts.py                   # 异常告警
│   └── pipeline.py                 # 编排（主入口）
├── 🧪 tests/
│   ├── test_governance.py
│   └── test_reconciliation.py
├── 📂 reports/                     # 报表输出目录
├── 📚 docs/                        # 详细文档
│   ├── architecture.md
│   ├── usage.md
│   └── dev-notes.md
└── 🎬 run_demo.py                  # 一键 Demo
```

---

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/chanxaviersy/financial-reporting-pipeline.git
cd financial-reporting-pipeline
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 运行 Demo

```bash
python run_demo.py
```

执行后会：
1. ✅ 生成 3 个数据源（交易系统、风控系统、客户主数据）的模拟数据
2. ✅ 执行对账、治理校验、风险指标计算
3. ✅ 在 `reports/` 下生成 Excel 报表 + HTML 邮件草稿
4. ✅ 输出审计日志到 `reports/audit_log.csv`

### 跑测试

```bash
pytest tests/ -v
# 带覆盖率
pytest tests/ -v --cov=src
```

---

## ✨ 核心功能

### 🔄 1. 多源数据接入（ingestion）

模拟金融业务常见的多系统数据源：

- **Trading System**：交易明细
- **Risk System**：风险敞口
- **CRM**：客户主数据

### 🛡 2. 数据治理（governance）

按照 UBS 内部标准实施：

- ✅ **完整性校验**：必填字段检查
- ✅ **唯一性校验**：主键重复检查
- ✅ **范围校验**：金额、日期等业务字段范围
- ✅ **一致性校验**：跨表外键完整性
- ✅ **审计日志**：所有操作记录到 `audit_log`

### ⚖️ 3. 数据对账（reconciliation）

对交易系统、风控系统、客户主数据进行三方对账，找出：

- 金额不一致的记录
- 状态不一致的记录
- 客户信息不一致的记录

### 📋 4. 报表生成（reporting）

- **Excel 多 Sheet 报表**：每日运营报表，包含 KPI、明细、异常
- **HTML 邮件草稿**：Jinja2 渲染，CC 给利益相关方

### ⚠️ 5. 风险监控（alerts）

对关键风险指标设置阈值：

- 单笔交易金额异常
- 客户集中度风险
- 当日 P&L 异常波动

### 📸 可视化

> 截图待补充：运行 `run_demo.py` 后会生成报告与图表，保存到 [`assets/`](assets/)。

---

## ⚙️ 配置

`config/pipeline_config.yaml` 支持自定义：

- 数据源连接信息
- 报表输出格式
- 邮件收件人
- 告警阈值

```bash
cp config/pipeline_config.yaml.example config/pipeline_config.yaml
# 编辑你的配置
```

---

## 🚀 后续可扩展方向

- 接入真实 PostgreSQL + BI 工具
- 用 Airflow 实现生产级调度
- 加入 Slack/邮件自动推送
- 接入 Bloomberg/Reuters 行情数据
- 数据血缘追踪（lineage）

---

## 📚 更多文档

| 文档 | 说明 |
|------|------|
| [📐 项目架构](docs/architecture.md) | 整体设计、模块关系、数据流 |
| [📖 使用指南](docs/usage.md) | 详细安装、配置、模块使用 |
| [🔧 开发笔记](docs/dev-notes.md) | 踩过的坑、性能优化、审计经验 |
| [📝 CHANGELOG](CHANGELOG.md) | 版本变更记录 |
| [🤝 CONTRIBUTING](CONTRIBUTING.md) | 如何参与贡献 |

---

## 📄 License

本项目基于 [MIT](LICENSE) 协议开源。

---

<div align="center">

**[⬆ 回到顶部](#-金融数据自动化报表管道)**

Made with ❤️ by [Xavier Chen](https://github.com/chanxaviersy)

</div>
