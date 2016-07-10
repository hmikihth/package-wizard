#!/usr/bin/env python
# -*- coding: utf-8 -*-

import string
import gettext
import gtk.glade
gettext.bindtextdomain('rpmanager', 'locale')
gtk.glade.bindtextdomain('rpmanager', 'locale')
gettext.textdomain('rpmanager')
gtk.glade.textdomain('rpmanager')
_ = gettext.gettext
#def _(s):
#    return s

GLADE_FILENAME = 'gui/rpmanager.glade'

DEBUG_PACKAGES = 2**0
DEBUG_FORKS = 2**1

debug_level = DEBUG_FORKS | DEBUG_PACKAGES


def debug(level, string):
    """Print string if debug level is set."""
    debug_strings = {
        DEBUG_PACKAGES: 'DEBUG_PACKAGES',
        DEBUG_FORKS: 'DEBUG_FORKS'
    }
    if debug_level & level:
        print debug_strings[level] + ': '+ string

def conv(string):
    """Return the unicode representation of string."""
    return unicode(string, 'iso-8859-1')

def get_human_readable_size(size):
    """Return the more easily readable string representation of size."""
    if size > 10**6:
        return `size/10**6`+'MiB'
    elif size > 10**3:
        return `size/10**3`+'KiB'
    else:
        return `size`+'b'

def get_bool_str(bool):
    return {True: 'Igen', False: 'Nem'}[bool]

def unescape(s):
    r = ''
    for c in s:
        if c == '"':
            r += '\\'
        r += c
    return r
    
def escape(s):
    t = ''
    for c in s:
        if c not in string.ascii_letters + string.digits:
            t += '\\' + c
        else:
            t += c
    return t
