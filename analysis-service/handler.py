try:
    import unzip_requirements
except ImportError:
    pass

import json
import logging
import os

import db
import image_analysis

logger = logging.getLogger('analysis')


def analyse_single_site(body, context):
    domain = body['msg']['domain']
    sites_details = db.get_site_details(domain)
    images = sites_details.get('Images', [])
    bucket_name = sites_details.get('Bucket', os.getenv('GBIMAGECLASSIFIER_BUCKET'))
    for image in images:
        image_contents = image_analysis.analyze_image(bucket_name, image)
        image['analysis'] = image_contents

    db.update_site_details(sites_details)


def analyse_sites(event, context):
    for record in event['Records']:
        try:
            body = json.loads(record['body'])
            action = body['action']
            if action == 'analyze':
                analyse_single_site(body, context)

        except json.decoder.JSONDecodeError as e:
            logger.error("Parse error: {}".format(e))
        except KeyError as e:
            logger.error("Malformed message: {}".format(e))


# if __name__ == "__main__":

#     event = {
#         "Records": [
#             {"body": '{"action": "analyze", "msg": {"domain": "c2e97f28.www.garybake.com"}}'}
#         ]
#     }

#     analyse_sites(event, "")
