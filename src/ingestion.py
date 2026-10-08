"""数据接入：从多个数据源加载数据。"""
from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_source(source_path: str | Path, source_name: str) -> pd.DataFrame:
    """加载单个数据源。

    生产环境可扩展为：
    - PostgreSQL / MySQL 数据库连接
    - SFTP / S3 文件下载
    - REST API / Kafka 消息流
    """
    path = Path(source_path)
    if not path.exists():
        raise FileNotFoundError(f"数据源不存在: {path}")

    if path.suffix == ".csv":
        df = pd.read_csv(path)
    elif path.suffix in {".xlsx", ".xls"}:
        df = pd.read_excel(path)
    elif path.suffix == ".parquet":
        df = pd.read_parquet(path)
    else:
        raise ValueError(f"不支持的文件类型: {path.suffix}")

    print(f"[INGESTION] {source_name}: {len(df)} 条记录")
    return df


def load_all_sources(config: dict, base_dir: Path) -> dict[str, pd.DataFrame]:
    """根据配置加载所有数据源。"""
    sources = {}
    for name, src_cfg in config["sources"].items():
        path = base_dir / src_cfg["path"]
        sources[name] = load_source(path, name)
    return sources