#!/usr/bin/env python

"""TriG content-type support for Open Annotation."""

__author__ = 'Sampo Pyysalo'
__license__ = 'MIT'

import rdftools

# Short name for this format.
format_name = 'trig'

# The MIME types associated with this format.
mimetypes = ['application/trig']

def from_jsonld(data, options=None):
    """Render JSON-LD data into TriG.

    This is intended to be used as a mimerender render function
    (see http://mimerender.readthedocs.org/en/latest/).

    Args:
        data: dict containing JSON-LD data in expanded JSON-LD form
            (see http://www.w3.org/TR/json-ld/#expanded-document-form).
        options: dict of rendering options, or None for defaults.

    Returns:
        String representing the rendered data.
    """
    if options is None:
        options = {}

    return rdftools.from_jsonld(data, format='trig')

def to_jsonld(data, options=None):
    """Parse Trig data into JSON-LD.

    Args:
        data: string in Trig format.
        options: dict of parsing options, or None for defaults.

    Returns:
        dict containing JSON-LD data in expanded JSON-LD form
            (see http://www.w3.org/TR/json-ld/#expanded-document-form).
    """
    if options is None:
        options = {}

    return rdftools.to_jsonld(data, 'trig')
