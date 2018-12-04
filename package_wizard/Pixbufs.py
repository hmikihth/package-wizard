#!/usr/bin/env python
# -*- coding: iso-8859-2 -*-

import gtk

class Pixbufs:
    """This class is a singleton.  It stores the pixbufs used throughout the application."""
    
    def LoadPixbuf(filename):
        """Load and return the pixbuf related to filename."""
        path = 'gui/' + filename + '.png'
        pixbuf = gtk.gdk.pixbuf_new_from_file(path)
        return pixbuf
        
    INSTALLED = LoadPixbuf('installed')
    NOT_INSTALLED = LoadPixbuf('not-installed')
    UPGRADABLE = LoadPixbuf('upgradable')
    NOT_UPGRADABLE = LoadPixbuf('not-upgradable')
    MULTIPLE = LoadPixbuf('multiple')
    SINGLE = LoadPixbuf('single')
    APPLICATION = LoadPixbuf('application')
    LIBRARY = LoadPixbuf('library')
    INTERNET = LoadPixbuf('internet')
    CDROM = LoadPixbuf('cdrom')
    
