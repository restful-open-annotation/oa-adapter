#!/usr/bin/env python

"""HTML support for Open Annotation."""

__author__ = 'Sampo Pyysalo'
__license__ = 'MIT'

from pyld import jsonld

# Short name for this format.
format_name = 'html'

# The MIME types associated with this format.
mimetypes = ['text/html', 'text/html; charset=UTF-8']

# The HTML header and trailer.
_html_header = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>JSON-LD</title>
    <link rel="stylesheet" href="/static/css/bootstrap.css">
    <link rel="stylesheet" href="/static/css/bootstrap-theme.css">
    <link rel="stylesheet" href="/static/css/style.css">
    <link rel="stylesheet" href="/static/css/hint.css">
    <link href='http://fonts.googleapis.com/css?family=Montserrat:400,700' rel='stylesheet' type='text/css'>
  </head>
  <body>
"""

_html_trailer = """  </body>
</html>
"""

def from_jsonld(data, options=None):
    """Render JSON-LD data into HTML.

    This is intended to be used as a mimerender render function
    (see http://mimerender.readthedocs.org/en/latest/).

    Args:
        data: dict containing JSON-LD data in expanded JSON-LD form
            (see http://www.w3.org/TR/json-ld/#expanded-document-form).
        options: dict of rendering options, or None for defaults.

    Returns:
        String representing the rendered data.
    """
    if options is None:
        options = {}

    # Special case: allow pre-rendered data to be passed through
    # without modification.
    # TODO: this is a bit of a hack. Try to avoid it.
    if options.get('passthrough'):
        return data

    parts = (
        [_html_header] +
        _to_html(data) +
        [_html_trailer]
    )
    html = ''.join(parts)
    return _pretty_print_html(html)

def to_jsonld(data, options=None):
    """Parse HTML data into JSON-LD.

    Args:
        data: string in HTML format.
        options: dict of parsing options, or None for defaults.

    Returns:
        dict containing JSON-LD data in expanded JSON-LD form
            (see http://www.w3.org/TR/json-ld/#expanded-document-form).
    """
    if options is None:
        options = {}

    # TODO: this is a hack for allowing HTML to be passed through
    # proxying unmodified. Resolve more systematically.
    return data

def _pretty_print_html(html):
    try:
        from BeautifulSoup import BeautifulSoup
    except ImportError:
        # no can do
        return html
    return BeautifulSoup(html).prettify()

def _get_url(document):
    """Return the URL for the given JSON-LD document."""
    return document['@id']
    
def _is_url(value):
    """Return True if given value is JSON-LD URL, False otherwise."""
    try:
        # TODO: don't assume all IRIs are URLs.
        if len(value) != 1:
            return False
        url = _get_url(value)
        return True
    except:
        return False

def _is_plain_value(dict_):
    """Return True if dict is plain JSON-LD value, False otherwise."""
    return len(dict_) == 1 and '@value' in dict_

def _plain_value_to_html(dict_, html=None):
    """Convert plain JSON-LD value to HTML."""
    if html is None:
        html = []
    html.append(dict_['@value'])
    return html

def _is_datetime(dict_):
    """Return True if dict is a JSON-LD datetime, False otherwise."""
    return (len(dict_) == 2 and '@value' in dict_ and '@type' in dict_ and
            dict_['@type'] == 'http://www.w3.org/2001/XMLSchema#dateTimeStamp')

def _datetime_to_html(dict_, html=None):
    """Convert JSON-LD datetime to HTML."""
    if html is None:
        html = []
    datetime = dict_['@value']
    html.append('<time datetime="%s">%s</time>' % (datetime, datetime))
    return html

def _list_to_html(list_, html=None):
    """Convert JSON-LD list to HTML."""
    if html is None:
        html = []
    if len(list_) == 1:
        _to_html(list_[0], html)
    else:
        html.append('<ul>\n')
        for item in list_:
            html.append('<li>')
            _to_html(item, html)
            html.append('</li>\n')        
        html.append('</ul>\n')
    return html

def _key_value_to_html(key, value, html=None):
    """Convert (key, value) pair in JSON-LD dict to HTML."""
    if html is None:
        html = []
    if key == '@id':
        # IDs map to links
        html.append('<a href="%s">%s</a>' % (value, value))
    else:
        html.append('<dt>')
        _to_html(key, html)
        html.append('</dt>')
        html.append('<dd>')
        _to_html(value, html)
        html.append('</dd>\n')
    return html

def _dict_to_html(dict_, html=None):
    """Convert JSON-LD dict to HTML."""
    if html is None:
        html = []
    if _is_plain_value(dict_):
        _plain_value_to_html(dict_, html)
    elif _is_datetime(dict_):
        _datetime_to_html(dict_, html)
    else:
        # Generic processing
        html.append('<dl>\n')
        for key, value in sorted(dict_.items()):
            _key_value_to_html(key, value, html)
        html.append('</dl>\n')        
    return html

def _to_html(value, html=None):
    """Convert JSON-LD value to HTML.

    Args:
        value: JSON-LD dict, list, or primive value.
        html: list to append HTML to, or None to create a new list.

    Returns:
        list with converted HTML.
    """
    if html is None:
        html = []
    if isinstance(value, list):
        _list_to_html(value, html)
    elif isinstance(value, dict):
        _dict_to_html(value, html)
    else:
        html.append(str(value))
    return html
