#!/usr/bin/env python

"""Support for rendering JSON-LD into various MIME types."""

__author__ = 'Sampo Pyysalo'
__license__ = 'MIT'

import json

import mimerender
flaskmimerender = mimerender.FlaskMimeRender()

import formats.jsonf
import formats.jsonldf
import formats.n3f
import formats.ntf
import formats.nquadsf
import formats.rdfxmlf
import formats.trigf
import formats.trixf
import formats.turtlef

from formats import rdfgraph

# make sure required content types are registered with mimerender
for shortname, content_types in rdfgraph.format_to_content_types.iteritems():
    try:
        mimerender.register_mime(shortname, content_types)
    except mimerender.MimeRenderException:
        # assume already registered
        pass

def no_mimetype_callback(accept_header, supported):
    """Callback for mimeparser when no acceptable MIME type is found."""
    # Expected return value is (content-type, data).
    # TODO: match returned content-type to accept_header.
    return ('application/json', json.dumps({
                'error': 'No acceptable content type found',
                'submitted': accept_header,
                'supported': supported
            }, indent=2))

def render_resource(f):
    return flaskmimerender(
        default='jsonld',
        json=formats.jsonf.from_jsonld,
        jsonld=formats.jsonldf.from_jsonld,
        n3=formats.n3f.from_jsonld,
        nt=formats.ntf.from_jsonld,
        nquads=formats.nquadsf.from_jsonld,
        rdf=formats.rdfxmlf.from_jsonld,
        trig=formats.trigf.from_jsonld,
        trix=formats.trixf.from_jsonld,
        turtle=formats.turtlef.from_jsonld,
        override_input_key='format',
        not_acceptable_callback=no_mimetype_callback
    )(f)
