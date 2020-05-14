import json
import decimal
import logging

import db
import crawler_queue

logger = logging.getLogger('crawler')


class DecimalEncoder(json.JSONEncoder):
    # https://stackoverflow.com/questions/43678946/python-3-x-cannot-serialize-decimal-to-json
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return float(o)
        return super(DecimalEncoder, self).default(o)


def list_urls(event, context):
    urls = db.all_urls()
    response = {
        "statusCode": 200,
        "body": json.dumps(urls, cls=DecimalEncoder)
    }
    return response


def list_images(event, context):
    pageid = event["queryStringParameters"]["pageid"]
    page_data = db.url_data(pageid)

    response = {
        "statusCode": 200,
        "body": json.dumps(page_data, cls=DecimalEncoder)
    }
    return response


def analyze_url(event, context):
    logger.error(event['body'])
    payload = json.loads(event["body"])
    logger.error(payload)
    url = payload["url"]
    logger.error(url)

    # send request to queue
    queue_resp = crawler_queue.notify(url)
    response = {
        "statusCode": 200,
        "body": json.dumps(queue_resp, cls=DecimalEncoder)
    }
    return response


if __name__ == "__main__":
    # event = {
    #     "queryStringParameters": {
    #         "pageid": "a611b823.www.garybake.com"
    #     }
    # }
    # response = list_images(event, "")
    # print(response)

    event = {
        "queryStringParameters": {
            "url": "https://www.wpbeginner.com/wp-themes/how-to-create-a-custom-homepage-in-wordpress/"
        }
    }
    response = analyze_url(event, "")
    print(response)
