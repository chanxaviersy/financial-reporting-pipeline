"""报表生成：Excel + HTML 邮件草稿。"""
from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pandas as pd
from jinja2 import Template


HTML_EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>{{ pipeline_name }} - 日报</title>
<style>
  body { font-family: 'Helvetica Neue', Arial, sans-serif; color: #333; max-width: 800px; margin: 0 auto; padding: 20px; }
  h1 { color: #1f4e79; border-bottom: 2px solid #1f4e79; padding-bottom: 10px; }
  h2 { color: #2e75b6; margin-top: 30px; }
  table { border-collapse: collapse; width: 100%; margin: 10px 0; }
  th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
  th { background-color: #1f4e79; color: white; }
  .kpi-row { display: flex; justify-content: space-around; margin: 20px 0; }
  .kpi { text-align: center; padding: 15px; background-color: #f0f4f8; border-radius: 8px; min-width: 150px; }
  .kpi-value { font-size: 24px; font-weight: bold; color: #1f4e79; }
  .kpi-label { color: #666; font-size: 14px; margin-top: 5px; }
  .alert { background-color: #fff3cd; border-left: 4px solid #ffc107; padding: 10px; margin: 10px 0; }
  .footer { color: #999; font-size: 12px; margin-top: 30px; text-align: center; }
</style>
</head>
<body>
<h1>📊 {{ pipeline_name }} - {{ report_date }}</h1>

<div class="kpi-row">
  <div class="kpi">
    <div class="kpi-value">¥{{ "{:,.0f}".format(kpis.gmv) }}</div>
    <div class="kpi-label">总成交额</div>
  </div>
  <div class="kpi">
    <div class="kpi-value">{{ kpis.trade_count }}</div>
    <div class="kpi-label">交易笔数</div>
  </div>
  <div class="kpi">
    <div class="kpi-value">{{ kpis.client_count }}</div>
    <div class="kpi-label">活跃客户数</div>
  </div>
  <div class="kpi">
    <div class="kpi-value">¥{{ "{:,.0f}".format(kpis.avg_trade) }}</div>
    <div class="kpi-label">平均交易额</div>
  </div>
</div>

{% if alerts %}
<h2>⚠️ 风险告警</h2>
{% for alert in alerts %}
<div class="alert">
  <strong>{{ alert.level }}</strong>: {{ alert.message }}
</div>
{% endfor %}
{% else %}
<h2>✅ 今日无异常告警</h2>
{% endif %}

<h2>数据治理结果</h2>
{{ governance_table }}

<h2>对账结果</h2>
{{ reconciliation_table }}

<div class="footer">
  报告生成时间: {{ generated_at }}<br>
  本报告由自动化管道生成，如有疑问请联系数据团队。
</div>
</body>
</html>
"""


def generate_excel_report(
    trades: pd.DataFrame,
    governance_results: list,
    recon_results: dict,
    output_path: str | Path,
) -> None:
    """生成 Excel 多 Sheet 报表。"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        # Sheet 1: 概览
        overview = pd.DataFrame({
            "指标": ["总成交额", "交易笔数", "活跃客户数", "平均交易额"],
            "数值": [
                trades["amount"].sum(),
                len(trades),
                trades["client_id"].nunique(),
                trades["amount"].mean(),
            ],
        })
        overview.to_excel(writer, sheet_name="概览", index=False)

        # Sheet 2: 交易明细（脱敏：保留前 1000 条）
        trades.head(1000).to_excel(writer, sheet_name="交易明细", index=False)

        # Sheet 3: 数据治理结果
        gov_df = pd.DataFrame([
            {
                "规则": r.rule,
                "数据源": r.source,
                "是否通过": "✅" if r.passed else "❌",
                "失败条数": r.failed_count,
                "详情": r.details,
            }
            for r in governance_results
        ])
        gov_df.to_excel(writer, sheet_name="数据治理", index=False)

        # Sheet 4: 对账结果
        recon_summary = []
        for name, df in recon_results.items():
            if isinstance(df, pd.DataFrame) and not df.empty:
                recon_summary.append({"对账项": name, "不一致条数": len(df)})
            else:
                recon_summary.append({"对账项": name, "不一致条数": 0})
        pd.DataFrame(recon_summary).to_excel(writer, sheet_name="对账结果", index=False)

    print(f"[REPORT] Excel 报表已生成: {output_path}")


def generate_html_email(
    pipeline_name: str,
    kpis: dict,
    governance_results: list,
    recon_results: dict,
    alerts: list[dict],
    output_path: str | Path,
) -> None:
    """生成 HTML 邮件草稿。"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 把 governance 结果渲染为 HTML 表格
    gov_html = "<table><tr><th>规则</th><th>数据源</th><th>结果</th><th>失败条数</th></tr>"
    for r in governance_results:
        status = "✅" if r.passed else "❌"
        gov_html += f"<tr><td>{r.rule}</td><td>{r.source}</td><td>{status}</td><td>{r.failed_count}</td></tr>"
    gov_html += "</table>"

    recon_html = "<table><tr><th>对账项</th><th>不一致条数</th></tr>"
    for name, df in recon_results.items():
        n = len(df) if isinstance(df, pd.DataFrame) else 0
        recon_html += f"<tr><td>{name}</td><td>{n}</td></tr>"
    recon_html += "</table>"

    template = Template(HTML_EMAIL_TEMPLATE)
    html = template.render(
        pipeline_name=pipeline_name,
        report_date=datetime.now().strftime("%Y-%m-%d"),
        kpis=kpis,
        alerts=alerts,
        governance_table=gov_html,
        reconciliation_table=recon_html,
        generated_at=datetime.now().isoformat(timespec="seconds"),
    )

    output_path.write_text(html, encoding="utf-8")
    print(f"[REPORT] HTML 邮件草稿已生成: {output_path}")