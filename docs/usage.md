# 详细使用指南

## 安装

```bash
git clone https://github.com/chanxaviersy/financial-reporting-pipeline.git
cd financial-reporting-pipeline
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 配置

```bash
cp .env.example .env
# 填入数据库连接、告警邮箱等
```

## 运行

### Demo

```bash
python run_demo.py
```

### 跑测试

```bash
pytest tests/ -v
```

输出测试报告（含覆盖率）：
```bash
pytest tests/ -v --cov=src
```

## 模块使用

### 接入数据

```python
from src.ingestion import fetch_orders

df = fetch_orders(
    source="postgres",
    start_date="2024-01-01",
    end_date="2024-01-31",
)
```

### 对账

```python
from src.reconciliation import reconcile

diff_df = reconcile(
    orders_df=orders,
    finance_df=finance,
    bank_df=bank,
    tolerance=0.01,
)
print(f"差异行数: {len(diff_df)}")
```

### 治理检查

```python
from src.governance import check_data_quality

report = check_data_quality(df)
print(report)
```

### 生成报告

```python
from src.reporting import generate_monthly_report

generate_monthly_report(
    year=2024,
    month=1,
    output_path="reports/2024-01.xlsx",
)
```

## Cron 调度

```cron
# 每天 02:00 跑管道
0 2 * * * cd /opt/fin-pipeline && python src/pipeline.py >> /var/log/fin.log 2>&1
```

## 常见问题

**Q: 数据库连接失败？**
A: 检查 `.env` 的 `DATABASE_URL` 格式：`postgresql://user:pass@host:port/db`。

**Q: 告警邮件没收到？**
A: 检查 `ALERT_EMAIL` + SMTP 配置（环境变量）。

**Q: 怎么加新数据源？**
A: 在 `src/ingestion.py` 加新函数，输出统一 schema 即可。

## 扩展

- **换 Airflow**：把 `pipeline.py` 拆成 DAG 任务
- **加新指标**：在 `src/reporting.py` 加 Excel sheet
- **加新告警**：在 `src/alerts.py` 加规则
