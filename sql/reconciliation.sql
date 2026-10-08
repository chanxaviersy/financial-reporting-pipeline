"""对账 SQL 查询（生产可对接 PostgreSQL）。"""

-- 交易系统 vs 风控系统金额一致性
SELECT
    t.trade_id,
    t.amount AS trade_amount,
    r.exposure AS risk_exposure,
    ABS(t.amount - r.exposure) AS diff,
    CASE
        WHEN r.exposure IS NULL THEN '仅交易系统'
        WHEN t.amount IS NULL THEN '仅风控系统'
        WHEN ABS(t.amount - r.exposure) > 0.01 THEN '金额不一致'
        ELSE '一致'
    END AS status
FROM trading_system t
FULL OUTER JOIN risk_system r USING (trade_id)
WHERE
    r.exposure IS NULL
    OR t.amount IS NULL
    OR ABS(t.amount - r.exposure) > 0.01;

-- 客户主数据完整性
SELECT
    t.client_id,
    c.name,
    c.risk_rating,
    CASE WHEN c.client_id IS NULL THEN '孤儿客户' ELSE '正常' END AS status
FROM trading_system t
LEFT JOIN crm c ON t.client_id = c.client_id
WHERE c.client_id IS NULL;