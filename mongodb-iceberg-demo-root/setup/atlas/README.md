# Atlas Setup

The demo needs four Atlas pieces.

## 1. Atlas Cluster

Create or reuse an Atlas cluster in any supported cloud.

The Python scripts use:

```text
Database:   iceberg_demo
Collection: orders
```

The collection is automatically created when `scripts/seed_orders.py` writes the first document.

## 2. Stream Processing Workspace

Create a Stream Processing workspace in the same Atlas project.

For this demo, use a workspace/processor configuration that can run **SP10**. `$iceberg` currently supports SP10, SP30, and SP50.

## 3. Atlas Source Connection

In the workspace Connection Registry, create an Atlas connection to the cluster.

Recommended demo name:

```text
atlas-orders
```

`stream-processing/create_processor.js` expects this name by default.

## 4. S3 Connection

After completing `setup/aws/bootstrap.sh` and Unified AWS Access, create an AWS S3 connection.

Recommended demo name:

```text
s3-iceberg
```

## 5. Stream Processing Database User

Connect `mongosh` to the Stream Processing workspace with a database user that can create and start stream processors. `atlasAdmin` is the simplest demo role.

## 6. Create the Processor

Edit the constants at the top of:

```text
stream-processing/create_processor.js
```

Then, from `mongosh` connected to the Stream Processing workspace:

```javascript
load("stream-processing/create_processor.js")
```

If you run `mongosh` from a different working directory, use the full path to the file.

## Cross-Cloud

The Atlas source can be on AWS, Azure, or GCP. The `$iceberg` sink currently targets S3. If the Stream Processing workspace is not on AWS, `region` is required in the `$iceberg` stage. The demo specifies it unconditionally for clarity.

Official docs:

- https://www.mongodb.com/docs/atlas/atlas-stream-processing/
- https://www.mongodb.com/docs/atlas/atlas-stream-processing/manage-connection-registry/
- https://www.mongodb.com/docs/manual/reference/method/sp.createstreamprocessor/
