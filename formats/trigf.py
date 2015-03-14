#!/usr/bin/env python

"""TriG content-type support for Open Annotation."""

__author__ = 'Sampo Pyysalo'
__license__ = 'MIT'

import rdfgraph

def render(data, options=None):
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

    graph = rdfgraph.from_jsonld(data)

    return graph.serialize(format='trig')

def parse(data, options=None):
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

    return rdfgraph.to_jsonld(data, 'trig')
