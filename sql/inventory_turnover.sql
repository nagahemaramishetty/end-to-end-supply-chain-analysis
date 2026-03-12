-- ============================================
-- 02. Inventory Turnover & Storage Cost
-- Which products move fast vs sit in warehouse?
-- ============================================

-- Inventory turnover ratio by product
-- Turnover = Total Units Sold / Average Warehouse Inventory
SELECT
    o."Product Name",
    o."Product Category",
    SUM(o."Order Quantity") AS total_units_sold,
    ROUND(AVG(i."Warehouse Inventory"), 2) AS avg_inventory,
    ROUND(
        SUM(o."Order Quantity") * 1.0 / NULLIF(AVG(i."Warehouse Inventory"), 0), 2
    ) AS inventory_turnover_ratio,
    ROUND(SUM(i."Inventory Cost Per Unit" * i."Warehouse Inventory"), 2) AS total_storage_cost
FROM orders o
LEFT JOIN inventory i ON o."Product Name" = i."Product Name"
GROUP BY o."Product Name", o."Product Category"
ORDER BY inventory_turnover_ratio DESC
LIMIT 20;

-- Most expensive products to store (highest carrying cost)
SELECT
    "Product Name",
    ROUND(AVG("Inventory Cost Per Unit"), 2) AS avg_cost_per_unit,
    ROUND(AVG("Warehouse Inventory"), 0) AS avg_inventory_units,
    ROUND(AVG("Inventory Cost Per Unit") * AVG("Warehouse Inventory"), 2) AS avg_monthly_carrying_cost
FROM inventory
GROUP BY "Product Name"
ORDER BY avg_monthly_carrying_cost DESC
LIMIT 10;

-- Overstock: products with high inventory but low sales
SELECT
    i."Product Name",
    ROUND(AVG(i."Warehouse Inventory"), 0) AS avg_inventory,
    COALESCE(SUM(o."Order Quantity"), 0) AS total_units_sold,
    ROUND(AVG(i."Warehouse Inventory") - COALESCE(SUM(o."Order Quantity") / 12.0, 0), 0) AS excess_stock_estimate
FROM inventory i
LEFT JOIN orders o ON i."Product Name" = o."Product Name"
GROUP BY i."Product Name"
ORDER BY excess_stock_estimate DESC
LIMIT 10;
