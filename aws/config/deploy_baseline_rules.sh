#!/usr/bin/env bash

set -u

REGION="${AWS_REGION:-us-east-1}"
PREFIX="baseline"

usage() {
  cat <<EOF
Usage: $(basename "$0") [options]

Create/update a baseline set of AWS Config managed rules for ECS/Lambda/RDS workloads.

Options:
  --region <region>   AWS region (default: us-east-1 or AWS_REGION env)
  --prefix <name>     Config rule name prefix (default: baseline)
  -h, --help          Show help

Example:
  ./deploy_baseline_rules.sh --region us-east-1 --prefix prod
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --region)
      REGION="$2"
      shift 2
      ;;
    --prefix)
      PREFIX="$2"
      shift 2
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

if ! command -v aws >/dev/null 2>&1; then
  echo "AWS CLI is not installed or not in PATH." >&2
  exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
  echo "python3 is required for generating JSON payload." >&2
  exit 1
fi

TMP_DIR="$(mktemp -d)"
SUCCESS=0
FAILED=0

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

create_rule_json() {
  local output_file="$1"
  local name="$2"
  local identifier="$3"
  local description="$4"
  local input_parameters_json="${5:-}"

  if [[ -n "$input_parameters_json" ]]; then
    python3 - "$output_file" "$name" "$identifier" "$description" "$input_parameters_json" <<'PY'
import json
import sys

output_file, name, identifier, description, input_parameters_json = sys.argv[1:6]
data = {
    "ConfigRuleName": name,
    "Description": description,
    "Source": {
        "Owner": "AWS",
        "SourceIdentifier": identifier
    },
    "InputParameters": input_parameters_json,
}

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
PY
  else
    python3 - "$output_file" "$name" "$identifier" "$description" <<'PY'
import json
import sys

output_file, name, identifier, description = sys.argv[1:5]
data = {
    "ConfigRuleName": name,
    "Description": description,
    "Source": {
        "Owner": "AWS",
        "SourceIdentifier": identifier
    }
}

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)
PY
  fi
}

put_rule() {
  local short_name="$1"
  local identifier="$2"
  local description="$3"
  local input_parameters_json="${4:-}"
  local rule_name="${PREFIX}-${short_name}"
  local payload_file="${TMP_DIR}/${rule_name}.json"

  create_rule_json "$payload_file" "$rule_name" "$identifier" "$description" "$input_parameters_json"

  if aws configservice put-config-rule --region "$REGION" --config-rule "file://${payload_file}" >/dev/null 2>&1; then
    SUCCESS=$((SUCCESS + 1))
    echo "[OK] ${rule_name} (${identifier})"
  else
    FAILED=$((FAILED + 1))
    echo "[FAIL] ${rule_name} (${identifier})"
  fi
}

echo "Deploying managed rules in region ${REGION} with prefix ${PREFIX}..."

put_rule "cloudtrail-enabled" "CLOUD_TRAIL_ENABLED" "Ensure CloudTrail is enabled"
put_rule "root-mfa-enabled" "ROOT_ACCOUNT_MFA_ENABLED" "Ensure root account has MFA enabled"
put_rule "iam-user-mfa-enabled" "IAM_USER_MFA_ENABLED" "Ensure IAM users have MFA enabled"

put_rule "s3-public-read-prohibited" "S3_BUCKET_PUBLIC_READ_PROHIBITED" "Ensure S3 buckets block public read"
put_rule "s3-public-write-prohibited" "S3_BUCKET_PUBLIC_WRITE_PROHIBITED" "Ensure S3 buckets block public write"
put_rule "s3-sse-enabled" "S3_BUCKET_SERVER_SIDE_ENCRYPTION_ENABLED" "Ensure S3 buckets use server-side encryption"

put_rule "rds-storage-encrypted" "RDS_STORAGE_ENCRYPTED" "Ensure RDS storage encryption is enabled"
put_rule "rds-not-public" "RDS_INSTANCE_PUBLIC_ACCESS_CHECK" "Ensure RDS instances are not publicly accessible"

put_rule "incoming-ssh-disabled" "INCOMING_SSH_DISABLED" "Ensure SSH is not open to 0.0.0.0/0"
put_rule "default-sg-closed" "VPC_DEFAULT_SECURITY_GROUP_CLOSED" "Ensure default security group has no ingress/egress"

put_rule "ecr-scan-enabled" "ECR_PRIVATE_IMAGE_SCANNING_ENABLED" "Ensure ECR image scanning is enabled"
put_rule "ecs-nonprivileged" "ECS_CONTAINERS_NONPRIVILEGED" "Ensure ECS containers do not run in privileged mode"

put_rule "lambda-public-access-prohibited" "LAMBDA_FUNCTION_PUBLIC_ACCESS_PROHIBITED" "Ensure Lambda public access is prohibited"
put_rule "lambda-inside-vpc" "LAMBDA_INSIDE_VPC" "Ensure Lambda functions run inside VPC"

put_rule "required-tags" "REQUIRED_TAGS" "Ensure required tags exist" '{"tag1Key":"Environment","tag2Key":"Owner","tag3Key":"Project"}'

echo
echo "Completed: ${SUCCESS} success, ${FAILED} failed."
if [[ "$FAILED" -gt 0 ]]; then
  echo "Some rules failed. Common reasons: unsupported rule in region, missing prerequisite service, or IAM permissions."
fi

echo "List current rules:"
echo "  aws configservice describe-config-rules --region ${REGION} --query 'ConfigRules[].ConfigRuleName' --output table"
