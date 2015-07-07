#-*- coding: utf-8 -*-
#
# Copyright (c) 2015 blackPanther OS - Charles Barcza
#
#
from smart.const import ERROR, WARNING, DEBUG
from smart.interfaces.qt5 import getPixmap
from smart import *
from PyQt5 import QtGui as QtGui, QtWidgets

from PyQt5 import QtCore as QtCore, QtWidgets

import locale

try:
    ENCODING = locale.getpreferredencoding()
except locale.Error:
    ENCODING = "C"

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtCore.QCoreApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtCore.QCoreApplication.translate(context, text, disambig)

class BackgroundScrollView(QtWidgets.QScrollArea):
    def __init__(self, parent):
        QtWidgets.QScrollArea.__init__(self, parent)
        self.setSizePolicy(
            QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))

    def drawContents(self, *args):
        if len(args)==1:
            return apply(QtWidgets.QFrame.drawContents, (self,)+args)
        else:
            painter, clipx, clipy, clipw, cliph = args
        color = self.eraseColor()
        painter.fillRect(clipx, clipy, clipw, cliph, QtGui.QBrush(color))
        QtWidgets.QScrollArea.drawContents(self, painter, clipx, clipy, clipw, cliph)

class QtLog(QtWidgets.QDialog):

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)

        self.setWindowIcon(QtGui.QIcon(getPixmap("smart")))
        self.setWindowTitle(_("Log"))
        self.setMinimumSize(400, 300)
        #self.setModal(True)

        layout = QtWidgets.QVBoxLayout(self)
        #layout.setResizeMode(QtGui.QLayout.FreeResize)

        self._vbox = QtWidgets.QWidget(self)
        QtWidgets.QVBoxLayout(self._vbox)
        self._vbox.layout().setMargin(10)
        self._vbox.layout().setSpacing(10)
        self._vbox.show()

        layout.addWidget(self._vbox)

        self._scrollview = BackgroundScrollView(self._vbox)

        #self._scrollview = QtGui.QScrollArea(self._vbox)
        self._scrollview.setGeometry(QtCore.QRect(5, 1, 380, 225))
        self._scrollview.setMinimumSize(QtCore.QSize(380, 225))
        self._scrollview.setFrameShape(QtWidgets.QFrame.Box)
        self._scrollview.setFrameShadow(QtWidgets.QFrame.Plain)
        self._scrollview.setLineWidth(0)
        self._scrollview.setMidLineWidth(0)
        self._scrollview.setWidgetResizable(True)
        self._scrollview.setObjectName(_fromUtf8("_scrollview"))
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 378, 223))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self._scrollview.setWidget(self.scrollAreaWidgetContents)

        self._vbox.layout().addWidget(self._scrollview)

        self._textview = QtWidgets.QLabel(self._scrollview.viewport())
        self._textview.setAlignment(QtCore.Qt.AlignTop)
        self._textview.setTextFormat(QtCore.Qt.LogText)
        self._textview.setAutoFillBackground(True)
        self._textview.setBackgroundRole(QtGui.QPalette.Base)
        self._textview.show()
        self._textview.adjustSize()
        
        #self._textview.setEraseColor(self._scrollview.eraseColor())
        self._scrollview.setWidget(self._textview)

        self._buttonbox = QtWidgets.QWidget(self._vbox)
        QtWidgets.QHBoxLayout(self._buttonbox)
        self._buttonbox.layout().setSpacing(10)
        self._buttonbox.layout().addStretch(1)
        self._buttonbox.show()
        self._buttonbox.setMinimumSize(QtCore.QSize(500, 50))
        self._vbox.layout().addWidget(self._buttonbox)

        self._clearbutton = QtWidgets.QPushButton(_("Clear"), self._buttonbox)
        self._clearbutton.show()
        self._clearbutton.clicked[()].connect(self.clearText)
        self._buttonbox.layout().addWidget(self._clearbutton)

        self._closebutton = QtWidgets.QPushButton(_("Close"), self._buttonbox)
        self._closebutton.show()
        self._closebutton.clicked[()].connect(self.hide)
        self._buttonbox.layout().addWidget(self._closebutton)

        self._closebutton.setDefault(True)


    def clearText(self):
	print "CLEAR"
        self._textview.clear()
    
    def isVisible(self):
        return QtWidgets.QDialog.isVisible(self)

    def message(self, level, msg):
        prefix = {ERROR: _("error"), WARNING: _("warning"),
                  DEBUG: _("debug")}.get(level)
        buffer = self._textview.text()
        if not isinstance(msg, unicode):
            msg = msg.decode(ENCODING)
        if prefix:
            for line in msg.split("\n"):
                buffer += "%s: %s\n" % (prefix, line)
        else:
            buffer += msg
        buffer += "\n"
        self._textview.setText(buffer)
        self._textview.adjustSize()

        if level == ERROR:
            response = QtWidgets.QMessageBox.critical(self, "", msg)
        else:
            self.show()
