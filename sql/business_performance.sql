-- ============================================
-- 03. Business Performance KPIs
-- Profit, revenue, and top products
-- ============================================

-- Overall business summary
SELECT
    COUNT(DISTINCT "Order ID") AS total_orders,
    COUNT(DISTINCT "Customer ID") AS total_customers,
    ROUND(SUM("Gross Sales"), 2) AS total_revenue,
    ROUND(SUM("Profit"), 2) AS total_profit,
    -- ROUND(AVG(TRY_CAST("Discount %" AS DOUBLE)), 2) AS avg_discount_pct,
    ROUND(SUM("Profit") / NULLIF(SUM("Gross Sales"), 0) * 100, 2) AS overall_profit_margin_pct
FROM orders;

-- Profit by Product Department
SELECT
    "Product Department",
    COUNT(*) AS total_orders,
    ROUND(SUM("Gross Sales"), 2) AS total_revenue,
    ROUND(SUM("Profit"), 2) AS total_profit,
    ROUND(SUM("Profit") / NULLIF(SUM("Gross Sales"), 0) * 100, 2) AS profit_margin_pct
FROM orders
GROUP BY "Product Department"
ORDER BY total_profit DESC;

-- Top 10 most profitable products
SELECT
    "Product Name",
    "Product Category",
    COUNT(*) AS total_orders,
    ROUND(SUM("Profit"), 2) AS total_profit,
    ROUND(AVG("Profit"), 2) AS avg_profit_per_order,
    ROUND(SUM("Profit") / NULLIF(SUM("Gross Sales"), 0) * 100, 2) AS profit_margin_pct
FROM orders
GROUP BY "Product Name", "Product Category"
ORDER BY total_profit DESC
LIMIT 10;

-- Revenue trend by Year and Month
SELECT
    "Order Year",
    "Order Month",
    COUNT(DISTINCT "Order ID") AS total_orders,
    ROUND(SUM("Gross Sales"), 2) AS monthly_revenue,
    ROUND(SUM("Profit"), 2) AS monthly_profit
FROM orders
GROUP BY "Order Year", "Order Month"
ORDER BY "Order Year", "Order Month";
