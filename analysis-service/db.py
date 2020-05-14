import os
import json
import logging

import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key

logger = logging.getLogger('analysis')


def update_site_details(site_details):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.getenv('GBIMAGECLASSIFIER_TABLE'))

    page_id = site_details.get("PageID")
    image_details = site_details.get("Images")

    response = table.update_item(
        Key={'PageID': page_id},
        UpdateExpression="set Images=:i, IsAnalysed=:s",
        ExpressionAttributeValues={
            ':i': image_details,
            ':s': True
        },
        ReturnValues="UPDATED_NEW"
    )

    logger.error(f"{site_details} updated in dynamodb")


def get_site_details(domain):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(os.getenv('GBIMAGECLASSIFIER_TABLE'))

    try:
        response = table.get_item(
            Key={"PageID": domain}
        )
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
    else:
        item = response.get('Item')
        if item:
            logger.warn(f"GetItem succeeded: {domain}")
            # logger.warn(json.dumps(item, indent=4))
            return item
        else:
            logger.warn("WebPage not found: {}".format(domain))
            return None


if __name__ == "__main__":
    domain = "fec9ae39.garybake.com"
    get_site_details(domain)
