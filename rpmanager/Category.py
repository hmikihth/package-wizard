#!/usr/bin/env python
# -*- coding: iso-8859-2 -*-

from StoreRow import *
from Pixbufs import *
import common; _ = common._

class Category(StoreRow):
    """This class represents a category."""
    def __init__(self, name):
        self.name = name
        self.sub_categories = {}
        self.packages = []
        self.package_counter = 0
        
    def GetSubCategory(self, name):
        """Get the sub Category object named 'name'.
            Create if it doesn't already exists."""
        if not self.sub_categories.has_key(name):
            self.sub_categories[name] = Category(name)
        self.sub_categories[name].package_counter += 1
        return self.sub_categories[name]
                
    def AddPackage(self, package):
        """Add package 'package'."""
        self.packages.append(package)
    
    def GetSubCategories(self):
        return self.sub_categories.values()
        
    def GetPackages(self):
        return self.packages
    
    def GetStoreRow(self):
        row = self.GetSimpleStoreRow(Pixbufs.INTERNET, self.name)
        return row

    def GetInfo(self, arg):
        infos = [
            (_('Type'),  _('Category')),
            (_('Name'), self.name),
            (_('Number of (filtered) packages'), `self.package_counter`)
        ]
        return infos
