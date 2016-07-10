#!/usr/bin/env python
# -*- coding: iso-8859-2 -*-

from common import *

class StoreRow:
    """This is an absract class.
        Its descendants are intended to be visualized in PackageView."""
    
    STORE_TYPE_ICON = 0
    STORE_TYPE_STATE = 1
    STORE_CHECKBOX = 2
    STORE_INSTALLED_ICON = 3
    STORE_INSTALLED_STATE = 4
    STORE_UPGRADABLE_ICON = 5
    STORE_UPGRADABLE_STATE = 6
    STORE_MULTIPLE_ICON = 7
    STORE_MULTIPLE_STATE = 8
    STORE_NAME = 9
    STORE_DATE_STRING = 10
    STORE_DATE_VALUE = 11
    STORE_SIZE_STRING = 12
    STORE_SIZE_VALUE = 13
    STORE_OBJECT = 14
    STORE_LAST_ITEM = 15

    def GetSimpleStoreRow(self, pixbuf, name):
        """Return a simple store row containing pixbuf and name."""
        row = [pixbuf, False, False, None, False, None, False, None, False, \
                    conv(name), '', 0, '', 0, self]
        return row

    def IsPackage(self):
        return False
    
