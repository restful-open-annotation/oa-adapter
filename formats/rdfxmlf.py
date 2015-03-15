#!/usr/bin/env python

"""RDF/XML content-type support for Open Annotation."""

__author__ = 'Sampo Pyysalo'
__license__ = 'MIT'

import rdftools

# Default values for rendering options
PRETTYPRINT_DEFAULT = True

def from_jsonld(data, options=None):
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

    prettyprint = options.get('prettyprint', PRETTYPRINT_DEFAULT)
    if prettyprint:
        format='pretty-xml'
    else:
        format='xml'

    try:
        return rdftools.from_jsonld(data, format=format)
    except Exception, e:
        _process_xml_serialization_exception(e)

def to_jsonld(data, options=None):
    """Parse RDF/XML data into JSON-LD.

    Args:
        data: string in RDF/XML format.
        options: dict of parsing options, or None for defaults.

    Returns:
        dict containing JSON-LD data in expanded JSON-LD form
            (see http://www.w3.org/TR/json-ld/#expanded-document-form).
    """
    if options is None:
        options = {}

    return rdftools.to_jsonld(data, 'xml')

def _process_xml_serialization_exception(e):
    # Special-case processing for rdflib failures to serialize into
    # RDF/XML.
    if "Can't split " in str(e):
        print """
Note: it appears that rdflib is failing to split a URI into a namespace
and name in RDF/XML serialization:

    %s

This may be a bug in rdflib. You could try adding a hash into the URI,
this seems to help in some cases.
""" % str(e)
        raise Exception('rdflib failed to split URI into namespace and name: %s' % str(e))
    else:
        raise e
