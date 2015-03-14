#!/bin/bash

FORMATS="
application/ld+json
text/n3
application/n-triples
application/n-quads
application/rdf+xml
application/trig
application/trix
text/turtle
"

# JSON-LD input, various output formats
for f in $FORMATS; do
    echo -e "\n--- JSON-LD to $f ---"
    curl -H 'Content-Type: application/ld+json' -d '
    {
      "@context": "http://www.w3.org/ns/oa.jsonld",
      "@id": "http://ex.com/1",
      "target": "http://ex.com/2"
    }' -H "Accept: $f" 127.0.0.1:5000/echo/
done

# Roundtrip triples via various formats
for f in $FORMATS; do
    echo -e "\n--- triples to $f to triples (should be same) ---"
    input="<http://ex.com/1> <http://www.w3.org/ns/oa#hasTarget> <http://ex.com/2> ."
    converted=$(curl -H 'Content-Type: application/n-triples' -d "$input" \
	-H "Accept: $f" 127.0.0.1:5000/echo/)
    # NOTE: if data starts with "@", curl will assume it's a filename.
    # n3, trig and turtle outputs frequently start with "@prefix", so
    # we'll want to tweak these a bit to avoid that interpretation.
    if [[ "$converted" == @* ]]; then
	converted=" $converted" # add initial space
    fi    
    output=$(curl -H "Content-Type: $f" -d "$converted" \
 	-H 'Accept: application/n-triples' 127.0.0.1:5000/echo/)
    echo "in:  $input"
    echo "out: $output"
done
