SELECT
    region,
    COUNT(*) AS orders,
    SUM(amount) AS revenue
FROM mongodb_iceberg_demo.orders
GROUP BY region
ORDER BY revenue DESC;
