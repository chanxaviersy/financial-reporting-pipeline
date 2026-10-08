"""多源数据对账。"""
from __future__ import annotations

import pandas as pd


def reconcile_trade_vs_risk(
    trades: pd.DataFrame, risks: pd.DataFrame, tolerance: float = 0.01
) -> dict[str, pd.DataFrame]:
    """交易系统 vs 风控系统对账：检查每笔交易的金额与风控敞口是否一致。"""
    merged = trades.merge(risks, on="trade_id", how="outer", suffixes=("_trade", "_risk"))
    merged["amount_diff"] = (merged["amount"] - merged["exposure"]).abs()

    inconsistent = merged[merged["amount_diff"] > tolerance].copy()

    # 仅在交易系统中存在
    only_in_trades = merged[merged["exposure"].isna()].copy()
    # 仅在风控系统中存在
    only_in_risk = merged[merged["amount"].isna()].copy()

    return {
        "inconsistent_amount": inconsistent,
        "only_in_trades": only_in_trades,
        "only_in_risk": only_in_risk,
    }


def reconcile_client_info(
    trades: pd.DataFrame, crm: pd.DataFrame
) -> pd.DataFrame:
    """交易关联的客户信息反查：检查所有交易客户都在 CRM 中存在。"""
    clients_in_trades = trades["client_id"].unique()
    clients_in_crm = crm["client_id"].unique()

    orphan_clients = set(clients_in_trades) - set(clients_in_crm)
    if not orphan_clients:
        return pd.DataFrame()
    return pd.DataFrame({"orphan_client_id": list(orphan_clients)})


def summarize_reconciliation(recon_results: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """汇总对账结果。"""
    summary = []
    for name, df in recon_results.items():
        summary.append({"对账项": name, "不一致条数": len(df)})
    return pd.DataFrame(summary)