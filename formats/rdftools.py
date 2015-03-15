#!/usr/bin/env python

"""RDF processing support."""

__author__ = 'Sampo Pyysalo'
__license__ = 'MIT'

import rdflib

from pyld import jsonld

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
    if format != 'nquads':
        graph = from_string(data, format)
        data = graph.serialize(format='nquads')
        # The above conversion introduces blank node identifiers for
        # triples that have no graph label (the fourth value).
        # Remove these to avoid modifying the data.
        data = _remove_blank_graph_labels(data)

    # Note: the N-Quads mime type is "application/n-quads"
    # (http://www.w3.org/TR/n-quads/), but pyld drops the dash.
    return jsonld.from_rdf(data, { 'format': 'application/nquads' })
