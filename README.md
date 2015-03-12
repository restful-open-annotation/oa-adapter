# Open Annotation adapter

Middleware for RESTful Open Annotation services.

Work in progress.

---

Try this:

    for f in application/ld+json text/n3 application/n-triples application/n-quads application/rdf+xml application/trig application/trix text/turtle; do
      echo -e "\n--- $f ---"
      curl -H 'Content-Type: application/ld+json' -d '
      {
        "@id": "http://www.ex.com/1",
        "target": "http://www.ex.com/2"
      }' -H "Accept: $f" 127.0.0.1:5000/echo/
    done
