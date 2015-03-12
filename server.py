#!/usr/bin/env python

"""Open Annotation adapter server."""

__author__ = 'Sampo Pyysalo'
__license__ = 'MIT'

import sys
import json

import flask

import oajson

from render import render_resource

DEBUG = True

app = flask.Flask(__name__)

def get_content_type(request):
    """Return Content-Type from Flask request."""
    return reques.mimetype

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

@app.route('/echo/', methods=['PUT', 'POST'])
@render_resource
def echo():
    """Echo back received data, possibly in a different representation."""
    data = get_json(flask.request, True)
    # Output rendering functions expect expanded JSON-LD
    # TODO: provide a way for the client to assign base
    data = oajson.expand(data, base=flask.request.base_url)
    return { 'data': data }

def main(argv):
    app.run(debug=DEBUG)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
