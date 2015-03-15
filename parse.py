#!/usr/bin/env python

"""Support for parsing various MIME types into JSON-LD."""

__author__ = 'Sampo Pyysalo'
__license__ = 'MIT'

def make_parser(formats):
    """Return a function for parsing data into JSON-LD."""

    mimetype_to_parse_function = {}
    for f in formats:
        for m in f.mimetypes:
            mimetype_to_parse_function[m] = f.to_jsonld

    def parse_data(data, mimetype=None, charset=None):
        """Parse data into JSON-LD."""
        options = { 'encoding': charset }
        parse_function = mimetype_to_parse_function.get(mimetype)
        if not parse_function:
            raise NotImplementedError('not implemented: parsing %s' % mimetype)
        else:
            return parse_function(data, options)

    return parse_data
