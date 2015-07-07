#-*- coding: utf-8 -*-
#
# Copyright (c) 2015 blackPanther OS - Charles Barcza
# GPL
#
from smart.interfaces.qt5 import getPixmap, centerWindow
from smart import *
from PyQt5 import QtGui as QtGui, QtWidgets

from PyQt5 import QtCore as QtCore, QtWidgets

import re

TARGETRE = re.compile(r"^\s*(\S+?)\s*(?:([<>=]+)\s*(\S+))?\s*$")

class QtFlags(object):

    def __init__(self, parent=None):

        self._window = QtWidgets.QDialog(None)
        self._window.setWindowIcon(QtGui.QIcon(getPixmap("smart")))
        self._window.setWindowTitle(_("Flags"))
        self._window.setModal(True)
        
        self._window.setMinimumSize(600, 400)

        layout = QtWidgets.QVBoxLayout(self._window)
        #layout.setResizeMode(QtGui.QLayout.FreeResize)

        topvbox = QtWidgets.QWidget(self._window)
        QtWidgets.QVBoxLayout(topvbox)
        topvbox.layout().setMargin(10)
        topvbox.layout().setSpacing(10)
        topvbox.show()

        layout.addWidget(topvbox)

        tophbox = QtWidgets.QWidget(topvbox)
        QtWidgets.QHBoxLayout(tophbox)
        tophbox.layout().setSpacing(20)
        tophbox.show()
        topvbox.layout().addWidget(tophbox)

        # Left side
        vbox = QtWidgets.QGroupBox(tophbox)
        QtWidgets.QVBoxLayout(vbox)
        vbox.layout().setSpacing(10)
        vbox.show()
        tophbox.layout().addWidget(vbox)

        self._flagsview = QtWidgets.QTableWidget(vbox)
        self._flagsview.show()
        vbox.layout().addWidget(self._flagsview)

        self._flagsview.selectionChanged.connect(self.flagSelectionChanged)

        #self._flagsview.addColumn(_("Flags"))
        self._flagsview.setHorizontalHeaderLabels([_("Flags")])
        self._flagsview.horizontalHeader().show()

        #bbox = QtGui.QHBox(vbox)
        bbox = QtWidgets.QWidget(vbox)
        QtWidgets.QHBoxLayout(bbox)
        bbox.layout().setMargin(5)
        bbox.layout().setSpacing(10)
        bbox.show()
        vbox.layout().addWidget(bbox)

        button = QtWidgets.QPushButton(_("New"), bbox)
        button.setEnabled(True)
        button.setIcon(QtGui.QIcon(getPixmap("crystal-add")))
        button.show()
        button.clicked[()].connect(self.newFlag)
        self._newflag = button
        bbox.layout().addWidget(button)

        button = QtWidgets.QPushButton(_("Delete"), bbox)
        button.setEnabled(False)
        button.setIcon(QtGui.QIcon(getPixmap("crystal-delete")))
        button.show()
        button.clicked[()].connect(self.delFlag)
        self._delflag = button
        bbox.layout().addWidget(button)

        # Right side
        vbox = QtWidgets.QGroupBox(tophbox)
        QtWidgets.QVBoxLayout(vbox)
        vbox.layout().setSpacing(10)
        vbox.show()
        tophbox.layout().addWidget(vbox)

        self._targetsview = QtWidgets.QTableWidget(vbox)
        self._targetsview.show()
        vbox.layout().addWidget(self._targetsview)

        self._targetsview.selectionChanged.connect(self.targetSelectionChanged)

        #self._targetsview.addColumn(_("Targets"))
        self._targetsview.setHorizontalHeaderLabels([_("Targets")])
        self._targetsview.horizontalHeader().show()

        bbox = QtWidgets.QWidget(vbox)
        QtWidgets.QHBoxLayout(bbox)
        bbox.layout().setMargin(5)
        bbox.layout().setSpacing(10)
        bbox.show()
        vbox.layout().addWidget(bbox)

        button = QtWidgets.QPushButton(_("New"), bbox)
        button.setEnabled(False)
        button.setIcon(QtGui.QIcon(getPixmap("crystal-add")))
        button.show()
        button.clicked[()].connect(self.newTarget)
        self._newtarget = button
        bbox.layout().addWidget(button)

        button = QtWidgets.QPushButton(_("Delete"), bbox)
        button.setEnabled(False)
        button.setIcon(QtGui.QIcon(getPixmap("crystal-delete")))
        button.show()
        button.clicked[()].connect(self.delTarget)
        self._deltarget = button
        bbox.layout().addWidget(button)


        # Bottom
        sep = QtWidgets.QFrame(topvbox)
        sep.setFrameShape(QtWidgets.QFrame.HLine)
        sep.setFrameShadow(QtWidgets.QFrame.Sunken)
        sep.show()
        topvbox.layout().addWidget(sep)

        bbox = QtWidgets.QWidget(topvbox)
        QtWidgets.QHBoxLayout(bbox)
        bbox.layout().setSpacing(10)
        bbox.layout().addStretch(1)
        bbox.show()
        topvbox.layout().addWidget(bbox)

        button = QtWidgets.QPushButton(_("Close"), bbox)
        button.show()
        button.clicked[()].connect(self._window.accept)
        bbox.layout().addWidget(button)
        
        button.setDefault(True)

    def fillFlags(self):
        self._flagsview.clear()
        flaglst = pkgconf.getFlagNames()
        flaglst.sort()
        for flag in flaglst:
            item = QtWidgets.QTableWidgetItem()
            item.setText(flag)
            self._flagsview.setItem(self._flagsview.rowCount(), 0, item)
    
    def fillTargets(self):
        self._targetsview.clear()
        if self._flag:
            names = pkgconf.getFlagTargets(self._flag)
            namelst = names.keys()
            namelst.sort()
            for name in namelst:
                for relation, version in names[name]:
                    if relation and version:
                        item = QtWidgets.QTableWidgetItem(self._targetsview)
                        item.setText(0, "%s %s %s" % (name, relation, version))
                    else:
                        QtWidgets.QTableWidgetItem(self._targetsview).setText(0, name)

    def show(self):
        self.fillFlags()
        self._window.show()
        centerWindow(self._window)
        self._window.raise_()
        self._window.exec_()
        self._window.hide()

    def newFlag(self):
        flag = FlagCreator(self._window).show()
        if flag:
            if pkgconf.flagExists(flag):
                iface.error(_("Flag already exists!"))
            else:
                pkgconf.createFlag(flag)
                self.fillFlags()

    def newTarget(self):
        target = TargetCreator(self._window).show()
        if target:
            m = TARGETRE.match(target)
            if m:
                name, relation, version = m.groups()
                pkgconf.setFlag(self._flag, name, relation, version)
            self.fillTargets()

    def delFlag(self):
        item = self._flagsview.selectedItem()
        if item:
            pkgconf.clearFlag(self._flag)
            self.fillFlags()
            self.fillTargets()

    def delTarget(self):
        item = self._targetsview.selectedItem()
        if item:
            target = str(item.text(0))
            m = TARGETRE.match(target)
            if not m:
                iface.error(_("Invalid target!"))
            else:
                name, relation, version = m.groups()
                pkgconf.clearFlag(self._flag, name, relation, version)
                if not pkgconf.flagExists(self._flag):
                    self.fillFlags()
                else:
                    self.fillTargets()

    def flagEdited(self, cell, row, newtext):
        model = self._flagsmodel
        iter = model.get_iter_from_string(row)
        oldtext = model.get_value(iter, 0)
        if newtext != oldtext:
            if pkgconf.flagExists(newtext):
                iface.error(_("Flag already exists!"))
            else:
                pkgconf.renameFlag(oldtext, newtext)
                model.set_value(iter, 0, newtext)

    def targetEdited(self, cell, row, newtext):
        model = self._targetsmodel
        iter = model.get_iter_from_string(row)
        oldtext = model.get_value(iter, 0)
        if newtext != oldtext:
            m = TARGETRE.match(oldtext)
            if not m:
                iface.error(_("Invalid target!"))
            else:
                oldname, oldrelation, oldversion = m.groups()
                m = TARGETRE.match(newtext)
                if not m:
                    iface.error(_("Invalid target!"))
                else:
                    newname, newrelation, newversion = m.groups()
                    pkgconf.clearFlag(self._flag, oldname,
                                      oldrelation, oldversion)
                    pkgconf.setFlag(self._flag, newname,
                                    newrelation, newversion)
                    if newrelation and newversion:
                        model.set_value(iter, 0, "%s %s %s" %
                                        (newname, newrelation, newversion))
                    else:
                        model.set_value(iter, 0, newname)

    def flagSelectionChanged(self):
        item = self._flagsview.selectedItem()
        self._delflag.setEnabled(bool(item))
        self._newtarget.setEnabled(bool(item))
        if item:
            self._flag = str(item.text(0))
        else:
            self._flag = None
        self.fillTargets()

    def targetSelectionChanged(self):
        item = self._targetsview.selectedItem()
        self._deltarget.setEnabled(bool(item))

