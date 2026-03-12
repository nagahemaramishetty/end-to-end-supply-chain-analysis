-- ============================================
-- 01. Shipment Delay Analysis
-- How many orders are delayed and by how much?
-- ============================================

-- Overall delay rate
SELECT
    COUNT(*) AS total_orders,
    SUM(CASE WHEN "Shipment Days - Scheduled" > 0 THEN 1 ELSE 0 END) AS delayed_orders,
    ROUND(
        100.0 * SUM(CASE WHEN "Shipment Days - Scheduled" > 0 THEN 1 ELSE 0 END) / COUNT(*), 2
    ) AS delay_rate_pct,
    ROUND(AVG("Shipment Days - Scheduled"), 2) AS avg_delay_days
FROM orders;

-- Delay rate by Shipment Mode
SELECT
    "Shipment Mode",
    COUNT(*) AS total_orders,
    ROUND(
        100.0 * SUM(CASE WHEN "Shipment Days - Scheduled" > 0 THEN 1 ELSE 0 END) / COUNT(*), 2
    ) AS delay_rate_pct,
    ROUND(AVG("Shipment Days - Scheduled"), 2) AS avg_delay_days
FROM orders
GROUP BY "Shipment Mode"
ORDER BY delay_rate_pct DESC;

-- Delay rate by Customer Region
SELECT
    "Customer Region",
    COUNT(*) AS total_orders,
    ROUND(
        100.0 * SUM(CASE WHEN "Shipment Days - Scheduled" > 0 THEN 1 ELSE 0 END) / COUNT(*), 2
    ) AS delay_rate_pct,
    ROUND(AVG("Shipment Days - Scheduled"), 2) AS avg_delay_days
FROM orders
GROUP BY "Customer Region"
ORDER BY delay_rate_pct DESC;

-- Top 10 most delayed products
SELECT
    "Product Name",
    COUNT(*) AS total_orders,
    ROUND(AVG("Shipment Days - Scheduled"), 2) AS avg_delay_days,
    ROUND(
        100.0 * SUM(CASE WHEN "Shipment Days - Scheduled" > 0 THEN 1 ELSE 0 END) / COUNT(*), 2
    ) AS delay_rate_pct
FROM orders
GROUP BY "Product Name"
HAVING COUNT(*) > 50
ORDER BY avg_delay_days DESC
LIMIT 10;
