#!/usr/bin/env python

"""RESTful Open Annotation client."""

import requests

from server import parse_data

def get(url):
    """Get RESTful annotations from given URL.

    Returns:
        response data in JSON-LD format.
    """
    headers = { 'Accept': 'application/ld+json' }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    # Note: Requests resolves encoding when response.text is accessed,
    # so parse_data doesn't need to address encoding.
    data, mimetype = response.text, response.headers.get('Content-Type')
    return parse_data(data, mimetype), mimetype
