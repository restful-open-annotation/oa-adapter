#!/usr/bin/env python

"""Open Annotation adapter server."""

__author__ = 'Sampo Pyysalo'
__license__ = 'MIT'

import sys
import json

import flask

from render import render_resource

DEBUG = True

app = flask.Flask(__name__)

@app.route('/echo/', methods=['PUT', 'POST'])
@render_resource
def echo():
    """Echo back received data, possibly in a different representation."""
    # force for JSON-LD: application/ld+json is not recognized by
    # older Flask versions.
    data = flask.request.get_json(force=True)
    return { 'data': data }

def main(argv):
    app.run(debug=DEBUG)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
