#!/usr/bin/env bash
set -euo pipefail

command -v aws >/dev/null 2>&1 || {
  echo "AWS CLI is required. Install/configure it first." >&2
  exit 1
}

AWS_REGION="${AWS_REGION:-us-east-1}"
GLUE_DATABASE="${GLUE_DATABASE:-mongodb_iceberg_demo}"
ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text)"
S3_BUCKET="${S3_BUCKET:-mongodb-iceberg-demo-${ACCOUNT_ID}}"

if aws s3api head-bucket --bucket "$S3_BUCKET" >/dev/null 2>&1; then
  echo "S3 bucket already exists and is accessible: $S3_BUCKET"
else
  echo "Creating S3 bucket: $S3_BUCKET in $AWS_REGION"
  if [[ "$AWS_REGION" == "us-east-1" ]]; then
    aws s3api create-bucket \
      --bucket "$S3_BUCKET" \
      --region "$AWS_REGION" >/dev/null
  else
    aws s3api create-bucket \
      --bucket "$S3_BUCKET" \
      --region "$AWS_REGION" \
      --create-bucket-configuration "LocationConstraint=$AWS_REGION" >/dev/null
  fi
fi

aws s3api put-public-access-block \
  --bucket "$S3_BUCKET" \
  --public-access-block-configuration \
    'BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true'

if aws glue get-database --name "$GLUE_DATABASE" --region "$AWS_REGION" >/dev/null 2>&1; then
  echo "Glue database already exists: $GLUE_DATABASE"
else
  echo "Creating Glue database: $GLUE_DATABASE"
  aws glue create-database \
    --region "$AWS_REGION" \
    --database-input "{\"Name\":\"$GLUE_DATABASE\",\"Description\":\"MongoDB Atlas Stream Processing Iceberg demo\"}" >/dev/null
fi

cat > aws-values.txt <<EOF
AWS_REGION=$AWS_REGION
S3_BUCKET=$S3_BUCKET
GLUE_DATABASE=$GLUE_DATABASE
EOF

echo
echo "AWS bootstrap complete."
echo "----------------------------------------"
cat aws-values.txt
echo "----------------------------------------"
echo "Copy these values into ../../stream-processing/create_processor.js"
echo "Then configure Atlas Unified AWS Access and the S3 connection."
