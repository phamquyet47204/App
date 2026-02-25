import json
import os

import boto3
from botocore.exceptions import ClientError


SES_REGION = os.getenv("SES_REGION", "us-east-1")
FROM_EMAIL = os.getenv("FROM_EMAIL")
SOURCE_ARN = os.getenv("SES_SOURCE_ARN")

ses = boto3.client("ses", region_name=SES_REGION)


def lambda_handler(event, context):
    if not FROM_EMAIL or not SOURCE_ARN:
        return {
            "statusCode": 500,
            "body": json.dumps(
                {
                    "detail": "Missing lambda environment variables: FROM_EMAIL or SES_SOURCE_ARN",
                }
            ),
        }

    to_email = event.get("to")
    subject = event.get("subject", "Thông báo")
    text = event.get("text", "")
    html = event.get("html")

    if not to_email:
        return {
            "statusCode": 400,
            "body": json.dumps({"detail": "Missing required field: to"}),
        }

    body = {"Text": {"Data": text or ""}}
    if html:
        body["Html"] = {"Data": html}

    try:
        response = ses.send_email(
            Source=FROM_EMAIL,
            SourceArn=SOURCE_ARN,
            Destination={"ToAddresses": [to_email]},
            Message={
                "Subject": {"Data": subject, "Charset": "UTF-8"},
                "Body": body,
            },
        )
    except ClientError as error:
        return {
            "statusCode": 500,
            "body": json.dumps(
                {
                    "detail": "SES send failed",
                    "error": error.response.get("Error", {}),
                }
            ),
        }

    return {
        "statusCode": 200,
        "body": json.dumps({"message_id": response["MessageId"]}),
    }
