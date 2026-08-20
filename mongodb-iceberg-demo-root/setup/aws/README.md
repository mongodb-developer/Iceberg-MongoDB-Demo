# AWS Setup

`bootstrap.sh` handles only the demo resources owned by your AWS account:

- S3 bucket
- S3 public-access blocking
- Glue database

Run:

```bash
./bootstrap.sh
```

It writes the resulting values to `aws-values.txt`.

## Atlas Access to AWS

Atlas Stream Processing S3 connections require **Unified AWS Access**.

In Atlas:

1. Configure/authorize an AWS IAM role through Unified AWS Access.
2. Grant that role the S3 and Glue permissions required for the demo bucket/catalog.
3. In the Stream Processing workspace Connection Registry, create an AWS S3 sink connection named `s3-iceberg` using that role.
4. If you use private connectivity, configure the appropriate S3 Private Link path as well.

Use the Atlas UI-generated trust relationship / external ID rather than inventing one in this repository.

Official docs:

- https://www.mongodb.com/docs/atlas/atlas-stream-processing/security/
- https://www.mongodb.com/docs/atlas/atlas-stream-processing/manage-connection-registry/
- https://www.mongodb.com/docs/atlas/atlas-stream-processing/sp-agg-iceberg/
