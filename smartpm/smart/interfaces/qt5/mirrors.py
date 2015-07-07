#-*- coding: utf-8 -*-
#
# Copyright (c) 2015 blackPanther OS - Charles Barcza
# GPL
#
from smart.interfaces.qt5 import getPixmap, centerWindow
from smart import *
from PyQt5 import QtGui as QtGui, QtWidgets

from PyQt5 import QtCore as QtCore, QtWidgets


class TextListViewItem(QtWidgets.QTreeWidgetItem):
    def __init__(self, parent):
        QtWidgets.QTreeWidgetItem.__init__(self, parent)
        self._text = {}
        self._oldtext = {}

    def setText(self, col, text):
        QtWidgets.QTreeWidgetItem.setText(self, col, text)
        if col in self._text:
            self._oldtext[col] = self._text[col]
        self._text[col] = text

    def oldtext(self, col):
        return self._oldtext.get(col, None)

class QtMirrors(object):

    def __init__(self, parent=None):

        self._window = QtWidgets.QDialog(None)
        self._window.setWindowIcon(QtGui.QIcon(getPixmap("smart")))
        self._window.setWindowTitle(_("Mirrors"))
        self._window.setModal(True)

        self._window.setMinimumSize(600, 400)

        layout = QtWidgets.QVBoxLayout(self._window)
        #layout.setResizeMode(QtGui.QLayout.FreeResize)

        vbox = QtWidgets.QWidget(self._window)
        QtWidgets.QVBoxLayout(vbox)
        vbox.layout().setMargin(10)
        vbox.layout().setSpacing(10)
        vbox.show()

        layout.addWidget(vbox)

        self._treeview = QtWidgets.QTreeWidget(vbox)
        self._treeview.setHeaderHidden(True)
        self._treeview.show()
        vbox.layout().addWidget(self._treeview)

        #self._treeview.addColumn(_("Mirror"))
        self._treeview.setHeaderLabels([_("Mirror")])
        #self._treeview.itemChanged[QTreeWidgetItem.connect(self.itemChanged)
        #self._treeview.itemSelectionChanged.connect(self.selectionChanged)

        bbox = QtWidgets.QWidget(vbox)
        QtWidgets.QHBoxLayout(bbox)
        bbox.layout().setSpacing(10)
        bbox.layout().addStretch(1)
        bbox.show()
        vbox.layout().addWidget(bbox)

        button = QtWidgets.QPushButton(_("New"), bbox)
        button.setEnabled(True)
        button.setIcon(QtGui.QIcon(getPixmap("crystal-add")))
        button.show()
        button.clicked[()].connect(self.newMirror)
        self._newmirror = button
        bbox.layout().addWidget(button)

        button = QtWidgets.QPushButton(_("Delete"), bbox)
        button.setEnabled(False)
        button.setIcon(QtGui.QIcon(getPixmap("crystal-delete")))
        button.show()
        button.clicked[()].connect(self.delMirror)
        self._delmirror = button
        bbox.layout().addWidget(button)

        button = QtWidgets.QPushButton(_("Close"), bbox)
        button.clicked[()].connect(self._window.accept)
        bbox.layout().addWidget(button)
        
        button.setDefault(True)

    def fill(self):
        self._treeview.clear()
        mirrors = sysconf.get("mirrors", {})
        for origin in mirrors:
             parent = TextListViewItem(self._treeview)
             parent.setText(0, origin)
             #parent.setRenameEnabled(0, True)
             for mirror in mirrors[origin]:
                 item = TextListViewItem(parent)
                 item.setText(0, mirror)
                 #item.setRenameEnabled(0, True)
             parent.setExpanded(True)
        
    def show(self):
        self.fill()
        self._window.show()
        centerWindow(self._window)
        self._window.raise_()
        self._window.exec_()
        self._window.hide()

    def newMirror(self):
        item = self._treeview.selectedItems()
        if item:
            item = item[0]
            if item.childCount() == 2:
                item = item.parent()
            origin = str(item.text(0))
        else:
            origin = ""
        origin, mirror = MirrorCreator(self._window).show(origin)
        if origin and mirror:
            sysconf.add(("mirrors", origin), mirror, unique=True)
        self.fill()


    def delMirror(self):
        item = self._treeview.selectedItems()
        if not item:
            return
        item = item[0]
        if item.parent() is None:
            origin = str(item.text(0))
            sysconf.remove(("mirrors", origin))
        else:
            print
            mirror = str(item.text(0))
            origin = str(item.parent().text(0))
            print "%s %s" % (mirror, origin)
            sysconf.remove(("mirrors", origin), mirror)
        self.fill()

    def selectionChanged(self):
        item = self._treeview.selectedItems()
        self._delmirror.setEnabled(bool(item))

    def itemChanged(self, item, col):
        newtext = item.text(col)
        oldtext = item.oldtext(col)
        if not oldtext:
            return
        if not item.parent():
            if sysconf.has(("mirrors", str(newtext))):
                iface.error(_("Origin already exists!"))
            else:
                sysconf.move(("mirrors", str(oldtext)), ("mirrors", str(newtext)))
                
        else:
            origin = item.parent().text(0)
            if sysconf.has(("mirrors", str(origin)), str(newtext)):
                iface.error(_("Mirror already exists!"))
            else:
                sysconf.remove(("mirrors", str(origin)), oldtext)
                sysconf.add(("mirrors", str(origin)), str(newtext), unique=True)


