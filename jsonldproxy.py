#!/usr/bin/env python

"""Support for proxying JSON-LD data."""

__author__ = 'Sampo Pyysalo'
__license__ = 'MIT'

import urllib

def rewrite_urls(data, proxy_url):
    """Rewrite URLs in JSON-LD data to pass through proxy."""
    if isinstance(data, dict):
        data = _rewrite_dict_urls(data, proxy_url)
    elif isinstance(data, list):
        data = _rewrite_list_urls(data, proxy_url)
    else:
        pass
    return data

def _rewrite_dict_urls(dict_, proxy_url):
    if '@id' in dict_:
        dict_['@id'] = proxy_url + urllib.quote(dict_['@id'])
    for key, value in dict_.iteritems():
        if key == '@id':
            continue
        rewrite_urls(value, proxy_url)
    return dict_

def _rewrite_list_urls(list_, proxy_url):
    for item in list_:
        rewrite_urls(item, proxy_url)
    return list_
