# Demo Flow: Operational to Lakehouse in 5 Minutes

## Before the meeting

1. Atlas cluster is running.
2. `iceberg_demo.orders` contains the seeded records.
3. S3 bucket exists.
4. Glue database exists.
5. Stream Processing source and S3 connections are READY.
6. `ordersToIceberg` is RUNNING.
7. Athena can query `mongodb_iceberg_demo.orders`.

## Demo

### 1. Establish the baseline

Show one order in Atlas, then run:

```sql
SELECT region, COUNT(*) AS orders, SUM(amount) AS revenue
FROM mongodb_iceberg_demo.orders
GROUP BY region
ORDER BY revenue DESC;
```

Message: **This is the operational MongoDB collection represented as an open Iceberg table.**

### 2. Insert

```bash
python scripts/insert_order.py
```

Run `sql/02_find_live_order.sql`.

Message: **No export job, Kafka connector, or Spark ingestion job was started.**

### 3. Update

```bash
python scripts/update_order.py
```

Run `sql/03_validate_update.sql`.

Message: **This is CDC table maintenance, not an append-only pile of files.**

### 4. Delete

```bash
python scripts/delete_order.py
```

Run `sql/04_validate_delete.sql`.

Message: **The operational delete is reflected in the Iceberg table.**

### 5. Schema evolution

```bash
python scripts/add_schema_field.py
```

The new MongoDB document includes:

```text
fraudScore: 0.92
```

Run `sql/05_validate_schema.sql` and show the new field/column.

Message: **The document model changed without rebuilding an ETL schema mapping.**

## Close

> MongoDB remains the operational system of record. Atlas Stream Processing continuously publishes that operational data into an open Apache Iceberg table that analytics engines can consume.

## Cleanup

```bash
python scripts/reset_demo.py
```

If you want to stop the processor:

```javascript
load("stream-processing/stop_processor.js")
```
