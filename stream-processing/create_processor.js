// Run this file from mongosh CONNECTED TO THE ATLAS STREAM PROCESSING WORKSPACE.
//
// Example inside mongosh:
//   load("stream-processing/create_processor.js")
//
// Edit these constants before running.

const PROCESSOR_NAME = "ordersToIceberg";
const SOURCE_CONNECTION = "atlas-orders";
const SOURCE_DATABASE = "iceberg_demo";
const SOURCE_COLLECTION = "orders";

const S3_CONNECTION = "s3-iceberg";
const S3_BUCKET = "mongodb-iceberg-demo-REPLACE_ME";
const AWS_REGION = "us-east-1";
const ICEBERG_DATABASE = "mongodb_iceberg_demo";
const ICEBERG_TABLE = "orders";
const ICEBERG_PATH = "iceberg-warehouse/";

const isDeleteExpr = {
  $eq: [{ $meta: "stream.source.operationType" }, "delete"]
};

const pipeline = [
  {
    $source: {
      connectionName: SOURCE_CONNECTION,
      db: SOURCE_DATABASE,
      coll: SOURCE_COLLECTION,
      initialSync: {
        enable: true
      },
      config: {
        fullDocument: "required"
      }
    }
  },
  {
    $match: {
      operationType: {
        $in: ["insert", "update", "delete", "replace"]
      }
    }
  },
  {
    $replaceRoot: {
      newRoot: {
        $cond: {
          if: isDeleteExpr,
          then: "$documentKey",
          else: "$fullDocument"
        }
      }
    }
  },
  {
    $iceberg: {
      connectionName: S3_CONNECTION,
      bucket: S3_BUCKET,
      databaseName: ICEBERG_DATABASE,
      tableName: ICEBERG_TABLE,
      path: ICEBERG_PATH,
      region: AWS_REGION,
      mode: "cdc",
      idFieldName: "_id",
      catalog: {
        type: "glue"
      }
    }
  }
];

print(`Creating stream processor ${PROCESSOR_NAME}...`);
sp.createStreamProcessor(PROCESSOR_NAME, pipeline);

print(`Starting ${PROCESSOR_NAME} on SP10...`);
sp.ordersToIceberg.start({ tier: "SP10" });

print("Processor started. Use load(\"stream-processing/status.js\") to see stats.");
