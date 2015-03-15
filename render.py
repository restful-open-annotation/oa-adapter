#!/usr/bin/env python

"""Support for rendering JSON-LD into various MIME types."""

__author__ = 'Sampo Pyysalo'
__license__ = 'MIT'

import json

import mimerender
flaskmimerender = mimerender.FlaskMimeRender()

def no_mimetype_callback(accept_header, supported):
    """Callback for mimeparser when no acceptable MIME type is found."""
    # Expected return value is (content-type, data).
    # TODO: match returned content-type to accept_header.
    return ('application/json', json.dumps({
                'error': 'No acceptable content type found',
                'submitted': accept_header,
                'supported': supported
            }, indent=2))

def register_types(formats):
    # make sure required content types are registered with mimerender
    for f in formats:
        try:
            mimerender.register_mime(f.format_name, f.mimetypes)
        except mimerender.MimeRenderException:
            # assume already registered
            pass

def make_renderer(formats, default='jsonld'):
    format_args = { f.format_name: f.from_jsonld for f in formats }
    assert default in format_args, 'Default format %s not available' % default

    register_types(formats)

    def render_resource(f):
        return flaskmimerender(default=default,
                               override_input_key='format',
                               not_acceptable_callback=no_mimetype_callback,
                               **format_args)(f)
    return render_resource
