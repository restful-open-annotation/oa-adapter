#!/usr/bin/env python

"""Support for working with JSON-LD contexts."""

from pyld import jsonld

def context_urls_to_objects(document):
    """Replace context URLs with their corresponding objects.

    This function is intended to be called with a JSON-LD document
    prior to expansion to avoid unnecessary HTTP GETs.
    """
    # TODO: process recursively.
    try:
        if '@context' in document:
            document['@context'] = _get_context_for_url(document['@context'])
    except TypeError:
        # Assume document is not dict (e.g. list). TODO: implementation.
        pass
    return document

def context_objects_to_urls(document):
    """Replace context objects with their corresponding URLs.

    This function is intended to be called with a JSON-LD document
    after compaction for more concise presentation.
    """
    try:
        if '@context' in document:
            document['@context'] = _get_url_for_context(document['@context'])
    except TypeError:
        # Assume document is not dict (e.g. list). TODO: implementation.
        pass
    return document

# Context description from the final Open Annotation collaboration
# working draft (08 February 2013).
oa_context_20130208 = {
  "@context": {
    "oa": "http://www.w3.org/ns/oa#",
    "cnt": "http://www.w3.org/2011/content#",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "dctypes": "http://purl.org/dc/dcmitype/",
    "foaf": "http://xmlns.com/foaf/0.1/",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "owl": "http://www.w3.org/2002/07/owl#",
    "prov": "http://www.w3.org/ns/prov#",
    "trig": "http://www.w3.org/2004/03/trix/rdfg-1/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",

    "hasBody" :         {"@type":"@id", "@id" : "oa:hasBody"},
    "hasTarget" :       {"@type":"@id", "@id" : "oa:hasTarget"},
    "hasSource" :       {"@type":"@id", "@id" : "oa:hasSource"},
    "hasSelector" :     {"@type":"@id", "@id" : "oa:hasSelector"},
    "hasState" :        {"@type":"@id", "@id" : "oa:hasState"},
    "hasScope" :        {"@type":"@id", "@id" : "oa:hasScope"},
    "annotatedBy" :  {"@type":"@id", "@id" : "oa:annotatedBy"},
    "serializedBy" : {"@type":"@id", "@id" : "oa:serializedBy"},
    "motivatedBy" :  {"@type":"@id", "@id" : "oa:motivatedBy"},
    "equivalentTo" : {"@type":"@id", "@id" : "oa:equivalentTo"},
    "styledBy" :     {"@type":"@id", "@id" : "oa:styledBy"},
    "cachedSource" : {"@type":"@id", "@id" : "oa:cachedSource"},
    "conformsTo" :   {"@type":"@id", "@id" : "dcterms:conformsTo"},
    "default" :      {"@type":"@id", "@id" : "oa:default"},
    "item" :         {"@type":"@id", "@id" : "oa:item"},
    "first":         {"@type":"@id", "@id" : "rdf:first"},
    "rest":          {"@type":"@id", "@id" : "rdf:rest", "@container" : "@list"},

    "annotatedAt" :  { "@type": "xsd:dateTimeStamp", "@id": "oa:annotatedAt" },
    "end" :          { "@type": "xsd:nonNegativeInteger", "@id": "oa:end" },
    "exact" :        "oa:exact",
    "prefix" :       "oa:prefix",
    "serializedAt" : { "@type": "xsd:dateTimeStamp", "@id": "oa:serializedAt" },
    "start" :        { "@type": "xsd:nonNegativeInteger", "@id": "oa:start" },
    "styleClass" :   "oa:styleClass",
    "suffix" :       "oa:suffix",
    "when" :         { "@type": "xsd:dateTimeStamp", "@id": "oa:when" },

    "chars" :        "cnt:chars",
    "bytes" :        "cnt:bytes",
    "format" :       "dc:format",
    "language" :     "dc:language",
    "value" :        "rdf:value",
    "label" :        "rdfs:label",
    "name" :         "foaf:name",
    "mbox" :         "foaf:mbox"
  }
}

