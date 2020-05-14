import os
import logging
import json

import boto3

logger = logging.getLogger('crawler')


def notify(url):
    sqs = boto3.client('sqs')

    account_id = os.getenv('AWS_ACCOUNT_ID')
    aws_region = os.getenv('AWS_DEFAULT_REGION')
    sqs_queue = os.getenv('GBIMAGECLASSIFIER_CRAWLERQUEUE')

    queue_url = f"https://sqs.{aws_region}.amazonaws.com/{account_id}/{sqs_queue}"

    try:
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=(
                json.dumps({"action": "download", "msg": {"url": url}})
            )
        )
        return response
    except Exception as e:
        logger.error(f"Failed to send {url} to analysis queue")
        logger.error(queue_url)
        logger.error(e)
