#!/usr/bin/env python

"""Open Annotation JSON-LD support.

This is primarily a thin wrapper around PyLD and the Open Annotation
recommended context.

See:

* http://www.openannotation.org/
* http://json-ld.org/
* https://github.com/digitalbazaar/pyld
* http://www.openannotation.org/spec/core/publishing.html#Serialization
"""

__author__ = 'Sampo Pyysalo'
__license__ = 'MIT'

import contexts

from pyld import jsonld

def default_context():
    return contexts.roaa_context_20150317

def default_base():
    return None

def _make_options(context, base):
    """Return pyld options for given context and base."""
    options = {}
    if context is None:
        context = default_context()
    options['expandContext'] = context
    if base is not None:
        options['base'] = base
    return options

def expand(document, context=None, base=None):
    """Expand OA JSON-LD, removing context.

    See http://www.w3.org/TR/json-ld-api/#expansion.
    """
    # Try to avoid GETting URL contexts
    document = contexts.context_urls_to_objects(document)
    return jsonld.expand(document, _make_options(context, base))

def compact(document, context=None, base=None, remove_context=False):
    """Compact OA JSON-LD, shortening forms according to context.

    See http://www.w3.org/TR/json-ld-api/#compaction.
    """

    if context is None:
        context = default_context()
    if base is None:
        base = default_base()

    options = {}
    if base is not None:
        options['base'] = base

    compacted = jsonld.compact(document, context, options)
    # Replace known context objects with URLs.
    compacted = contexts.context_objects_to_urls(compacted)

    if remove_context:
        try:
            del compacted['@context']
        except KeyError:
            pass

    return compacted

def flatten(document):
    """Flatten OA JSON-LD."""

    # See http://www.w3.org/TR/json-ld-api/#flattening

    return jsonld.flatten(document)

def to_rdf(document, context=None, base=None):
    """Deserialize OA JSON-LD to RDF, return N-Quads as string."""

    # From http://www.w3.org/TR/json-ld/#h3_serializing-deserializing-rdf:
    # 
    #     The procedure to deserialize a JSON-LD document to RDF
    #     involves the following steps:
    #
    #     1. Expand the JSON-LD document, removing any context; this
    #     ensures that properties, types, and values are given their
    #     full representation as IRIs and expanded values. [...]
    # 
    #     2. Flatten the document, which turns the document into an
    #     array of node objects. [...]
    #
    #     3. Turn each node object into a series of RDF triples.
    #
    # See also: http://www.w3.org/TR/2014/REC-json-ld-api-20140116/#rdf-serialization-deserialization-algorithms

    if context is None:
        context = default_context()
    if base is None:
        base = default_base()

    expanded = expand(document, context, base)
    print 'baz', expanded
    flattened = flatten(expanded)
    print 'quux', flattened
    return jsonld.to_rdf(expanded, {'format': 'application/nquads'})

def from_rdf(rdf, context=None, base=None, remove_context=False):
    """Serialize RDF as OA JSON-LD, return compacted JSON-LD."""

    # From http://www.w3.org/TR/json-ld/#h3_serializing-deserializing-rdf:
    #
    #    Deserializing [expanded and flattened JSON-LD] to RDF now is
    #    a straightforward process of turning each node object into
    #    one or more RDF triples. [...] The process of serializing RDF
    #    as JSON-LD can be thought of as the inverse of this last
    #    step, creating an expanded JSON-LD document closely matching
    #    the triples from RDF, using a single node object for all
    #    triples having a common subject, and a single property for
    #    those triples also having a common predicate.
    #
    # See also: http://www.w3.org/TR/2014/REC-json-ld-api-20140116/#rdf-serialization-deserialization-algorithms

    if context is None:
        context = default_context()
    if base is None:
        base = default_base()

    document = jsonld.from_rdf(rdf, {'format': 'application/nquads'})
    return compact(document, context, base, remove_context)
