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
    'application/ld+json': formats.jsonldf.to_jsonld,
    'application/n-triples': formats.ntf.to_jsonld,
    'application/n-quads': formats.nquadsf.to_jsonld,
    'text/n3': formats.n3f.to_jsonld,
    'application/trig': formats.trigf.to_jsonld,
    'application/trix': formats.trixf.to_jsonld,
    'application/rdf+xml': formats.rdfxmlf.to_jsonld,
    'text/turtle': formats.turtlef.to_jsonld,
}

def parse_data(data, mimetype=None, charset=None):
    """Parse data into JSON-LD."""

    options = { 'encoding': charset }

    parse_function = mimetype_to_parse_function.get(mimetype)

    if not parse_function:
        raise NotImplementedError('not implemented: parsing %s' % mimetype)
    else:
        return parse_function(data, options)
