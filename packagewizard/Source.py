#!/usr/bin/env python
# -*- coding: iso-8859-2 -*-

from StoreRow import *
from Pixbufs import *
import common; _ = common._

class Source(StoreRow):
    """This class describes a package source."""

    def __init__(self, name):
        self.name = name
        self.packages = []
        self.ignore = False
        self.removable = False
        self.package_counter = 0
        
    def AddPackage(self, package):
        """Add 'package' to this source."""
        self.packages.append(package)
        self.package_counter += 1
        
    def GetStoreRow(self):
        if self.removable:
            pixbuf = Pixbufs.CDROM
        else:
            pixbuf = Pixbufs.INTERNET
        
        row = self.GetSimpleStoreRow(pixbuf, self.name)
        return row

    def GetInfo(self, arg):
        infos = [
            (_('Type'), _('Source')),
            (_('Name'), self.name),
            (_('Active'), get_bool_str(not self.ignore)),
            (_('Media'), {True: 'CDROM', False: 'Internet'}[self.removable]),
            (_('Number of packages'), `self.package_counter`)
        ]
        return infos
    
