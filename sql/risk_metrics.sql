-- 风险指标聚合（生产可对接 PostgreSQL）

-- 客户集中度（前 10 大客户）
SELECT
    client_id,
    SUM(amount) AS total_amount,
    SUM(amount) * 100.0 / (SELECT SUM(amount) FROM trading_system) AS pct_of_total
FROM trading_system
WHERE status = 'SETTLED'
GROUP BY client_id
ORDER BY total_amount DESC
LIMIT 10;

-- 单日大额交易监控
SELECT
    trade_date,
    COUNT(*)            AS large_trade_count,
    SUM(amount)         AS large_trade_amount
FROM trading_system
WHERE amount > 1000000
GROUP BY trade_date
ORDER BY trade_date DESC;

-- 当日 P&L 波动
SELECT
    trade_date,
    SUM(CASE WHEN status = 'SETTLED' THEN amount ELSE 0 END) AS gross_inflow,
    SUM(CASE WHEN status IN ('CANCELLED', 'FAILED') THEN amount ELSE 0 END) AS cancelled_amount
FROM trading_system
GROUP BY trade_date
ORDER BY trade_date DESC;