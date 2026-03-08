#!/usr/bin/env bash

set -euo pipefail

REGION="${AWS_REGION:-us-east-1}"
BUCKET_NAME=""
SNS_TOPIC_ARN=""
INCLUDE_GLOBAL="true"

usage() {
  cat <<EOF
Usage: $(basename "$0") --bucket <s3-bucket-name> [options]

Bootstrap AWS Config in one region:
  - create/validate S3 bucket for Config snapshots
  - create service-linked role for AWS Config
  - create delivery channel + configuration recorder
  - start recorder

Options:
  --bucket <name>        Required. S3 bucket used by AWS Config.
  --region <region>      AWS region (default: us-east-1 or AWS_REGION env).
  --sns-topic-arn <arn>  Optional SNS topic ARN for Config notifications.
  --no-global            Do not include IAM/global resources in recorder.
  -h, --help             Show help.

Example:
  ./setup_config.sh --bucket my-org-config-logs --region us-east-1
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --bucket)
      BUCKET_NAME="$2"
      shift 2
      ;;
    --region)
      REGION="$2"
      shift 2
      ;;
    --sns-topic-arn)
      SNS_TOPIC_ARN="$2"
      shift 2
      ;;
    --no-global)
      INCLUDE_GLOBAL="false"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage
      exit 1
      ;;
  esac
done

if [[ -z "$BUCKET_NAME" ]]; then
  echo "Missing required argument: --bucket" >&2
  usage
  exit 1
fi

if ! command -v aws >/dev/null 2>&1; then
  echo "AWS CLI is not installed or not in PATH." >&2
  exit 1
fi

ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text)"
CONFIG_ROLE_ARN="arn:aws:iam::${ACCOUNT_ID}:role/aws-service-role/config.amazonaws.com/AWSServiceRoleForConfig"

echo "[1/6] Ensuring S3 bucket exists: ${BUCKET_NAME} (${REGION})"
if ! aws s3api head-bucket --bucket "$BUCKET_NAME" 2>/dev/null; then
  if [[ "$REGION" == "us-east-1" ]]; then
    aws s3api create-bucket --bucket "$BUCKET_NAME"
  else
    aws s3api create-bucket \
      --bucket "$BUCKET_NAME" \
      --create-bucket-configuration "LocationConstraint=${REGION}"
  fi
fi

aws s3api put-bucket-versioning \
  --bucket "$BUCKET_NAME" \
  --versioning-configuration Status=Enabled

aws s3api put-bucket-encryption \
  --bucket "$BUCKET_NAME" \
  --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'

echo "[2/6] Applying bucket policy for AWS Config delivery"
POLICY_FILE="$(mktemp)"
cat > "$POLICY_FILE" <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AWSConfigBucketPermissionsCheck",
      "Effect": "Allow",
      "Principal": {"Service": "config.amazonaws.com"},
      "Action": "s3:GetBucketAcl",
      "Resource": "arn:aws:s3:::${BUCKET_NAME}",
      "Condition": {"StringEquals": {"AWS:SourceAccount": "${ACCOUNT_ID}"}}
    },
    {
      "Sid": "AWSConfigBucketExistenceCheck",
      "Effect": "Allow",
      "Principal": {"Service": "config.amazonaws.com"},
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::${BUCKET_NAME}",
      "Condition": {"StringEquals": {"AWS:SourceAccount": "${ACCOUNT_ID}"}}
    },
    {
      "Sid": "AWSConfigBucketDelivery",
      "Effect": "Allow",
      "Principal": {"Service": "config.amazonaws.com"},
      "Action": "s3:PutObject",
      "Resource": "arn:aws:s3:::${BUCKET_NAME}/AWSLogs/${ACCOUNT_ID}/Config/*",
      "Condition": {
        "StringEquals": {
          "AWS:SourceAccount": "${ACCOUNT_ID}",
          "s3:x-amz-acl": "bucket-owner-full-control"
        }
      }
    }
  ]
}
EOF
aws s3api put-bucket-policy --bucket "$BUCKET_NAME" --policy "file://${POLICY_FILE}"
rm -f "$POLICY_FILE"

echo "[3/6] Ensuring service-linked role for AWS Config"
aws iam create-service-linked-role --aws-service-name config.amazonaws.com >/dev/null 2>&1 || true

echo "[4/6] Creating/updating configuration recorder"
aws configservice put-configuration-recorder \
  --configuration-recorder "name=default,roleARN=${CONFIG_ROLE_ARN},recordingGroup={allSupported=true,includeGlobalResourceTypes=${INCLUDE_GLOBAL}}" \
  --region "$REGION"

echo "[5/6] Creating/updating delivery channel"
if [[ -n "$SNS_TOPIC_ARN" ]]; then
  aws configservice put-delivery-channel \
    --delivery-channel "name=default,s3BucketName=${BUCKET_NAME},snsTopicARN=${SNS_TOPIC_ARN}" \
    --region "$REGION"
else
  aws configservice put-delivery-channel \
    --delivery-channel "name=default,s3BucketName=${BUCKET_NAME}" \
    --region "$REGION"
fi

echo "[6/6] Starting recorder"
aws configservice start-configuration-recorder \
  --configuration-recorder-name default \
  --region "$REGION"

echo
echo "AWS Config bootstrap completed."
echo "Verify with:"
echo "  aws configservice describe-configuration-recorders --region ${REGION}"
echo "  aws configservice describe-delivery-channels --region ${REGION}"
