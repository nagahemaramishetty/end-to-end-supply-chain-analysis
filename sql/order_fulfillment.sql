-- ============================================
-- 04. Order Fulfillment Analysis
-- How fast and completely are orders fulfilled?
-- ============================================

-- Average fulfillment days by product category
SELECT
    o."Product Category",
    o."Product Department",
    COUNT(*) AS total_orders,
    ROUND(AVG(f."Warehouse Order Fulfillment (days)"), 2) AS avg_fulfillment_days,
    MIN(f."Warehouse Order Fulfillment (days)") AS min_fulfillment_days,
    MAX(f."Warehouse Order Fulfillment (days)") AS max_fulfillment_days
FROM orders o
LEFT JOIN fulfillment f ON o."Product Name" = f."Product Name"
GROUP BY o."Product Category", o."Product Department"
ORDER BY avg_fulfillment_days DESC;

-- Perfect Order Rate
-- Orders with no delay AND fulfilled on time
SELECT
    COUNT(*) AS total_orders,
    SUM(CASE WHEN "Shipment Days - Scheduled" <= 0 THEN 1 ELSE 0 END) AS on_time_orders,
    ROUND(
        100.0 * SUM(CASE WHEN "Shipment Days - Scheduled" <= 0 THEN 1 ELSE 0 END) / COUNT(*), 2
    ) AS perfect_order_rate_pct
FROM orders;

-- Fulfillment performance by market
SELECT
    o."Customer Market",
    COUNT(*) AS total_orders,
    ROUND(AVG(f."Warehouse Order Fulfillment (days)"), 2) AS avg_fulfillment_days,
    ROUND(
        100.0 * SUM(CASE WHEN o."Shipment Days - Scheduled" <= 0 THEN 1 ELSE 0 END) / COUNT(*), 2
    ) AS on_time_rate_pct
FROM orders o
LEFT JOIN fulfillment f ON o."Product Name" = f."Product Name"
GROUP BY o."Customer Market"
ORDER BY on_time_rate_pct DESC;
