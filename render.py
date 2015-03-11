#!/usr/bin/env python

"""Support for rendering various MIME types."""

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

# make sure required content types are registered with mimerender
_content_types = {
    'jsonld': ('application/ld+json', ),
    'nt':     ('application/n-triples', ),
    'nquads': ('application/n-quads', ),
    # Note: "charset" for n3 and turthe is not an error: "This MIME
    # type is used with a charset parameter: the encoding is always
    # utf-8. [...] This is because the default encoding for types in
    # the text/* tree is ASCII (http://www.w3.org/TeamSubmission/n3/).
    'n3':     ('text/n3; charset=utf-8', 'text/n3'),
    'trig':   ('application/trig', ),
    'trix':   ('application/trix', ),
    'turtle': ('text/turtle; charset=utf-8', 'text/turtle'),
}

for shortname, content_types in _content_types.iteritems():
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
        json=formats.jsonf.render,
        jsonld=formats.jsonldf.render,
        n3=formats.n3f.render,
        nt=formats.ntf.render,
        nquads=formats.nquadsf.render,
        rdf=formats.rdfxmlf.render,
        trig=formats.trigf.render,
        trix=formats.trixf.render,
        turtle=formats.turtlef.render,
        override_input_key='format',
        not_acceptable_callback=no_mimetype_callback
    )(f)