class FlagCreator(object):

    def __init__(self, parent=None):

        self._window = QtWidgets.QDialog(parent)
        self._window.setWindowIcon(QtGui.QIcon(getPixmap("smart")))
        self._window.setWindowTitle(_("New Flag"))
        self._window.setModal(True)

        #self._window.setMinimumSize(600, 400)

        vbox = QtWidgets.QWidget(self._window)
        QtWidgets.QVBoxLayout(vbox)
        vbox.layout().setMargin(10)
        vbox.layout().setSpacing(10)
        vbox.show()

        table = QtWidgets.QWidget(vbox) # 2
        QtWidgets.QGridLayout(table)
        table.layout().setSpacing(10)
        
        label = QtWidgets.QLabel(_("Name:"), table)

        self._flag = QtWidgets.QLineEdit(table)
        self._flag.setMaxLength(20)
        self._flag.show()

        sep = QtWidgets.QFrame(vbox)
        sep.setFrameShape(QtWidgets.QFrame.HLine)
        sep.setFrameShadow(QtWidgets.QFrame.Sunken)
        sep.show()

        bbox = QtGui.QHBox(vbox)
        QtWidgets.QHBoxLayout(bbox)
        bbox.layout().setSpacing(10)
        bbox.layout().addStretch(1)
        bbox.show()

        button = QtWidgets.QPushButton(bbox.tr("OK"), bbox)
        button.clicked[()].connect(self._window.accept)

        button = QtWidgets.QPushButton(bbox.tr("Cancel"), bbox)
        button.clicked[()].connect(self._window.reject)

        vbox.adjustSize()
        self._window.adjustSize()

    def show(self):

        self._window.show()
        self._window.raise_()
        self._window.activate()

        while True:
            self._result = self._window.exec_()
            if self._result == QtWidgets.QDialog.Accepted:
                flag = str(self._flag.text()).strip()
                if not flag:
                    iface.error(_("No flag name provided!"))
                    continue
                break
            flag = None
            break

        self._window.hide()

        return flag

