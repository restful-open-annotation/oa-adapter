# Open Annotation adapter

Middleware for RESTful Open Annotation services.

Work in progress.

---

Try running `test.sh`.

Or, try this:

    for f in application/ld+json text/n3 application/n-triples application/n-quads application/rdf+xml application/trig application/trix text/turtle; do
      echo -e "\n--- $f ---"
      curl -H 'Content-Type: application/ld+json' -d '
      {
        "@id": "http://www.ex.com/1",
        "target": "http://www.ex.com/2"
      }' -H "Accept: $f" 127.0.0.1:5000/echo/
    done

## Adding formats

Support for input and output formats is loaded dynamically from files
named `*_format.py` in the `formats` directory. Each such file must
define the following:

* `format_name`: string, short name of the format.
* `mimetypes`: list of strings specifying the MIME types to associate with the
  format.
* `rom_jsonld`: function taking a JSON-LD dict and returning a string in the
  format.
* `to_jsonld`: function taking a string in the format and returning a JSON-LD
  dict.
