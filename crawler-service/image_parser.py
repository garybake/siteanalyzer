# Functions to parse a web page and return a list of images
import logging

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger('crawler')


def request_page(domain):
    user_agent = {'User-agent': 'Mozilla/5.0'}
    req = requests.get(domain, headers=user_agent)
    if req.status_code == 200:
        return req.content
    return


def get_images(content):
    return [tag["src"] for tag in content.findAll('img')]


def parse_domain(domain):
    logger.warn("Requesting: " + domain)
    content = BeautifulSoup(request_page(domain), 'html.parser')
    images = get_images(content)
    return images
