#!/usr/bin/env python

"""RDF/XML content-type support for Open Annotation."""

__author__ = 'Sampo Pyysalo'
__license__ = 'MIT'

import rdfgraph

# Default values for rendering options
PRETTYPRINT_DEFAULT = True

def render(data, options=None):
    """Render JSON-LD data into RDF/XML.

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

    graph = rdfgraph.from_jsonld(data)

    prettyprint = options.get('prettyprint', PRETTYPRINT_DEFAULT)
    if prettyprint:
        return graph.serialize(format='pretty-xml')
    else:
        return graph.serialize(format='xml')