class TargetCreator(object):

    def __init__(self, parent=None):

        self._window = QtWidgets.QDialog(parent)
        self._window.setWindowIcon(QtGui.QIcon(getPixmap("smart")))
        self._window.setWindowTitle(_("New Target"))
        self._window.setModal(True)

        #self._window.setMinimumSize(600, 400)

        vbox = QtWidgets.QWidget(self._window)
        QtWidgets.QVBoxLayout(vbox)
        vbox.layout().setMargin(10)
        vbox.layout().setSpacing(10)
        vbox.show()

        table = QtWidgets.QWidget(vbox) # 2
        QtWidgets.QGridLayout(table)
        table.layout().setSpacing(10)
        table.show()
        
        label = QtWidgets.QLabel(_("Target:"), table)

        self._target = QtWidgets.QLineEdit(table)
        self._target.setMaxLength(40)
        self._target.show()

        blank = QtWidgets.QWidget(table)

        label = QtWidgets.QLabel(_("Examples: \"pkgname\", \"pkgname = 1.0\" or "
                            "\"pkgname <= 1.0\""), table)

        sep = QtWidgets.QFrame(vbox)
        sep.setFrameShape(QtWidgets.QFrame.HLine)
        sep.setFrameShadow(QtWidgets.QFrame.Sunken)
        sep.show()

        bbox = QtWidgets.QWidget(vbox)
        QtWidgets.QHBoxLayout(bbox)
        bbox.layout().setSpacing(10)
        bbox.layout().addStretch(1)
        bbox.show()

        button = QtWidgets.QPushButton(bbox.tr("OK"), bbox)
        button.clicked[()].connect(self._window.accept)

        button = QtWidgets.QPushButton(bbox.tr("Cancel"), bbox)
        button.clicked[()].connect(self._window.reject)

        vbox.adjustSize()
        self._window.adjustSize()

    def show(self):

        self._window.show()
        self._window.raise_()
        self._window.activateWindow()

        while True:
            self._result = self._window.exec_loop()
            if self._result == QtWidgets.QDialog.Accepted:
                target = str(self._target.text()).strip()
                if not target:
                    iface.error(_("No target provided!"))
                    continue
                if ('"' in target or ',' in target or
                    not TARGETRE.match(target)):
                    iface.error(_("Invalid target!"))
                    continue
                break
            target = None
            break

        self._window.hide()

        return target


