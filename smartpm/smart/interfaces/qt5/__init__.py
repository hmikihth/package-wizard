#-*- coding: utf-8 -*-
#
# Copyright (c) 2015 blackPanther OS - Charles Barcza
# GPL
#
from smart.interface import getImagePath
from smart import *
import os

try:
    from PyQt5 import QtCore, QtGui, QtWidgets

except ImportError:
    from smart.const import DEBUG
    if sysconf.get("log-level") == DEBUG:
        import traceback
        traceback.print_exc()
    raise Error, _("System has no support for qt python interface")

def create(ctrl, command=None, argv=None):
    if command:
        from smart.interfaces.qt5.command import QtCommandInterface
        return QtCommandInterface(ctrl)
    else:
        from smart.interfaces.qt5.interactive import QtInteractiveInterface
        return QtInteractiveInterface(ctrl)


_pixmap = {}

def getPixmap(name):
    if name not in _pixmap:
        filename = getImagePath(name)
        if os.path.isfile(filename):
            pixmap = QtGui.QPixmap(filename)
            _pixmap[name] = pixmap
        else:
            raise Error, _("Image '%s' not found") % name
    return _pixmap[name]

def centerWindow(window):
    w = window.topLevelWidget()
    if w:
        scrn = QtWidgets.QApplication.desktop().screenNumber(w)
    elif QtWidgets.QApplication.desktop().isVirtualDesktop():
        scrn = QtWidgets.QApplication.desktop().screenNumber(QtGui.QCursor.pos())
    else:
        scrn = QtWidgets.QApplication.desktop().screenNumber(window)
    desk = QtWidgets.QApplication.desktop().availableGeometry(scrn)
    window.move((desk.width() - window.frameGeometry().width()) / 2, \
                (desk.height() - window.frameGeometry().height()) / 2)

