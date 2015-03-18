#!/usr/bin/env python

"""File format support module loader.

The import and export formats supported by the adapter are determined
at runtime based on the format support "modules" found in the formats/
directory.
"""

import sys
import os

# Directory containing format modules.
FORMAT_DIRECTORY = 'formats'

# Attributes that every module should have.
# format_name: string giving the short name of the format.
# mimetypes:   list of MIME types that should be associated with the format.
# from_jsonld: function rendering JSON-LD to string in the format.
# to_jsonld:   function parsing string in the format to JSON-LD.
REQUIRED_ATTRIBUTES = [
    'format_name',
    'mimetypes', 
    'from_jsonld',
    'to_jsonld',
]

def _is_valid(m, err=None):
    """Returns if the given module has all required attributes."""
    if err is None:
        err = sys.stderr
    for a in REQUIRED_ATTRIBUTES:
        try:
            getattr(m, a)
        except AttributeError, e:
            print >> err, 'Module %s is not valid: %s' % (m.__name__, e)
            return False
    return True

def _is_format_module(fn):
    if fn == '__init__.py':
        return False
    return fn.endswith('_format.py')

def _load_format_module(dir, mn):
    if mn.endswith('.py'):
        mn = mn[:-3]
    try:
        mod = __import__(dir, fromlist=[mn])
    except:
        raise
    return getattr(mod, mn)

def load(dir=FORMAT_DIRECTORY):
    """Load format processing modules."""
    # Load everything matching the naming conventions.
    modules = []
    for fn in (f for f in os.listdir(dir) if _is_format_module(f)):
        module = _load_format_module(dir, fn)
        if module is None:
            continue
        modules.append(module)
    # Filter to exclude modules that don't have the required attributes.
    valid = []
    seen = set()
    for module in (m for m in modules if _is_valid(m)):
        if module.format_name in seen:
            print >> sys.stderr, 'Duplicate format %s' % module.format_name
        else:
            valid.append(module)
            seen.add(module)
    return valid
