#!/usr/bin/env python

"""N-Triples content-type support for Open Annotation."""

__author__ = 'Sampo Pyysalo'
__license__ = 'MIT'

import rdftools

def render(data, options=None):
    """Render JSON-LD data into N-Triples.

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

    # TODO: rdflib N-Triples serialization silently discards the
    # fourth value in any quad. Check for quads and at least warn if
    # any found.
    return rdftools.from_jsonld(data, format='nt')

def parse(data, options=None):
    """Parse N-Triples data into JSON-LD.

    Args:
        data: string in N-Triples format.
        options: dict of parsing options, or None for defaults.

    Returns:
        dict containing JSON-LD data in expanded JSON-LD form
            (see http://www.w3.org/TR/json-ld/#expanded-document-form).
    """
    if options is None:
        options = {}

    return rdftools.to_jsonld(data, 'nt')
