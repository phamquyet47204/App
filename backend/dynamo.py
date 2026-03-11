import os
from decimal import Decimal
from functools import lru_cache

import boto3


DYNAMODB_REGION = os.getenv("DYNAMODB_REGION", os.getenv("AWS_REGION", "ap-southeast-1"))
TABLE_PREFIX = os.getenv("DYNAMODB_TABLE_PREFIX", "")


def tbl(name):
    return f"{TABLE_PREFIX}{name}"


@lru_cache(maxsize=1)
def dynamodb_resource():
    return boto3.resource("dynamodb", region_name=DYNAMODB_REGION)


def table(name):
    return dynamodb_resource().Table(tbl(name))


def to_native(value):
    if isinstance(value, Decimal):
        return int(value) if value % 1 == 0 else float(value)
    if isinstance(value, list):
        return [to_native(v) for v in value]
    if isinstance(value, dict):
        return {k: to_native(v) for k, v in value.items()}
    return value


def scan_all(table_obj, **kwargs):
    items = []
    response = table_obj.scan(**kwargs)
    items.extend(response.get("Items", []))
    while "LastEvaluatedKey" in response:
        response = table_obj.scan(ExclusiveStartKey=response["LastEvaluatedKey"], **kwargs)
        items.extend(response.get("Items", []))
    return items


def next_numeric_id(table_name):
    table_obj = table(table_name)
    items = scan_all(table_obj, ProjectionExpression="id")
    if not items:
        return 1
    return max(int(item["id"]) for item in items) + 1
