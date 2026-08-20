SELECT *
FROM mongodb_iceberg_demo.orders
WHERE _id = 'ORD-LIVE-001';

-- Expected after scripts/delete_order.py: 0 rows
