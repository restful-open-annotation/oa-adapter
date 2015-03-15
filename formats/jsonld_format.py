#!/usr/bin/env python

"""JSON-LD content-type support for Open Annotation."""

__author__ = 'Sampo Pyysalo'
__license__ = 'MIT'

import json

import flask

import oajson

# Default values for rendering options
PRETTYPRINT_DEFAULT = True

# Short name for this format.
format_name = 'jsonld'

# The MIME types associated with this format.
mimetypes = ['application/ld+json']

# The profiles specifying the various JSON-LD document forms.
# (See http://www.w3.org/TR/json-ld-syntax/#application-ld-json)
JSON_LD_COMPACTED = "http://www.w3.org/ns/json-ld#compacted"
JSON_LD_EXPANDED = "http://www.w3.org/ns/json-ld#expanded"
JSON_LD_FLATTENED = "http://www.w3.org/ns/json-ld#flattened"
JSON_LD_PROFILES = [
    JSON_LD_COMPACTED,
    JSON_LD_EXPANDED,
    JSON_LD_FLATTENED,
]
DEFAULT_PROFILE = JSON_LD_COMPACTED

def _select_response_form(request=None):
    """Return the JSON-LD profile applying to the response."""
    if request is None:
        request = flask.request
    header = request.headers.get('Accept', '')
    for profile in JSON_LD_PROFILES:
        # TODO: parse the header instead of just looking for a substring
        if profile in header:
            return profile
    # TODO: check for Link headers with profile.
    return DEFAULT_PROFILE

def from_jsonld(data, options=None):
    """Render JSON-LD data into string.

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

    # Select the specific document form (expanded, compacted, or
    # flattened) based on the request.
    document_form = _select_response_form()
    if document_form == JSON_LD_COMPACTED:
        data = oajson.compact(data)
    elif document_form == JSON_LD_FLATTENED:
        data = oajson.flatten(data)
    else:
        assert document_form == JSON_LD_EXPANDED, 'internal error'
        pass # no-op: internal representation is alredy expanded.

    prettyprint = options.get('prettyprint', PRETTYPRINT_DEFAULT)
    if prettyprint:
        return json.dumps(data, indent=2, separators=(',', ': '))+'\n'
    else:
        return json.dumps(data)

def to_jsonld(data, options=None):
    """Parse JSON-LD data.

    Args:
        data: string in JSON-LD format.
        options: dict of parsing options, or None for defaults.

    Returns:
        dict containing JSON-LD data in expanded JSON-LD form
            (see http://www.w3.org/TR/json-ld/#expanded-document-form).
    """
    if options is None:
        options = {}

    encoding = options.get('encoding')

    if encoding is None:
        jsonld = json.loads(data)
    else:
        jsonld = json.loads(data, encoding=encoding)

    # TODO: expand
    return jsonld
