#!/usr/bin/env python

"""JSON-LD content-type support for Open Annotation."""

__author__ = 'Sampo Pyysalo'
__license__ = 'MIT'

import json

# Default values for rendering options
PRETTYPRINT_DEFAULT = True

def from_jsonld(data, options=None):
    """Render JSON-LD data into string.

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
    if options is None:
        options = {}

    prettyprint = options.get('prettyprint', PRETTYPRINT_DEFAULT)
    if prettyprint:
        return json.dumps(data, indent=2, separators=(',', ': '))+'\n'
    else:
        return json.dumps(data)

def to_jsonld(data, options=None):
    """Parse JSON-LD data.

    Args:
        data: string in JSON-LD format.
        options: dict of parsing options, or None for defaults.

    Returns:
        dict containing JSON-LD data in expanded JSON-LD form
            (see http://www.w3.org/TR/json-ld/#expanded-document-form).
    """
    if options is None:
        options = {}

    encoding = options.get('encoding')

    if encoding is None:
        jsonld = json.loads(data)
    else:
        jsonld = json.loads(data, encoding=encoding)

    # TODO: expand
    return jsonld
