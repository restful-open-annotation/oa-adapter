#!/usr/bin/env python

"""RDF processing support."""

__author__ = 'Sampo Pyysalo'
__license__ = 'MIT'

import rdflib

from pyld import jsonld

def from_jsonld(data):
    """Return RDF graph from given JSON-LD data.

    Args:
        data: dict containing JSON-LD data in expanded JSON-LD form
            (see http://www.w3.org/TR/json-ld/#expanded-document-form).

    Returns:
        instance of rdflib.Graph.
    """
    # As of this writing, 'application/nquads' is the only RDF format
    # (other than JSON-LD) supported by pyld.
    quads = jsonld.to_rdf(data, {'format': 'application/nquads'})    
    # Using ConjunctiveGraph instead of Graph for nquads support.
    graph = rdflib.ConjunctiveGraph()
    graph.parse(data=quads, format='nquads')
    return graph

def to_jsonld(graph):
    """Return JSON-LD data from given RDF Graph."""
    raise NotImplementedError
