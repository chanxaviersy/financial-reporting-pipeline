"""数据治理：完整性、唯一性、范围、一致性校验 + 审计日志。"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import pandas as pd


@dataclass
class ValidationResult:
    """单条校验结果。"""

    rule: str
    source: str
    passed: bool
    failed_count: int
    details: str


class AuditLog:
    """审计日志：记录所有数据治理操作。"""

    def __init__(self, log_path: str | Path):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        # 初始化为空 CSV
        if not self.log_path.exists():
            pd.DataFrame(columns=["timestamp", "action", "source", "details"]).to_csv(
                self.log_path, index=False
            )

    def record(self, action: str, source: str, details: str = "") -> None:
        entry = {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "action": action,
            "source": source,
            "details": details,
        }
        df = pd.DataFrame([entry])
        df.to_csv(self.log_path, mode="a", header=False, index=False)


def check_completeness(
    df: pd.DataFrame, required_columns: list[str], source: str
) -> ValidationResult:
    """完整性校验：必填列不能为空。"""
    failed = 0
    details_list = []
    for col in required_columns:
        if col not in df.columns:
            failed += len(df)
            details_list.append(f"列缺失: {col}")
            continue
        null_count = df[col].isnull().sum()
        failed += null_count
        if null_count > 0:
            details_list.append(f"{col}: {null_count} 个空值")
    return ValidationResult(
        rule="完整性",
        source=source,
        passed=failed == 0,
        failed_count=int(failed),
        details="; ".join(details_list) if details_list else "全部字段非空",
    )


def check_uniqueness(
    df: pd.DataFrame, primary_key: str, source: str
) -> ValidationResult:
    """唯一性校验：主键不能重复。"""
    if primary_key not in df.columns:
        return ValidationResult(
            rule="唯一性",
            source=source,
            passed=False,
            failed_count=len(df),
            details=f"主键列缺失: {primary_key}",
        )
    dup_count = df[primary_key].duplicated().sum()
    return ValidationResult(
        rule="唯一性",
        source=source,
        passed=dup_count == 0,
        failed_count=int(dup_count),
        details=f"{primary_key} 重复 {dup_count} 条" if dup_count > 0 else "主键唯一",
    )


def check_range(
    df: pd.DataFrame, column: str, min_value: float, max_value: float, source: str
) -> ValidationResult:
    """范围校验：数值列必须在合理范围内。"""
    if column not in df.columns:
        return ValidationResult(
            rule="范围",
            source=source,
            passed=False,
            failed_count=len(df),
            details=f"列缺失: {column}",
        )
    out_of_range = ((df[column] < min_value) | (df[column] > max_value)).sum()
    return ValidationResult(
        rule="范围",
        source=source,
        passed=out_of_range == 0,
        failed_count=int(out_of_range),
        details=f"{column} ∈ [{min_value}, {max_value}]",
    )


def check_allowed_values(
    df: pd.DataFrame, column: str, allowed: list[str], source: str
) -> ValidationResult:
    """枚举校验：字段值必须在白名单内。"""
    if column not in df.columns:
        return ValidationResult(
            rule="枚举",
            source=source,
            passed=False,
            failed_count=len(df),
            details=f"列缺失: {column}",
        )
    invalid = (~df[column].isin(allowed)).sum()
    return ValidationResult(
        rule="枚举",
        source=source,
        passed=invalid == 0,
        failed_count=int(invalid),
        details=f"{column} ∈ {allowed}",
    )


def check_foreign_key(
    df: pd.DataFrame, fk_column: str, reference_df: pd.DataFrame, reference_pk: str, source: str
) -> ValidationResult:
    """外键完整性校验。"""
    if fk_column not in df.columns:
        return ValidationResult(
            rule="外键",
            source=source,
            passed=False,
            failed_count=len(df),
            details=f"列缺失: {fk_column}",
        )
    invalid = (~df[fk_column].isin(reference_df[reference_pk])).sum()
    return ValidationResult(
        rule="外键",
        source=source,
        passed=invalid == 0,
        failed_count=int(invalid),
        details=f"{fk_column} -> {reference_pk}",
    )


def run_all_governance_checks(
    sources: dict[str, pd.DataFrame], config: dict, audit: AuditLog
) -> list[ValidationResult]:
    """对所有数据源执行完整的数据治理校验。"""
    results: list[ValidationResult] = []
    gov_cfg = config["governance"]

    # 交易系统
    if "trading_system" in sources:
        ts = sources["trading_system"]
        audit.record("GOVERNANCE", "trading_system", "开始校验")
        results.extend([
            check_completeness(ts, ["trade_id", "client_id", "amount", "status"], "trading_system"),
            check_uniqueness(ts, "trade_id", "trading_system"),
            check_range(ts, "amount", gov_cfg["amount"]["min_value"], gov_cfg["amount"]["max_value"], "trading_system"),
            check_allowed_values(ts, "status", gov_cfg["status"], "trading_system"),
        ])

    # 风控系统
    if "risk_system" in sources and "trading_system" in sources:
        rs = sources["risk_system"]
        ts = sources["trading_system"]
        audit.record("GOVERNANCE", "risk_system", "开始校验")
        results.extend([
            check_completeness(rs, ["trade_id", "exposure"], "risk_system"),
            check_uniqueness(rs, "trade_id", "risk_system"),
            check_foreign_key(rs, "trade_id", ts, "trade_id", "risk_system"),
        ])

    # CRM
    if "crm" in sources:
        crm = sources["crm"]
        audit.record("GOVERNANCE", "crm", "开始校验")
        results.extend([
            check_completeness(crm, ["client_id", "name", "risk_rating"], "crm"),
            check_uniqueness(crm, "client_id", "crm"),
        ])

    audit.record("GOVERNANCE", "ALL", f"完成 {len(results)} 项校验")
    return results