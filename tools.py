#!/usr/bin/env python

"""Miscellaneous support methods."""

__author__ = 'Sampo Pyysalo'
__license__ = 'MIT'

import urlparse

def get_request_data(request):
    """Return (data, mimetype, charset) triple for Flask request."""
    mimetype = request.mimetype
    charset = request.mimetype_params.get('charset')
    data = request.get_data()
    return (data, mimetype, charset)

def base_url(url):
    """Returns the "base URL" for the given URL."""
    # TODO: avoid this ugly hack
    magic_string = '1234567890'
    joined = urlparse.urljoin(url, magic_string)
    return joined.replace(magic_string, '')