# Context description from the first Web Annotation WG working draft
# (11 December 2014).
wa_context_20141211 = {
 "@context": {
    "oa" :     "http://www.w3.org/ns/oa#",
    "dc" :     "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "dctypes": "http://purl.org/dc/dcmitype/",
    "foaf" :   "http://xmlns.com/foaf/0.1/",
    "rdf" :    "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs" :   "http://www.w3.org/2000/01/rdf-schema#",
    "skos" :   "http://www.w3.org/2004/02/skos/core#",

    "body" :         {"@id" : "oa:hasBody"},
    "target" :       {"@type":"@id", "@id" : "oa:hasTarget"},
    "source" :       {"@type":"@id", "@id" : "oa:hasSource"},
    "selector" :     {"@type":"@id", "@id" : "oa:hasSelector"},
    "state" :        {"@type":"@id", "@id" : "oa:hasState"},
    "scope" :        {"@type":"@id", "@id" : "oa:hasScope"},
    "annotatedBy" :  {"@type":"@id", "@id" : "oa:annotatedBy"},
    "serializedBy" : {"@type":"@id", "@id" : "oa:serializedBy"},
    "motivation" :   {"@type":"@id", "@id" : "oa:motivatedBy"},
    "stylesheet" :   {"@type":"@id", "@id" : "oa:styledBy"},
    "cached" :       {"@type":"@id", "@id" : "oa:cachedSource"},
    "conformsTo" :   {"@type":"@id", "@id" : "dcterms:conformsTo"},
    "members" :      {"@type":"@id", "@id" : "oa:membershipList", "@container": "@list"},
    "item" :         {"@type":"@id", "@id" : "oa:item"},
    "related" :      {"@type":"@id", "@id" : "skos:related"},

    "format" :       "dc:format",
    "language":      "dc:language",
    "annotatedAt" :  "oa:annotatedAt",
    "serializedAt" : "oa:serializedAt",
    "when" :         "oa:when",
    "value" :        "rdf:value",
    "start" :        "oa:start",
    "end" :          "oa:end",
    "exact" :        "oa:exact",
    "prefix" :       "oa:prefix",
    "suffix" :       "oa:suffix",
    "label" :        "rdfs:label",
    "name" :         "foaf:name",
    "mbox" :         "foaf:mbox",
    "nick" :         "foaf:nick",
    "styleClass" :   "oa:styleClass"
  }
}

# Context description for the RESTful Open Annotation API
# (17 March 2015).
roaa_context_20150317 = {
 "@context": {
    "oa" :     "http://www.w3.org/ns/oa#",
    "dc" :     "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "dctypes": "http://purl.org/dc/dcmitype/",
    "foaf" :   "http://xmlns.com/foaf/0.1/",
    "rdf" :    "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rdfs" :   "http://www.w3.org/2000/01/rdf-schema#",
    "skos" :   "http://www.w3.org/2004/02/skos/core#",
    "lrel" :   "http://www.iana.org/assignments/link-relations/#",

    "body" :         {"@id" : "oa:hasBody"},
    "target" :       {"@type":"@id", "@id" : "oa:hasTarget"},
    "source" :       {"@type":"@id", "@id" : "oa:hasSource"},
    "selector" :     {"@type":"@id", "@id" : "oa:hasSelector"},
    "state" :        {"@type":"@id", "@id" : "oa:hasState"},
    "scope" :        {"@type":"@id", "@id" : "oa:hasScope"},
    "annotatedBy" :  {"@type":"@id", "@id" : "oa:annotatedBy"},
    "serializedBy" : {"@type":"@id", "@id" : "oa:serializedBy"},
    "motivation" :   {"@type":"@id", "@id" : "oa:motivatedBy"},
    "stylesheet" :   {"@type":"@id", "@id" : "oa:styledBy"},
    "cached" :       {"@type":"@id", "@id" : "oa:cachedSource"},
    "conformsTo" :   {"@type":"@id", "@id" : "dcterms:conformsTo"},
    "members" :      {"@type":"@id", "@id" : "oa:membershipList", "@container": "@list"},
    "item" :         {"@type":"@id", "@id" : "oa:item"},
    "related" :      {"@type":"@id", "@id" : "skos:related"},
    "start":         {"@type":"@id", "@id" : "lrel:start"},
    "prev":          {"@type":"@id", "@id" : "lrel:prev"},
    "next":          {"@type":"@id", "@id" : "lrel:next"},
    "last":          {"@type":"@id", "@id" : "lrel:last"},
    "item":          {"@type":"@id", "@id" : "lrel:item"},
    "collection":    {"@type":"@id", "@id" : "lrel:collection"},

    "format" :       "dc:format",
    "language":      "dc:language",
    "annotatedAt" :  "oa:annotatedAt",
    "serializedAt" : "oa:serializedAt",
    "when" :         "oa:when",
    "value" :        "rdf:value",
    "start" :        "oa:start",
    "end" :          "oa:end",
    "exact" :        "oa:exact",
    "prefix" :       "oa:prefix",
    "suffix" :       "oa:suffix",
    "label" :        "rdfs:label",
    "name" :         "foaf:name",
    "mbox" :         "foaf:mbox",
    "nick" :         "foaf:nick",
    "styleClass" :   "oa:styleClass"
  }
}

# mapping from URLs to context descriptions.
url_to_context = {
    # from http://www.openannotation.org/spec/core/publishing.html
    'http://www.w3.org/ns/oa-context-20130208.json': oa_context_20130208,
    # curl http://www.w3.org/ns/oa-context-20130208.json (12.03.2015)
    # status 307 Temporary Redirect
    'http://www.w3.org/ns/oa.jsonld': oa_context_20130208,
    'http://nlplab.org/ns/restoa-context-20150307.json': roaa_context_20150317,
}

def _get_context_for_url(url):
    """Return context object for given URL.

    Returns:
        context dict, or given URL if not found.
    """
    if not isinstance(url, basestring):
        return url  # can only map strings
    return url_to_context.get(url, url)

def _get_url_for_context(document):
    """Return URL for given context object.

    Returns:
        context URL, or given dict if not found.
    """
    for url, context in url_to_context.iteritems():
        # TODO: avoid unnecessarily repeated normalization of known contexts
        if jsonld.normalize(context['@context']) == jsonld.normalize(document):
            return url
    return document
