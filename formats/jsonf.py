#!/usr/bin/env python

"""JSON content-type support for Open Annotation."""

__author__ = 'Sampo Pyysalo'
__license__ = 'MIT'

import json

# Default values for rendering options
PRETTYPRINT_DEFAULT = True
KEEPCONTEXT_DEFAULT = False

def render(data, options=None):
    """Render JSON-LD data into JSON string.

    This is intended to be used as a mimerender render function
    (see http://mimerender.readthedocs.org/en/latest/).

    If options['prettyprint'] is True, renders the data so that it is
    more easily readable by humans.
    If options['keepcontext'] is True, includes the JSON-LD @context
    in the JSON data if present.

    Args:
        data: dict containing JSON-LD data in expanded JSON-LD form
            (see http://www.w3.org/TR/json-ld/#expanded-document-form).
        options: dict of rendering options, or None for defaults.

    Returns:
        String representing the rendered data.
    """
    if options is None:
        options = {}

    # @context is not considered part of the JSON format
    keepcontext = options.get('keepcontext', KEEPCONTEXT_DEFAULT)
    if not keepcontext and '@context' in data:
        del data['@context']

    prettyprint = options.get('prettyprint', PRETTYPRINT_DEFAULT)
    if prettyprint:
        return json.dumps(data, indent=2, separators=(',', ': '))+'\n'
    else:
        return json.dumps(data)

def parse(data, options=None):
    """Parse JSON data into JSON-LD.

    Args:
        data: string in JSON format.
        options: dict of parsing options, or None for defaults.

    Returns:
        dict containing JSON-LD data in expanded JSON-LD form
            (see http://www.w3.org/TR/json-ld/#expanded-document-form).
    """
    if options is None:
        options = {}

    encoding = options.get('encoding')

    if encoding is None:
        json = json.loads(data)
    else:
        json = json.loads(data, encoding=encoding)

    # TODO: add context and expand
    return json
