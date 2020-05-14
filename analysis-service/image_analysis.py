import os
import logging
from decimal import Decimal

import boto3
import botocore

logger = logging.getLogger('analysis')


def clean_detect_response(response):
    images = response.get('Labels', [])

    return [{'Name': i['Name'], 'Confidence': Decimal(str(i['Confidence']))} for i in images]


def analyze_image(bucket_name, image):
    # TODO handle more image types
    # TODO remove params from image urls

    # if image['ImageUrl'].endswith(".png"):
    #     logger.error(f"Failed to analyze, Invalid image format: {image['ImageUrl']}")
    #     return []

    logger.error(f"analyzing image: {image}")
    rekognition = boto3.client('rekognition')

    image_url = image['S3Url']
    try:
        response = rekognition.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': image_url,
                },
            },
            MaxLabels=10,
        )
    # except botocore.errorfactory.InvalidImageFormatException as e:
    except Exception as e:
        logger.error(f"Failed to analyze, Invalid image format: {image['ImageUrl']}")
        return []

    return clean_detect_response(response)


# if __name__ == "__main__":
#     bucket_name = os.getenv('GBIMAGECLASSIFIER_BUCKET', "gbimageclassifier_noenv")
#     image = {'ImageUrl': 'http://garybake.com/images/gameboy/gameboy.jpg', 'S3Url': 'fec9ae39.garybake.com/images_rl_mario-learning.jpg'}

#     labels = analyze_image_mock(bucket_name, image)
#     print(labels)
