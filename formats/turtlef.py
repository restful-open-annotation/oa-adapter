#!/usr/bin/env python

"""Turtle content-type support for Open Annotation."""

__author__ = 'Sampo Pyysalo'
__license__ = 'MIT'

import rdfgraph

def render(data, options=None):
    """Render JSON-LD data into Turtle.

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

    # TODO: rdflib Turtle serialization silently discards the fourth
    # value in any quad. Check for quads and at least warn if any
    # found.
    return graph.serialize(format='turtle')
