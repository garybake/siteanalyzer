
import os
import logging

import boto3

logger = logging.getLogger('crawler')


def create_parse_entry(pageid, url, bucket, images):
    dynamodb = boto3.resource('dynamodb')
    dynamodb_table = os.getenv('GBIMAGECLASSIFIER_TABLE')

    entry = {
      "PageID": pageid,
      "Url": url,
      "Bucket": bucket,
      "IsAnalysed": False,
      "Images": images
    }

    table = dynamodb.Table(dynamodb_table)
    try:
        response = table.put_item(Item=entry)

        if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
            logging.warn("Database entry created for {}".format(pageid))
        else:
            logging.error("Failed to create database entry for {}".format(pageid))
    except Exception as e:
        logging.error("Failed to log entry to db")
        logging.error(entry)
        logging.error(e)


# if __name__ == "__main__":
#     # create_dynamodb_entry()
#     url = "http://garybake.com"
#     read_entry(url)
