#!/usr/bin/env python

"""Open Annotation adapter server."""

__author__ = 'Sampo Pyysalo'
__license__ = 'MIT'

import sys
import json

import flask

import oajson
import formatloader

from parse import make_parser
from render import make_renderer

DEBUG = True

app = flask.Flask(__name__)

# Create functions for parsing received data and rendering output data
# dynamically based on the available format modules.
formats = formatloader.load()
parse_data = make_parser(formats)
render_resource = make_renderer(formats)

def get_request_data(request):
    """Return (data, mimetype, charset) triple for Flask request."""
    mimetype = request.mimetype
    charset = request.mimetype_params.get('charset')
    data = request.get_data()
    return (data, mimetype, charset)

@app.route('/echo/', methods=['PUT', 'POST'])
@render_resource
def echo():
    """Echo back received data, possibly in a different representation."""
    data, mimetype, charset = get_request_data(flask.request)
    data = parse_data(data, mimetype, charset)
    # TODO: check in which cases expansion is required.
    data = oajson.expand(data, base=flask.request.base_url)
    return { 'data': data }

def main(argv):
    app.run(debug=DEBUG)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
