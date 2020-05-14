import os
import logging

import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.conditions import Key


logger = logging.getLogger('ui')
dynamodb = boto3.resource('dynamodb')


def all_urls():
    table = dynamodb.Table(os.getenv('GBIMAGECLASSIFIER_TABLE'))

    try:
        response = table.scan()
        return response['Items']
    except ClientError as e:
        logger.error(e.response['Error']['Message'])


def url_data(pageid):
    table = dynamodb.Table(os.getenv('GBIMAGECLASSIFIER_TABLE'))

    try:
        response = table.query(
            KeyConditionExpression=Key('PageID').eq(pageid)
        )
        return response['Items'][0]
    except ClientError as e:
        logger.error(e.response['Error']['Message'])
    except IndexError as e:
        logger.error(f"PageID {pageid} not found")
        return None


if __name__ == "__main__":
    urls = all_urls()
    for url in urls:
        print(url)
