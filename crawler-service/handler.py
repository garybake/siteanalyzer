try:
    import unzip_requirements
except ImportError:
    pass

import os
import json
import logging
import uuid
from urllib.parse import urlparse

import boto3
import requests

import image_parser
import db

logger = logging.getLogger('crawler')


def shortid():
    return str(uuid.uuid4())[:8]


def create_unique_domain(domain):
    parsed = urlparse(domain)
    domain = shortid() + "." + parsed.hostname
    return domain.lower()


def download_site(body, context):
    """
    Get Images list
    Download images to S3
    Create db entry
    Send notification
    """
    bucket_name = os.getenv('GBIMAGECLASSIFIER_BUCKET')

    domain = body['msg']['url']
    unique_domain = create_unique_domain(domain)

    images = image_parser.parse_domain(domain)
    images_data = upload_images_to_s3(domain, images, bucket_name, unique_domain)
    db.create_parse_entry(unique_domain, domain, bucket_name, images_data)
    notify_analysis(unique_domain, context)


def upload_images_to_s3(domain, images, bucket, unique_domain):
    s3 = boto3.resource('s3')
    images_data = []

    # TODO parallize
    for image in images:
        image_url = domain + "/" + image
        # TODO not unique enough
        s3_filename = unique_domain + "/" + image.replace("/", "_")

        req = requests.get(image_url, stream=True)
        file_object_from_req = req.raw
        req_data = file_object_from_req.read()

        logger.warn("Uploading: {}".format(s3_filename))
        s3.Bucket(bucket).put_object(Key=s3_filename, Body=req_data)
        images_data.append({
            "ImageUrl": image_url,
            "S3Url": s3_filename
        })

    return images_data


def notify_analysis(unique_domain, context):
    sqs = boto3.client('sqs')

    account_id = os.getenv('AWS_ACCOUNT_ID')

    aws_region = os.getenv('AWS_DEFAULT_REGION')
    sqs_queue = os.getenv('GBIMAGECLASSIFIER_ANALYSISQUEUE')
    queue_url = f"https://sqs.{aws_region}.amazonaws.com/{account_id}/{sqs_queue}"

    try:
        response = sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=(
                json.dumps({"action": "analyze", "msg": {"domain": unique_domain}})
            )
        )
    except Exception as e:
        logger.error(f"Failed to send {unique_domain} to analysis queue")
        logger.error(queue_url)


def crawl_sites(event, context):
    for record in event['Records']:
        try:
            body = json.loads(record['body'])
            action = body['action']
            if action == 'download':
                download_site(body, context)

        except json.decoder.JSONDecodeError as e:
            logger.error("Parse error: {}".format(e))
        except KeyError as e:
            logger.error("Malformed message: {}".format(e))


# if __name__ == "__main__":
#     # event = {
#     #     "Records": [
#     #         {"body": '{"action": "download", "msg": {"url": "http://garybake.com"}}'},
#     #         {"body": '{"action": "download", "msg": {"url": "https://www.google.com"}}'}
#     #     ]
#     # }

#     event = {
#         "Records": [
#             {"body": '{"action": "download", "msg": {"url": "http://www.garybake.com"}}'}
#         ]
#     }

#     crawl_sites(event, "")
