#!/usr/bin/env python

"""RDF processing support."""

__author__ = 'Sampo Pyysalo'
__license__ = 'MIT'

import rdflib

from pyld import jsonld

# Mapping from short identifiers for RDF formats to their content types.
# Note: the format strings should match those used by rdflib.
format_to_content_types = {
    'jsonld': ('application/ld+json', ),
    'nt':     ('application/n-triples', ),
    'nquads': ('application/n-quads', ),
    # Note: "charset" for n3 and turtle is not an error: "This MIME
    # type is used with a charset parameter: the encoding is always
    # utf-8. [...] This is because the default encoding for types in
    # the text/* tree is ASCII (http://www.w3.org/TeamSubmission/n3/).
    'n3':     ('text/n3; charset=utf-8', 'text/n3'),
    'trig':   ('application/trig', ),
    'trix':   ('application/trix', ),
    'turtle': ('text/turtle; charset=utf-8', 'text/turtle'),
}

# Mapping from content types to short identifiers for RDF formats.
content_type_to_format = dict((ct, name)
                              for name, cts in format_to_content_types.items()
                              for ct in cts)

def from_jsonld(data, format):
    """Return string in given RDF format from JSON-LD data.

    Args:
        data: dict containing JSON-LD data in expanded JSON-LD form
            (see http://www.w3.org/TR/json-ld/#expanded-document-form).
        format: short name or MIME type of an RDF format. For example
            'nt' or 'application/n-triples' for N-Triples.

    Returns:
        instance of rdflib.Graph.
    """
    # As of this writing, 'application/nquads' is the only RDF format
    # (other than JSON-LD) supported by pyld. Convert via that.
    quads = jsonld.to_rdf(data, { 'format': 'application/nquads' })
    # Using ConjunctiveGraph instead of Graph for nquads support.
    graph = rdflib.ConjunctiveGraph()
    graph.parse(data=quads, format='nquads')
    return graph.serialize(format=format)

def from_string(data, format):
    """Return RDF graph from string in RDF format.

    Args:
        data: string in given RDF format.
        format: short name or MIME type of an RDF format. For example
            'nt' or 'application/n-triples' for N-Triples.
    Returns:
        instance of rdflib.Graph.
    """
    # Map to rdflib short format name if content type format.
    format = content_type_to_format.get(format, format)

    # Using ConjunctiveGraph instead of Graph for nquads support.
    graph = rdflib.ConjunctiveGraph()
    graph.parse(data=data, format=format)
    return graph

def _is_blank(i):
    """Return True if given a blank node identifier, False otherwise."""
    return i.startswith('_:')

def _remove_blank_graph_labels(data):
    """Remove blank node graph labels from N-Quads data.

    >>> _remove_blank_graph_label('<ex:1> <ex:2> <ex:3> _:b0 .')
    '<ex:1> <ex:2> <ex:3> .'

    Args:
        data: string in N-Quads format.

    Returns:
        data: string in N-Quads format.
    """
    # TODO: parse properly
    processed = []
    for line in data.split('\n'):
        fields = line.split()
        if len(fields) >= 4 and _is_blank(fields[3]):
            fields = fields[:3] + fields[4:]
        processed.append(' '.join(fields))
    return '\n'.join(processed)

def to_jsonld(data, format):
    """Return JSON-LD data from string in RDF format.

    Args:
        data: string in given RDF format.
        format: short name or MIME type of an RDF format. For example
            'nt' or 'application/n-triples' for N-Triples.

    Returns:
        data: dict containing JSON-LD data in expanded JSON-LD form
            (see http://www.w3.org/TR/json-ld/#expanded-document-form).
    """
    # pyld only supports parsing of nquads. Other formats are first
    # converted into nquads via rdflib.Graph.
    if content_type_to_format.get(format, format) != 'nquads':
        graph = from_string(data, format)
        data = graph.serialize(format='nquads')
        # The above conversion introduces blank node identifiers for
        # triples that have no graph label (the fourth value).
        # Remove these to avoid modifying the data.
        data = _remove_blank_graph_labels(data)

    # Note: the N-Quads mime type is "application/n-quads"
    # (http://www.w3.org/TR/n-quads/), but pyld drops the dash.
    return jsonld.from_rdf(data, { 'format': 'application/nquads' })
