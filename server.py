#!/usr/bin/env python

"""Open Annotation adapter server."""

__author__ = 'Sampo Pyysalo'
__license__ = 'MIT'

import sys
import json

import flask

import oajson

from parse import parse_data
from render import render_resource

DEBUG = True

app = flask.Flask(__name__)

def get_json(request, abort_on_failure=True):
    """Return JSON from Flask request."""
    try:
        # force for JSON-LD: application/ld+json is not recognized by
        # older Flask versions.
        return flask.request.get_json(force=True)
    except Exception, e:
        if abort_on_failure:
            # TODO: attach a JSON structure describing the error.
            flask.abort(400, 'failed to load JSON (Content-Type: %s)' %
                        flask.request.mimetype)
        else:
            raise

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
