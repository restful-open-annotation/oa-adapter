#!/usr/bin/env python

"""Support for parsing various MIME types into JSON-LD."""

__author__ = 'Sampo Pyysalo'
__license__ = 'MIT'

import formats.jsonf
import formats.jsonldf
import formats.n3f
import formats.ntf
import formats.nquadsf
import formats.rdfxmlf
import formats.trigf
import formats.trixf
import formats.turtlef

# TODO: unify with mimetype data in rdfgraph.py
mimetype_to_parse_function = {
    'application/ld+json': formats.jsonldf.parse,
    'application/n-triples': formats.ntf.parse,
    'application/n-quads': formats.nquadsf.parse,
    'text/n3': formats.n3f.parse,
    'application/trig': formats.trigf.parse,
    'application/trix': formats.trixf.parse,
    'application/rdf+xml': formats.rdfxmlf.parse,
    'text/turtle': formats.turtlef.parse,
}

def parse_data(data, mimetype=None, charset=None):
    """Parse data into JSON-LD."""

    options = { 'encoding': charset }

    parse_function = mimetype_to_parse_function.get(mimetype)

    if not parse_function:
        raise NotImplementedError('not implemented: parsing %s' % mimetype)
    else:
        return parse_function(data, options)
