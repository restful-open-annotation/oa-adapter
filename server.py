#!/usr/bin/env python

"""Open Annotation adapter server."""

__author__ = 'Sampo Pyysalo'
__license__ = 'MIT'

import sys
import json

import flask

import oajson
import formatloader
import restoaclient
import jsonldproxy
import tools

from parse import make_parser
from render import make_renderer

DEBUG = True

app = flask.Flask(__name__)

# Create functions for parsing received data and rendering output data
# dynamically based on the available format modules.
formats = formatloader.load()
parse_data = make_parser(formats)
render_resource = make_renderer(formats)

@app.route('/echo/', methods=['PUT', 'POST'])
@render_resource
def echo():
    """Echo back received data, possibly in a different representation."""
    data, mimetype, charset = tools.get_request_data(flask.request)
    data = parse_data(data, mimetype, charset)
    # TODO: check in which cases expansion is required.
    data = oajson.expand(data, base=flask.request.base_url)
    return { 'data': data }

@app.route('/proxy/<path:url>')
@render_resource
def proxy(url):
    """Mediate communication with other server."""
    data, mimetype = restoaclient.get(url)
    # TODO: parse mimetype properly
    if 'text/html' in mimetype:
        # Don't try to parse HTLM, but just pass it through.
        return { 'data': data, 'options': { 'passthrough': True } }
    else:
        data = oajson.expand(data, base=tools.base_url(url))
        # rewrite URLs in data so that they pass through this proxy.
        proxyurl = flask.url_for('proxy', url='')
        data = jsonldproxy.rewrite_urls(data, proxyurl)
        return { 'data': data }

def main(argv):
    app.run(debug=DEBUG)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
