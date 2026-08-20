SELECT *
FROM mongodb_iceberg_demo.orders
WHERE _id = 'ORD-LIVE-002';

-- The row was inserted with a new MongoDB field:
-- fraudScore = 0.92
--
-- Athena may normalize identifier casing in its UI/catalog. If needed,
-- inspect the table columns and query the normalized fraudScore column name.
