"""一键运行 Demo：生成数据 → 执行管道 → 输出报表。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))

from pipeline import run_pipeline  # noqa: E402


def main() -> None:
    print("=" * 60)
    print("  金融数据自动化报表管道 - 一键 Demo")
    print("=" * 60)
    run_pipeline(generate_data=True)

    print("\n[DEMO] 报表输出在 reports/ 目录：")
    print("  - reports/daily_report.xlsx")
    print("  - reports/email_draft.html")
    print("  - reports/audit_log.csv")


if __name__ == "__main__":
    main()