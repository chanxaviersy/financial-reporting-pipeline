"""风险监控与告警。"""
from __future__ import annotations

import pandas as pd


def check_alerts(
    trades: pd.DataFrame, config: dict, audit_log=None
) -> list[dict]:
    """检查所有告警规则。"""
    alerts = []
    cfg = config["alerts"]

    # 规则 1: 单笔交易金额超限
    max_threshold = cfg["single_trade_max_amount"]
    large_trades = trades[trades["amount"] > max_threshold]
    if not large_trades.empty:
        alerts.append({
            "level": "🔴 高",
            "rule": "单笔交易金额超限",
            "message": f"共 {len(large_trades)} 笔交易金额超过 {max_threshold:,.0f}",
            "count": len(large_trades),
        })
        if audit_log:
            audit_log.record("ALERT", "large_trades", f"发现 {len(large_trades)} 笔大额交易")

    # 规则 2: 客户集中度风险
    total = trades["amount"].sum()
    client_totals = trades.groupby("client_id")["amount"].sum().sort_values(ascending=False)
    threshold = cfg["client_concentration_pct"]
    top_pct = client_totals.iloc[0] / total if total > 0 else 0
    if top_pct > threshold:
        alerts.append({
            "level": "🟡 中",
            "rule": "客户集中度风险",
            "message": f"Top 1 客户占总成交额 {top_pct:.2%}（阈值 {threshold:.0%}）",
            "count": 1,
        })

    # 规则 3: 当日 P&L 波动
    vol_threshold = cfg["daily_pnl_volatility_pct"]
    daily_pnl = trades.groupby(trades["trade_date"])["daily_pnl"].sum()
    if not daily_pnl.empty and daily_pnl.std() != 0:
        cv = abs(daily_pnl.std() / (daily_pnl.mean() + 1e-10))
        if cv > vol_threshold:
            alerts.append({
                "level": "🟡 中",
                "rule": "P&L 波动率异常",
                "message": f"日 P&L 波动系数 {cv:.2%}（阈值 {vol_threshold:.0%}）",
                "count": 1,
            })

    if not alerts:
        alerts.append({
            "level": "🟢 正常",
            "rule": "所有检查项",
            "message": "无异常告警",
            "count": 0,
        })

    return alerts