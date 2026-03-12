-- ============================================
-- 05. Supply vs Demand Gap Analysis
-- Which products are understocked or overstocked?
-- ============================================

-- Supply vs Demand by Product Department
SELECT
    o."Product Department",
    ROUND(AVG(i."Warehouse Inventory"), 0) AS avg_supply,
    ROUND(AVG(o."Order Quantity"), 0) AS avg_demand_per_order,
    SUM(o."Order Quantity") AS total_demand,
    ROUND(AVG(i."Warehouse Inventory") - AVG(o."Order Quantity"), 0) AS supply_demand_gap,
    CASE
        WHEN AVG(i."Warehouse Inventory") < AVG(o."Order Quantity") THEN 'UNDERSTOCKED'
        WHEN AVG(i."Warehouse Inventory") > AVG(o."Order Quantity") * 3 THEN 'OVERSTOCKED'
        ELSE 'BALANCED'
    END AS stock_status
FROM orders o
LEFT JOIN inventory i ON o."Product Name" = i."Product Name"
GROUP BY o."Product Department"
ORDER BY supply_demand_gap ASC;

-- Top 10 understocked products (high demand, low inventory)
SELECT
    o."Product Name",
    o."Product Category",
    SUM(o."Order Quantity") AS total_demand,
    ROUND(AVG(i."Warehouse Inventory"), 0) AS avg_inventory,
    ROUND(AVG(i."Warehouse Inventory") - SUM(o."Order Quantity") / 12.0, 0) AS monthly_gap
FROM orders o
LEFT JOIN inventory i ON o."Product Name" = i."Product Name"
GROUP BY o."Product Name", o."Product Category"
HAVING monthly_gap < 0
ORDER BY monthly_gap ASC
LIMIT 10;

-- Top 10 overstocked products (low demand, high inventory)
SELECT
    o."Product Name",
    o."Product Category",
    SUM(o."Order Quantity") AS total_demand,
    ROUND(AVG(i."Warehouse Inventory"), 0) AS avg_inventory,
    ROUND(AVG(i."Warehouse Inventory") - SUM(o."Order Quantity") / 12.0, 0) AS monthly_surplus
FROM orders o
LEFT JOIN inventory i ON o."Product Name" = i."Product Name"
GROUP BY o."Product Name", o."Product Category"
HAVING monthly_surplus > 0
ORDER BY monthly_surplus DESC
LIMIT 10;
