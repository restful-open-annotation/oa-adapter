#!/usr/bin/env python

"""Notation3 content-type support for Open Annotation."""

__author__ = 'Sampo Pyysalo'
__license__ = 'MIT'

import rdftools

# Short name for this format.
format_name = 'n3'

# The MIME types associated with this format.
# Note: "charset" is not an error: "This MIME type is used with a
# charset parameter: the encoding is always utf-8. [...] This is
# because the default encoding for types in the text/* tree is ASCII
# (http://www.w3.org/TeamSubmission/n3/).
mimetypes = ['text/n3; charset=utf-8', 'text/n3']

def from_jsonld(data, options=None):
    """Render JSON-LD data into N3 string.

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

    # TODO: rdflib N3 serialization silently discards the fourth
    # value in any quad. Check for quads and at least warn if any
    # found.
    return rdftools.from_jsonld(data, format='n3')

def to_jsonld(data, options=None):
    """Parse N3 data into JSON-LD.

    Args:
        data: string in N3 format.
        options: dict of parsing options, or None for defaults.

    Returns:
        dict containing JSON-LD data in expanded JSON-LD form
            (see http://www.w3.org/TR/json-ld/#expanded-document-form).
    """
    if options is None:
        options = {}

    return rdftools.to_jsonld(data, 'n3')
