"""主流程编排。"""
from __future__ import annotations

from pathlib import Path

import pandas as pd
import yaml

from alerts import check_alerts
from governance import AuditLog, run_all_governance_checks
from ingestion import load_all_sources
from reconciliation import (
    reconcile_client_info,
    reconcile_trade_vs_risk,
    summarize_reconciliation,
)
from reporting import generate_excel_report, generate_html_email


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def load_config() -> dict:
    config_path = PROJECT_ROOT / "config" / "pipeline_config.yaml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def generate_synthetic_data(data_dir: Path) -> None:
    """生成 3 个数据源的模拟数据。"""
    data_dir.mkdir(parents=True, exist_ok=True)
    import numpy as np

    rng = np.random.default_rng(42)

    # 1. CRM
    n_clients = 100
    crm = pd.DataFrame({
        "client_id": [f"C{i:04d}" for i in range(1, n_clients + 1)],
        "name": [f"Client_{i}" for i in range(1, n_clients + 1)],
        "risk_rating": rng.choice(["LOW", "MEDIUM", "HIGH"], n_clients, p=[0.6, 0.3, 0.1]),
        "kyc_status": rng.choice(["VERIFIED", "PENDING"], n_clients, p=[0.9, 0.1]),
    })
    crm.to_csv(data_dir / "crm.csv", index=False)

    # 2. 交易系统
    n_trades = 1000
    trades = pd.DataFrame({
        "trade_id": [f"T{i:06d}" for i in range(1, n_trades + 1)],
        "client_id": rng.choice(crm["client_id"], n_trades),
        "amount": rng.exponential(scale=100000, size=n_trades).round(2),
        "status": rng.choice(["SETTLED", "PENDING", "CANCELLED", "FAILED"], n_trades, p=[0.7, 0.15, 0.1, 0.05]),
        "trade_date": rng.choice(pd.date_range("2024-10-01", periods=90).strftime("%Y-%m-%d"), n_trades),
    })
    # 故意制造 5 条异常数据（超出阈值）
    trades.loc[:4, "amount"] = 200_000_000
    trades.to_csv(data_dir / "trading_system.csv", index=False)

    # 3. 风控系统（与交易系统大致一致，但有少量不一致）
    risk = trades[["trade_id", "client_id"]].copy()
    risk["exposure"] = trades["amount"] * rng.uniform(0.95, 1.05, size=n_trades)
    # 故意让 10 笔交易金额不一致
    mismatch_idx = rng.choice(risk.index, 10, replace=False)
    risk.loc[mismatch_idx, "exposure"] *= 1.2
    # 添加一个风控系统独有的 trade_id
    extra = pd.DataFrame({"trade_id": ["T999999"], "client_id": ["C0001"], "exposure": [50000.0]})
    risk = pd.concat([risk, extra], ignore_index=True)
    risk.to_csv(data_dir / "risk_system.csv", index=False)

    print(f"[DATA] 已生成模拟数据：CRM={len(crm)}, Trades={len(trades)}, Risk={len(risk)}")


def run_pipeline(generate_data: bool = True) -> None:
    """运行完整管道。"""
    config = load_config()
    base_dir = PROJECT_ROOT

    if generate_data:
        generate_synthetic_data(base_dir / "data")

    # 审计日志
    audit = AuditLog(base_dir / config["reporting"]["audit_log_path"])
    audit.record("PIPELINE_START", "ALL", "管道启动")

    # 1. 数据接入
    print("\n[PIPELINE] Step 1: 数据接入")
    sources = load_all_sources(config, base_dir)

    # 2. 数据治理
    print("\n[PIPELINE] Step 2: 数据治理")
    gov_results = run_all_governance_checks(sources, config, audit)
    failed = sum(1 for r in gov_results if not r.passed)
    print(f"  完成 {len(gov_results)} 项校验，{failed} 项失败")

    # 3. 数据对账
    print("\n[PIPELINE] Step 3: 数据对账")
    trades = sources["trading_system"]
    risks = sources["risk_system"]
    crm = sources["crm"]

    recon_trade_risk = reconcile_trade_vs_risk(trades, risks)
    orphan = reconcile_client_info(trades, crm)
    recon_results = {
        "交易金额不一致": recon_trade_risk["inconsistent_amount"],
        "仅在交易系统中": recon_trade_risk["only_in_trades"],
        "仅在风控系统中": recon_trade_risk["only_in_risk"],
        "孤儿客户": orphan,
    }
    summary = summarize_reconciliation({k: v for k, v in recon_results.items() if isinstance(v, pd.DataFrame)})
    print(summary.to_string(index=False))

    # 4. 风险告警
    print("\n[PIPELINE] Step 4: 风险告警")
    trades_with_pnl = trades.copy()
    trades_with_pnl["daily_pnl"] = trades_with_pnl["amount"] * rng_pnl(len(trades_with_pnl))
    alerts = check_alerts(trades_with_pnl, config, audit)
    for a in alerts:
        print(f"  [{a['level']}] {a['rule']}: {a['message']}")

    # 5. 报表生成
    print("\n[PIPELINE] Step 5: 报表生成")
    kpis = {
        "gmv": float(trades["amount"].sum()),
        "trade_count": len(trades),
        "client_count": int(trades["client_id"].nunique()),
        "avg_trade": float(trades["amount"].mean()),
    }
    generate_excel_report(
        trades, gov_results, recon_results,
        base_dir / config["reporting"]["excel_path"],
    )
    generate_html_email(
        config["pipeline"]["name"],
        kpis,
        gov_results,
        recon_results,
        alerts,
        base_dir / config["reporting"]["html_email_path"],
    )

    audit.record("PIPELINE_END", "ALL", "管道结束")
    print("\n[PIPELINE] ✅ 全部完成")


def rng_pnl(n: int):
    """生成 P&L 因子（模拟收益/损失）。"""
    import numpy as np
    return np.random.default_rng(123).normal(loc=0, scale=0.02, size=n)


if __name__ == "__main__":
    run_pipeline()