#!/usr/bin/env python

"""N-Quads content-type support for Open Annotation."""

__author__ = 'Sampo Pyysalo'
__license__ = 'MIT'

from pyld import jsonld

def from_jsonld(data, options=None):
    """Render JSON-LD data into N-Quads.

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

    return jsonld.to_rdf(data, { 'format': 'application/nquads' })

def to_jsonld(data, options=None):
    """Parse N-Quads data into JSON-LD.

    Args:
        data: string in N-Quads format.
        options: dict of parsing options, or None for defaults.

    Returns:
        dict containing JSON-LD data in expanded JSON-LD form
            (see http://www.w3.org/TR/json-ld/#expanded-document-form).
    """
    if options is None:
        options = {}

    return jsonld.from_rdf(data, { 'format': 'application/nquads' })
