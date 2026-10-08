"""数据治理单元测试。"""
from __future__ import annotations

import pandas as pd

from governance import (
    check_allowed_values,
    check_completeness,
    check_range,
    check_uniqueness,
)


def test_check_completeness_pass():
    df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
    result = check_completeness(df, ["a", "b"], "test")
    assert result.passed is True
    assert result.failed_count == 0


def test_check_completeness_fail():
    df = pd.DataFrame({"a": [1, None, 3], "b": ["x", "y", None]})
    result = check_completeness(df, ["a", "b"], "test")
    assert result.passed is False
    assert result.failed_count == 2


def test_check_uniqueness():
    df = pd.DataFrame({"id": [1, 2, 2, 3]})
    result = check_uniqueness(df, "id", "test")
    assert result.passed is False
    assert result.failed_count == 1


def test_check_range():
    df = pd.DataFrame({"value": [1, 5, 10, 100]})
    result = check_range(df, "value", 0, 50, "test")
    assert result.passed is False
    assert result.failed_count == 1


def test_check_allowed_values():
    df = pd.DataFrame({"status": ["A", "B", "C", "D"]})
    result = check_allowed_values(df, "status", ["A", "B", "C"], "test")
    assert result.passed is False
    assert result.failed_count == 1