class MirrorCreator(object):

    def __init__(self, parent=None):

        self._window = QtWidgets.QDialog(parent)
        self._window.setWindowIcon(QtGui.QIcon(getPixmap("smart")))
        self._window.setWindowTitle(_("New Mirror"))
        self._window.setModal(True)

        #self._window.setMinimumSize(600, 400)

        vbox = QtWidgets.QWidget(self._window)
        QtWidgets.QVBoxLayout(vbox)
        vbox.layout().setMargin(10)
        vbox.layout().setSpacing(10)
        vbox.show()

        table = QtWidgets.QWidget(vbox)
        QtWidgets.QGridLayout(table)
        table.layout().setSpacing(10)
        table.show()
        vbox.layout().addWidget(table)
        
        label = QtWidgets.QLabel(_("Origin URL:"), table)
        label.show()
        table.layout().addWidget(label)

        self._origin = QtWidgets.QLineEdit(table)
        self._origin.setMaxLength(40)
        self._origin.show()
        table.layout().addWidget(self._origin)

        label = QtWidgets.QLabel(_("Mirror URL:"), table)
        label.show()
        table.layout().addWidget(label)

        self._mirror = QtWidgets.QLineEdit(table)
        self._mirror.setMaxLength(40)
        self._mirror.show()
        table.layout().addWidget(self._mirror)

        sep = QtWidgets.QFrame(vbox)
        sep.setFrameStyle(QtWidgets.QFrame.HLine)
        sep.show()
        vbox.layout().addWidget(sep)

        bbox = QtWidgets.QWidget(self._window)
        QtWidgets.QHBoxLayout(bbox)
        bbox.layout().setSpacing(10)
        bbox.layout().addStretch(1)
        bbox.show()
        vbox.layout().addWidget(bbox)

        button = QtWidgets.QPushButton(_("OK"), bbox)
        button.clicked[()].connect(self._window.accept)
        bbox.layout().addWidget(button)

        button = QtWidgets.QPushButton(_("Cancel"), bbox)
        button.clicked[()].connect(self._window.reject)
        bbox.layout().addWidget(button)
        
        vbox.adjustSize()
        self._window.adjustSize()

    def show(self, origin="", mirror=""):

        self._origin.setText(origin)
        self._mirror.setText(mirror)
        origin = mirror = None

        self._window.show()
        self._window.raise_()

        while True:
            self._result = self._window.exec_()
            if self._result == QtWidgets.QDialog.Accepted:
                origin = str(self._origin.text()).strip()
                if not origin:
                    iface.error(_("No origin provided!"))
                    continue
                mirror = str(self._mirror.text()).strip()
                if not mirror:
                    iface.error(_("No mirror provided!"))
                    continue
                break
            origin = mirror = None
            break

        self._window.hide()

        return origin, mirror


