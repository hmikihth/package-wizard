#-*- coding: utf-8 -*-
#
# Copyright (c) 2015 blackPanther OS - Charles Barcza
# GPL
#
from smart.util.strtools import ShortURL, sizeToStr
from smart.progress import Progress, INTERVAL
from smart.interfaces.qt5 import getPixmap, centerWindow
from smart import *
from  PyQt5 import QtGui as QtGui
from PyQt5 import QtCore as QtCore

import posixpath
import thread
import time
import sys

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class QtProgress(Progress, QtGui.QDialog):

    def __init__(self, hassub, parent=None):
        Progress.__init__(self)
        QtGui.QDialog.__init__(self, parent)

        self._hassub = hassub
        self._shorturl = ShortURL(50)
        self._ticking = False
        self._stopticking = False
        self._fetcher = None

        self._beenshown = False
        self._mainthread = None

        if hassub:
            self.setMinimumSize(500, 400)
        else:
            self.setMinimumSize(300, 80)

        self.setWindowIcon(QtGui.QIcon(getPixmap("smart")))
        self.setWindowTitle(_("Operation Progress"))

        vbox = QtGui.QVBoxLayout(self)
        #vbox.setResizeMode(QtGui.QLayout.FreeResize)
        vbox.setMargin(10)
        vbox.setSpacing(10)

        self._topic = QtGui.QLabel(self)
        vbox.addWidget(self._topic)

        self._progressbar = QtGui.QProgressBar(self)
        #self._progressbar.setPercentageVisible(True)

        self._progressbar.setGeometry(QtCore.QRect(50, 50, 271, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._progressbar.sizePolicy().hasHeightForWidth())
        self._progressbar.setSizePolicy(sizePolicy)
        self._progressbar.setAutoFillBackground(False)
        self._progressbar.setProperty("value", 24)
        self._progressbar.setObjectName(_fromUtf8("progressBar"))
        #self.label = QtGui.QLabel(Dialog)
        #self.label.setGeometry(QtCore.QRect(50, 10, 91, 16))
        #self.label.setObjectName(_fromUtf8("label"))

        print "Progressbar: Show"
        self._progressbar.show()
        vbox.addWidget(self._progressbar)

        if hassub:
            self._listview = QtGui.QTableWidget(self)
            #self._listview.setSorting(-1, False);
            self._listview.setSelectionMode(QtGui.QTableView.NoSelection )
            self._listview.show()
            vbox.addWidget(self._listview)

            #column = self._listview.addColumn(_("Progress"))
            #self._listview.setColumnWidthMode(column, QtGui.QTableView.Manual)
            #self._listview.setColumnWidth(column, 55)
            #column = self._listview.addColumn(_("Current"))
            #self._currentcolumn = column
            #column = self._listview.addColumn(_("Total"))
            #self._totalcolumn = column
            #column = self._listview.addColumn(_("Speed"))
            #self._speedcolumn = column
            #column = self._listview.addColumn(_("ETA"))
            #self._etacolumn = column
            #column = self._listview.addColumn(_("Description"))
            #self._listview.setColumnWidthMode(column, QtGui.QTableView.Manual)
            #self._listview.setColumnWidth(column, 165)
            #self._desccolumn = column
            self._listview.setHorizontalHeaderLabels([_("Progress"),
                _("Current"), _("Total"), _("Speed"), _("ETA"), _("Description")])

            self._subiters = {}
            self._subindex = 0

            self._bbox = QtGui.QWidget(self)
            QtGui.QHBoxLayout(self._bbox)
            self._bbox.layout().setSpacing(10)
            self._bbox.layout().addStretch(1)
            vbox.addWidget(self._bbox)
            
            button = QtGui.QPushButton(_("Cancel"), self._bbox)
            button.show()
            QtCore.QObject.connect(button, QtCore.SIGNAL("clicked()"), self._cancel)
            self._bbox.layout().addWidget(button)

    def setFetcher(self, fetcher):
        if fetcher:
            self._bbox.show()
            self._fetcher = fetcher
        else:
            self._bbox.hide()
            self._fetcher = None

    def _cancel(self):
        if self._fetcher:
            self._fetcher.cancel()

    def setMainThread(self, main):
        self._mainthread = main

    def tick(self):
        while not self._stopticking:
            self.lock()
            ## Note: it's NOT safe to call processEvents from threads other than main
            #while QtGui.QCoreApplication.instance().hasPendingEvents():
            #    QtGui.QCoreApplication.instance().processEvents()
            self.unlock()
            time.sleep(INTERVAL)
        self._ticking = False

    def start(self):
        Progress.start(self)

        self.setHasSub(self._hassub)
        self._ticking = True
        self._stopticking = False
        if self._hassub:
            #self._listview.hideColumn(self._currentcolumn) 
            #self._listview.hideColumn(self._totalcolumn) 
            #self._listview.hideColumn(self._speedcolumn) 
            #self._listview.hideColumn(self._etacolumn) 
            pass

        thread.start_new_thread(self.tick, ())

    def stop(self):
        self._stopticking = True
        while self._ticking: pass

        Progress.stop(self)

        if self._hassub:
            self._listview.clear()
            self._subiters.clear()
            self._subindex = 0

        self._shorturl.reset()

        QtGui.QDialog.hide(self)

    def _currentThread(self):
        return QtCore.QThread.currentThread()

    def expose(self, topic, percent, subkey, subtopic, subpercent, data, done):
        if self._currentThread() != self._mainthread:
            # Note: it's NOT safe to use Qt from threads other than main
            return
            
        QtGui.QDialog.show(self)
        if not self._beenshown:
            centerWindow(self)
            self._beenshown = True
        self.raise_()
        
        if self._hassub and subkey:
            if subkey in self._subiters:
                iter = self._subiters[subkey]
            else:
                row = self._listview.rowCount()
                self._listview.insertRow(row)
                iter = []
                iter.append(QtGui.QTableWidgetItem())
                self._listview.setItem(row, 0, iter[0])
                iter.append(QtGui.QTableWidgetItem())
                self._listview.setItem(row, 1, iter[1])
                iter.append(QtGui.QTableWidgetItem())
                self._listview.setItem(row, 2, iter[2])
                iter.append(QtGui.QTableWidgetItem())
                self._listview.setItem(row, 3, iter[3])
                iter.append(QtGui.QTableWidgetItem())
                self._listview.setItem(row, 4, iter[4])
                iter.append(QtGui.QTableWidgetItem())
                self._listview.setItem(row, 5, iter[5])
                self._subiters[subkey] = iter
                #self._listview.ensureItemVisible(iter)

            current = data.get("current", "")
            if current:
                self._listview.setColumnWidth(self._currentcolumn, 110)
            total = data.get("total", "")
            if total:
                self._listview.setColumnWidth(self._totalcolumn, 110)
            if done:
                speed = ""
                eta = ""
                subpercent = 100
            else:
                speed = data.get("speed", "")
                if speed:
                    self._listview.setColumnWidth(self._speedcolumn, 110)
                eta = data.get("eta", "")
                if eta:
                    self._listview.setColumnWidth(self._etacolumn, 110)
            if current or total or speed or eta:
                iter[1].setText(current)
                iter[2].setText(total)
                iter[3].setText(speed)
                iter[4].setText(eta)
                subtopic = self._shorturl.get(subtopic)
            iter[0].setText(str(subpercent) + "%")
            iter[5].setText(subtopic)
            #iter.widthChanged(self._desccolumn)
        else:
            self._topic.setText('<b>'+topic+'</b>')
            self._progressbar.setValue(percent)
            if self._hassub:
                self._listview.update()

        while QtGui.QCoreApplication.instance().hasPendingEvents():
            QtGui.QCoreApplication.instance().processEvents()


def test():
    import sys, time

    prog = QtProgress(True)
    prog.setMainThread(QtCore.QThread.currentThread())
        
    data = {"item-number": 0}
    total, subtotal = 100, 100
    prog.start()
    prog.setTopic("Installing packages...")
    for n in range(1,total+1):
        data["item-number"] = n
        prog.set(n, total)
        prog.setSubTopic(n, "package-name%d" % n)
        for i in range(0,subtotal+1):
            prog.setSub(n, i, subtotal, subdata=data)
            prog.show()
            while QtGui.QCoreApplication.instance().hasPendingEvents():
                QtGui.QCoreApplication.instance().processEvents()
            time.sleep(0.01)
    prog.stop()


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    test()


