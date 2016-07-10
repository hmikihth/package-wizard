 #!/usr/bin/env python
# -*- coding: iso-8859-2 -*-

import gobject
import gtk

from common import *
import common; _ = common._
import singletons
from StoreRow import *

class PackageView(StoreRow):
    """This class represents the package view widget."""
    LISTING_MODE_FLAT = 0
    LISTING_MODE_CATEGORY = 1
    LISTING_MODE_SOURCE = 2
    DEFAULT_LISTING_MODE = LISTING_MODE_FLAT
    listing_mode_to_toggle_column_width = { LISTING_MODE_FLAT: 40, LISTING_MODE_CATEGORY: 80, LISTING_MODE_SOURCE: 50}
    ROW_TYPE_PACKAGE = 0
    ROW_TYPE_CATEGORY = 1
    ROW_TYPE_SOURCE = 2
    COLUMN_TOGGLE = 0
    COLUMN_NAME = 5
    
    def __init__(self):
        """Initialize the view."""
        self.installable_count = 0
        self.removable_count = 0
        self.upgradable_count = 0
        self.mode = self.LISTING_MODE_FLAT
        # Create the TreeView and add it to the ScrolledWindow
        self.sw = gtk.ScrolledWindow()
        self.sw.set_policy(gtk.POLICY_NEVER, gtk.POLICY_ALWAYS)
        self.treeview = gtk.TreeView()
        self.treeview.connect('cursor_changed',  self.OnTreeviewCursorChanged)
        self.sw.add(self.treeview)
        # Create the TreeStore and bind it to the TreeView
        self.store = gtk.TreeStore(
            gtk.gdk.Pixbuf,  # STORE_TYPE_ICON
            gobject.TYPE_BOOLEAN,  # STORE_TYPE_STATE
            gobject.TYPE_BOOLEAN,  # STORE_CHECKBOX
            gtk.gdk.Pixbuf,  # STORE_INSTALLED_ICON
            gobject.TYPE_BOOLEAN,   # STORE_INSTALLED_STATE
            gtk.gdk.Pixbuf,  # STORE_UPGRADABLE_ICON
            gobject.TYPE_BOOLEAN,  # STORE_UPGRADABLE_STATE
            gtk.gdk.Pixbuf,  # STORE_MULTIPLE_ICON
            gobject.TYPE_BOOLEAN,  # STORE_MULTIPLE_STATE
            gobject.TYPE_STRING,  # STORE_NAME
            gobject.TYPE_STRING,  # STORE_DATE_STRING
            gobject.TYPE_INT,  # STORE_DATE_VALUE
            gobject.TYPE_STRING,  # STORE_SIZE_STRING
            gobject.TYPE_INT,  # STORE_SIZE_VALUE
            gobject.TYPE_PYOBJECT  # STORE_OBJECT
        )
        self.treeview.set_model(self.store)
        # Create the TreeViewColumns and bind them to the TreeView
        DEFAULT_NAME_COLUMN_WIDTH = 200
        DEFAULT_TOGGLE_COLUMN_WIDTH = self.listing_mode_to_toggle_column_width[self.DEFAULT_LISTING_MODE]
        cellrenderertoggle = gtk.CellRendererToggle()
        cellrenderertoggle.connect ('toggled', self.OnCheckButtonToggled, self.store)
        col1 = gtk.TreeViewColumn ('', cellrenderertoggle, active=self.STORE_CHECKBOX)
        col1.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        col1.set_fixed_width(DEFAULT_TOGGLE_COLUMN_WIDTH)
        col2 = gtk.TreeViewColumn ('A', gtk.CellRendererPixbuf(), pixbuf=self.STORE_TYPE_ICON)
        col2.set_sort_column_id(self.STORE_TYPE_STATE)
        col3 = gtk.TreeViewColumn (_('I'), gtk.CellRendererPixbuf(), pixbuf=self.STORE_INSTALLED_ICON)
        col3.set_sort_column_id(self.STORE_INSTALLED_STATE)
        cellrendererpixbuf = gtk.CellRendererPixbuf()
        col4 = gtk.TreeViewColumn (_('U'), cellrendererpixbuf, pixbuf=self.STORE_UPGRADABLE_ICON)
        col4.set_sort_column_id(self.STORE_UPGRADABLE_STATE)
        col5 = gtk.TreeViewColumn ('2+', gtk.CellRendererPixbuf(), pixbuf=self.STORE_MULTIPLE_ICON)
        col5.set_sort_column_id(self.STORE_MULTIPLE_STATE)
        col6 = gtk.TreeViewColumn (_('Name'), gtk.CellRendererText(), text=self.STORE_NAME)
        col6.set_sort_column_id(self.STORE_NAME)
        col6.set_sizing(gtk.TREE_VIEW_COLUMN_FIXED)
        col6.set_fixed_width(DEFAULT_NAME_COLUMN_WIDTH)
        col6.set_expand(True)
        col7 = gtk.TreeViewColumn(_('Install date'), gtk.CellRendererText(), text=self.STORE_DATE_STRING)
        col7.set_sort_column_id(self.STORE_DATE_VALUE)
        col8 = gtk.TreeViewColumn (_('Size'), gtk.CellRendererText(), text=self.STORE_SIZE_STRING)
        col8.set_sort_column_id(self.STORE_SIZE_VALUE)
        for col in [col1, col2, col3, col4, col5, col6, col7, col8]:
            self.treeview.append_column(col)

    # Signal handlers
    
    def OnTreeviewCursorChanged(self, widget):
        singletons.application.RefreshButtons()
        singletons.application.RefreshInfoWindow()
    
    def OnCheckButtonToggled(self, cellrenderertoggle, path, model):
        iter = model.get_iter(path)
        value = model.get_value(iter, self.STORE_CHECKBOX)
        self.ModifyRowSelection(iter, not value)
        if model.iter_has_child(iter):
            child_iter = model.iter_children(iter)
            self.CheckAllSubTrees(child_iter, not value)

    # Signal handler helper methods

    def CheckAllSubTrees(self, iter, value):
        """Check all subtrees of iter of the store."""
        while iter:
            self.ModifyRowSelection(iter, value)
            if self.store.iter_has_child(iter):
                child_iter = self.store.iter_children(iter)
                self.CheckAllSubTrees(child_iter, value)
            iter = self.store.iter_next(iter)

    def ModifyRowSelection(self, iter, active):
        """Modify the current row of the treeview and register the change."""
        old_active = self.store.get_value(iter, self.STORE_CHECKBOX)
        if active == old_active:
            return
        self.store.set_value(iter, self.STORE_CHECKBOX, active)
        object = self.store.get_value(iter, self.STORE_OBJECT)
        if not object.IsPackage():
            return
        package = self.store.get_value(iter, self.STORE_OBJECT)
        if old_active:
            change = -1
        else:
            change = 1
        if package.is_installed:
            self.installable_count += change
        else:
            self.removable_count += change
        if package.is_upgradable:
            self.upgradable_count += change
            
    # Public methods
    def GetSelectedPackages(self, iter=None):
        """Get every packages that are currently selected in the view."""
        if iter == None:
            iter = self.store.get_iter(0)
        packages = []
        while iter:
            object = self.store.get_value(iter, self.STORE_OBJECT)
            if object.IsPackage():
                checked = self.store.get_value(iter, self.STORE_CHECKBOX)
                if checked:
                    packages.append(object)
            if self.store.iter_has_child(iter):
                child_iter = self.store.iter_children(iter)
                packages += self.GetSelectedPackages(child_iter)
            iter = self.store.iter_next(iter)
        return packages
    
    def GetButtonCounts(self):
        """Return the numbers of the installable, removable and upgradable
        packages related to the operation buttons."""
        return (self.removable_count,
            self.installable_count, self.upgradable_count)

    def GetCurrentRowInfo(self, extended=False):
        """Get the info of the object of the currently selected row."""
        iter = self.GetIterAtCursor()
        object = self.store.get_value(iter, self.STORE_OBJECT)
        info = object.GetInfo(extended)
        return info
    
    def IsEmpty(self):
        """Return whether the view is empty or not."""
        try:
            path = (0,)
            first_iter = self.store.get_iter(path)
        except ValueError, e:
            return True
        return False
    
    def Populate(self, listing_mode):
        """Populate store with rows describing the packages."""
        self.store.clear()
        if listing_mode == self.LISTING_MODE_FLAT:
            for package in singletons.package_pool.packages:
                row = package.GetStoreRow()
                self.store.append(None, row)
        elif listing_mode == self.LISTING_MODE_CATEGORY:
            self.BuildCategoryStore(None, singletons.package_pool.category_tree)
        elif listing_mode == self.LISTING_MODE_SOURCE:
            for source in singletons.package_pool.all_sources:
                row = source.GetStoreRow()
                iter = self.store.append(None, row)
                for package in source.packages:
                    row = package.GetStoreRow()
                    self.store.append(iter, row)
        self.ResizeColumns(listing_mode)
        cursor_path = (0,)
        self.treeview.set_cursor(cursor_path)
        self.installable_count = 0
        self.removable_count = 0
        self.upgradable_count = 0

    # Other helper methods
    def BuildCategoryStore(self, iter, category):
        """Recursively build the category view in the store."""
        subcategories = category.GetSubCategories()
        for subcategory in subcategories:
            row = subcategory.GetStoreRow()
            sub_iter = self.store.append(iter, row)
            self.BuildCategoryStore(sub_iter, subcategory)
        packages = category.GetPackages()
        for package in packages:
            row = package.GetStoreRow()
            self.store.append(iter, row)

    def GetIterAtCursor(self):
        """Return the iter of the current cursor position."""
        path = self.treeview.get_cursor()[0]
        iter = self.store.get_iter(path)
        return iter
    
    def ResizeColumns(self, mode):
        """Resize the columns according to mode."""
        width = self.listing_mode_to_toggle_column_width[mode]
        toggle_column =  self.treeview.get_column(self.COLUMN_TOGGLE)
        toggle_column_width = toggle_column.get_width()
        name_column = self.treeview.get_column(self.COLUMN_NAME)
        name_column_width = name_column.get_width()
        if toggle_column_width == 0 and name_column_width == 0:
            return  # Gets called the first time, when columns are uninitialized
        diff = toggle_column_width - width
        toggle_column.set_fixed_width(toggle_column_width - diff)
        name_column.set_fixed_width(name_column_width + diff)
