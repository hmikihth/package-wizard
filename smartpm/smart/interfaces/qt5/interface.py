#-*- coding: utf-8 -*-
#
# Copyright (c) 2015 blackPanther OS - Charles Barcza
# GPL
#
from smart.interfaces.qt5.progress import QtProgress
from smart.interfaces.qt5.changes import QtChanges
from smart.interfaces.qt5.log import QtLog
from smart.interface import Interface, getScreenWidth
from smart.fetcher import Fetcher
from smart.const import DEBUG
from smart import *
from PyQt5 import QtGui as QtGui, QtWidgets

from PyQt5 import QtCore as QtCore, QtWidgets

import sys


app = QtWidgets.QApplication(sys.argv)

class QtInterface(Interface):

    def __init__(self, ctrl, argv):
        Interface.__init__(self, ctrl)
        self._log = QtLog()
        self._progress = QtProgress(False)
        self._hassubprogress = QtProgress(True)
        self._changes = QtChanges()
        self._window = None
        self._sys_excepthook = sys.excepthook

    def run(self, command=None, argv=None):
        self.setCatchExceptions(True)
        result = Interface.run(self, command, argv)
        self.setCatchExceptions(False)
        return result

    def eventsPending(self):
        return QtGui.QCoreApplication.instance().hasPendingEvents()
    
    def processEvents(self):
        QtGui.QCoreApplication.instance().processEvents(QtCore.QEventLoop.AllEvents)

    def getProgress(self, obj, hassub=False):
        if hassub:
            self._progress.hide()
            fetcher = isinstance(obj, Fetcher) and obj or None
            self._hassubprogress.setFetcher(fetcher)
            return self._hassubprogress
        else:
            self._hassubprogress.hide()
            return self._progress

    def getSubProgress(self, obj):
        return self._hassubprogress

    def askYesNo(self, question, default=False):
        response = QtWidgets.QMessageBox.question(self._window,
                                        _("Question..."),
                                        question,
                                        QtWidgets.QMessageBox.Yes,
                                        QtWidgets.QMessageBox.No)


        if response == QtWidgets.QMessageBox.Yes:
            return True
        elif response == QtWidgets.QMessageBox.No:
            return False
        else:
            return default

    def askContCancel(self, question, default=False):
        response = QtWidgets.QMessageBox.question(self._window,
                                   _("Question..."),
                                   question,
                                   _("Continue"),
                                   _("Cancel"),
                                   )

        #response.setButtonText(QMessageBox.Ok, )
        
        if response == 0:
            return True
        elif response == 1:
            return False
        else:
            return default

    def askOkCancel(self, question, default=False):
        response = QtWidgets.QMessageBox.question(self._window,
                                   _("Question..."),
                                   question,
                                   QtWidgets.QMessageBox.Ok,
                                   QtWidgets.QMessageBox.Cancel)

        
        if response == QtWidgets.QMessageBox.Ok:
            return True
        elif response == QtWidgets.QMessageBox.Cancel:
            return False
        else:
            return default

    def askInput(self, prompt, message=None, widthchars=40, echo=True):
        if (message != None):
            stringToShow = message + "\n" + prompt
        else:
            stringToShow = prompt
        if echo:
            echoMode = QtWidgets.QLineEdit.Normal
        else:
            echoMode = QtWidgets.QLineEdit.Password

        text, ok = QtWidgets.QInputDialog.getText(None, _("Input"), stringToShow, echoMode)
                
        if (ok and text != None):
            return text[0:widthchars]
        else:
            return ""

    def insertRemovableChannels(self, channels):
        question = _("Insert one or more of the following removable "
                     "channels:\n")
        question += "\n"
        for channel in channels:
            question += "    "
            question += channel.getName()
            question += "\n"
        return self.askOkCancel(question, default=True)

    def message(self, level, msg):
        self._log.message(level, msg)

    def confirmChange(self, oldchangeset, newchangeset, expected=1):
        changeset = newchangeset.difference(oldchangeset)
        keep = []
        for pkg in oldchangeset:
            if pkg not in newchangeset:
                keep.append(pkg)
        if len(keep)+len(changeset) <= expected:
            return True
        return self._changes.showChangeSet(changeset, keep=keep, confirm=True)

    def confirmChangeSet(self, changeset):
        return self._changes.showChangeSet(changeset, confirm=True)

    # Non-standard interface methods

    def _excepthook(self, type, value, tb):
        if issubclass(type, Error) and not sysconf.get("log-level") is DEBUG:
            self._hassubprogress.hide()
            self._progress.hide()
            iface.error(unicode(value[0]))
        else:
            import traceback
            lines = traceback.format_exception(type, value, tb)
            iface.error("\n".join(lines))

    def setCatchExceptions(self, flag):
        if flag:
            sys.excepthook = self._excepthook
        else:
            sys.excepthook = self._sys_excepthook

    def hideProgress(self):
        self._progress.hide()
        self._hassubprogress.hide()



