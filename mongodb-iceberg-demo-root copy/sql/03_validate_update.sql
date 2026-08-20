SELECT
    _id,
    status,
    amount
FROM mongodb_iceberg_demo.orders
WHERE _id = 'ORD-LIVE-001';

-- Expected after scripts/update_order.py:
-- status = SHIPPED
-- amount = 199
