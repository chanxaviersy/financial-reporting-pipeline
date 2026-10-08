"""对账单元测试。"""
from __future__ import annotations

import pandas as pd

from reconciliation import reconcile_trade_vs_risk


def test_reconcile_matching():
    trades = pd.DataFrame({"trade_id": ["T1", "T2"], "amount": [100.0, 200.0]})
    risks = pd.DataFrame({"trade_id": ["T1", "T2"], "exposure": [100.0, 200.0]})
    result = reconcile_trade_vs_risk(trades, risks)
    assert len(result["inconsistent_amount"]) == 0


def test_reconcile_amount_mismatch():
    trades = pd.DataFrame({"trade_id": ["T1", "T2"], "amount": [100.0, 200.0]})
    risks = pd.DataFrame({"trade_id": ["T1", "T2"], "exposure": [100.0, 250.0]})
    result = reconcile_trade_vs_risk(trades, risks)
    assert len(result["inconsistent_amount"]) == 1


def test_reconcile_only_in_trades():
    trades = pd.DataFrame({"trade_id": ["T1", "T2"], "amount": [100.0, 200.0]})
    risks = pd.DataFrame({"trade_id": ["T1"], "exposure": [100.0]})
    result = reconcile_trade_vs_risk(trades, risks)
    assert len(result["only_in_trades"]) == 1
    assert len(result["only_in_risk"]) == 0