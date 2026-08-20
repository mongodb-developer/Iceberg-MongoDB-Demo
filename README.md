# MongoDB Atlas `$iceberg` Demo

A small end-to-end demo showing how operational data in MongoDB Atlas can be continuously published as an Apache Iceberg v2 table in Amazon S3 using Atlas Stream Processing.

The goal is to make the value obvious:

> **MongoDB operational data → Atlas Stream Processing → Iceberg on S3 → SQL analytics**

No Kafka, no custom CDC service, no Spark ingestion job, and no separate ETL pipeline required for the basic flow.

---

## What This Demo Shows

The demo uses a simple `orders` collection in MongoDB Atlas and walks through four live changes:

1. **INSERT** a new order in MongoDB and see it appear in Iceberg.
2. **UPDATE** the order and see the Iceberg table reflect the change.
3. **DELETE** the order and confirm it disappears from the Iceberg table.
4. **ADD A NEW FIELD** to demonstrate schema evolution.

The Iceberg table is stored in Amazon S3 and registered in AWS Glue so it can be queried with Athena and other Iceberg-compatible analytics engines.

---

## Architecture

```text
                  Demo App / Python
                         |
                         v
                  MongoDB Atlas
                    orders
                         |
                  Change Stream
                         |
                         v
             Atlas Stream Processing
                transform / project
                         |
                     $iceberg
                         |
                         v
                    Amazon S3
                Apache Iceberg v2
                         |
                     AWS Glue
                         |
                         v
                    Amazon Athena
```

### Cross-Cloud Note

The `$iceberg` destination is Amazon S3 today, but the MongoDB Atlas source does not have to run on AWS.

For example:

```text
Atlas on Azure
      |
Atlas Stream Processing
      |
cross-cloud transfer
      |
Amazon S3 + Iceberg + Glue
```

That works, but cross-cloud network latency and egress cost should be considered.

---

## Demo Data Model

Example document:

```javascript
{
  _id: "ORD-10042",
  customerId: "C-8831",
  region: "TX",
  product: "Running Shoes",
  quantity: 2,
  amount: 189.98,
  status: "PROCESSING",
  orderDate: ISODate("2026-08-20T12:30:00Z")
}
```

The operational model stays in MongoDB while Atlas Stream Processing can shape the output into an analytics-friendly Iceberg table.

---

## Demo Flow

### 1. Seed MongoDB

Load a small set of sample orders into Atlas.

Planned script:

```bash
python scripts/seed_orders.py
```

---

### 2. Start Atlas Stream Processing

Create a Stream Processing pipeline that:

- Reads from the Atlas `orders` collection
- Performs any required projection or flattening
- Writes to an Iceberg v2 table in Amazon S3
- Registers table metadata with AWS Glue
- Runs in CDC mode so inserts, updates, replaces, and deletes are reflected downstream

The `$iceberg` stage is the final stage in the pipeline.

---

### 3. Query the Iceberg Table

Using Athena:

```sql
SELECT
    region,
    COUNT(*) AS orders,
    SUM(amount) AS revenue
FROM mongodb_iceberg_demo.orders
GROUP BY region
ORDER BY revenue DESC;
```

---

### 4. Insert a Live Order

```javascript
db.orders.insertOne({
  _id: "ORD-LIVE-001",
  customerId: "C-JEFF",
  region: "IL",
  product: "MongoDB Hoodie",
  quantity: 3,
  amount: 225,
  status: "PROCESSING",
  orderDate: new Date()
})
```

Then query Athena:

```sql
SELECT *
FROM mongodb_iceberg_demo.orders
WHERE _id = 'ORD-LIVE-001';
```

Expected result: the new MongoDB document appears as a row in the Iceberg table.

---

### 5. Update the Order

```javascript
db.orders.updateOne(
  { _id: "ORD-LIVE-001" },
  {
    $set: {
      status: "SHIPPED",
      amount: 199
    }
  }
)
```

Query Athena again.

Expected result: the Iceberg row now shows the updated values.

---

### 6. Delete the Order

```javascript
db.orders.deleteOne({
  _id: "ORD-LIVE-001"
})
```

Query:

```sql
SELECT *
FROM mongodb_iceberg_demo.orders
WHERE _id = 'ORD-LIVE-001';
```

Expected result:

```text
0 rows
```

This demonstrates that the integration is maintaining table state rather than simply dumping change events into S3.

---

### 7. Demonstrate Schema Evolution

Insert a document containing a new field:

```javascript
db.orders.insertOne({
  _id: "ORD-LIVE-002",
  customerId: "C-9999",
  region: "CA",
  product: "MacBook Pro",
  quantity: 1,
  amount: 3499,
  status: "REVIEW",
  fraudScore: 0.92,
  orderDate: new Date()
})
```

The demo will then verify that the Iceberg table evolves to include the new field.

---

## Planned Repository Structure

```text
mongodb-iceberg-demo/
├── README.md
├── requirements.txt
├── config.py
├── scripts/
│   ├── seed_orders.py
│   ├── insert_order.py
│   ├── update_order.py
│   ├── delete_order.py
│   └── add_schema_field.py
├── stream-processing/
│   └── iceberg_pipeline.js
├── sql/
│   ├── orders_by_region.sql
│   ├── find_live_order.sql
│   └── validate_schema.sql
└── docs/
    └── architecture.png
```

---

## Prerequisites

### MongoDB

- MongoDB Atlas cluster
- Database and collection for the demo
- Atlas Stream Processing workspace
- Connection from Stream Processing to the Atlas cluster

### AWS

- Amazon S3 bucket
- AWS Glue Data Catalog
- IAM permissions required by Atlas Stream Processing
- Amazon Athena for the simplest SQL demo

### Local

- Python 3.10+
- `pymongo`

Install dependencies:

```bash
pip install pymongo
```

---

## Configuration

For a demo repo, configuration can initially live in `config.py`.

Example:

```python
MONGODB_URI = "mongodb+srv://..."
DATABASE_NAME = "iceberg_demo"
COLLECTION_NAME = "orders"
```

AWS and Atlas Stream Processing connection details will be added as the demo is built out.

Do not commit real production credentials to a public repository.

---

## Why Iceberg Matters

S3 by itself stores files.

Iceberg adds the table abstraction around those files:

- Table schema
- Metadata and manifests
- Snapshots
- Partitioning
- Schema evolution
- Update and delete semantics
- Compatibility with multiple analytics engines

In simple terms:

> **S3 holds the files. Iceberg makes those files behave like a table.**

The `$iceberg` stage lets MongoDB continuously publish operational data into that table format.

---

## Demo Message

The demo is intentionally small.

The point is not to prove how many millions of events can be pushed through the system. The point is to show how little plumbing is required to keep operational MongoDB data synchronized with an open lakehouse table.

The key sequence is:

```text
INSERT → UPDATE → DELETE → SCHEMA CHANGE
```

If those four operations are visible end-to-end from MongoDB to Athena, the architecture speaks for itself.

---

## Next Steps

The remaining build work is:

- [ ] Create Atlas cluster and `orders` collection
- [ ] Create S3 bucket
- [ ] Configure AWS Glue
- [ ] Create Atlas Stream Processing workspace
- [ ] Configure Atlas and AWS connections
- [ ] Build the `$iceberg` pipeline
- [ ] Add Python seed and CRUD scripts
- [ ] Add Athena validation queries
- [ ] Add architecture image
- [ ] Record the final demo flow

---

## Working Title

**Operational to Lakehouse in 5 Minutes**

MongoDB Atlas remains the operational system of record while Atlas Stream Processing continuously publishes the data into an open Apache Iceberg table for analytics.
