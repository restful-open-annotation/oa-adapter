#!/usr/bin/env python

"""JSON content-type support for Open Annotation."""

__author__ = 'Sampo Pyysalo'
__license__ = 'MIT'

import json

# Default values for rendering options
PRETTYPRINT_DEFAULT = True

def render(data, options=None):
    """Render JSON-LD data into JSON string.

    This is intended to be used as a mimerender render function
    (see http://mimerender.readthedocs.org/en/latest/).

    If options['prettyprint'] is True, renders the data so that it is
    more easily readable by humans.

    Args:
        data: dict containing JSON-LD data in expanded JSON-LD form
            (see http://www.w3.org/TR/json-ld/#expanded-document-form).
        options: dict of rendering options, or None for defaults.

    Returns:
        String representing the rendered data.
    """
    # TODO: consider (optionally?) dropping @context and other JSON-LD
    # specific material.
    if options is None:
        options = {}

    prettyprint = options.get('prettyprint', PRETTYPRINT_DEFAULT)
    if prettyprint:
        return json.dumps(data, indent=2, separators=(',', ': '))+'\n'
    else:
        return json.dumps(data)
