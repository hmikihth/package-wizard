#-*- coding: utf-8 -*-
#
# Copyright (c) 2015 blackPanther OS - Charles Barcza
# GPL
#
from smart.interfaces.qt5.packageview import QtPackageView
from smart.interfaces.qt5 import getPixmap, centerWindow
from smart.util.strtools import sizeToStr
from smart.report import Report
from smart import *
#import PyQt4.QtGui as QtGui
#import PyQt4.QtCore as QtCore
from PyQt5 import QtGui as QtGui, QtWidgets

from PyQt5 import QtCore as QtCore, QtWidgets

from PyQt5 import QtCore as QtWidgets, QtWidgets


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class QtChanges(QtWidgets.QDialog):

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)

        self.setWindowIcon(QtGui.QIcon(getPixmap("smart")))
        self.setWindowTitle(_("Change Summary"))
        self.setModal(True)
        self.resize(520, 250)
        #self.setMaximumSize(QtCore.QSize(520, 400))
        self.setMinimumSize(QtCore.QSize(520, 300))
        #self.setMinimumSize(500, 350)
        centerWindow(self)
        
        self._vbox = QtWidgets.QVBoxLayout(self)
        self._vbox.setContentsMargins(5, 5, 5, 5)
        self._vbox.setSpacing(5)

        # Label summary
        self._label = QtWidgets.QLabel(self)
        # Label style start
        self._label.setGeometry(QtCore.QRect(20, 220, 490, 35))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._label.sizePolicy().hasHeightForWidth())
        self._label.setSizePolicy(sizePolicy)
        self._label.setMinimumSize(QtCore.QSize(490, 30))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("FreeSans"))
        font.setPointSize(11)
        font.setBold(False)
        font.setWeight(50)
        self._label.setFont(font)
        self._label.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self._label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self._label.setFrameShadow(QtWidgets.QFrame.Raised)
        self._label.setLineWidth(2)
        self._label.setWordWrap(True)
        self._label.setMargin(7)
        self._label.setIndent(0)
        self._label.setObjectName(_fromUtf8("_label"))

        # Label style end

        self._vbox.addWidget(self._label)

        self._pv = QtPackageView(self)
        #self._pv.getTreeView().header().hide()
        self._pv.setExpandPackage(True)
        #self._pv.setExpandAll()
        self._pv.show()
        self._vbox.addWidget(self._pv)

        self._lineLabel = QtWidgets.QLabel(self)
        self._lineLabel.setGeometry(QtCore.QRect(10, 250, 500, 10))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._lineLabel.sizePolicy().hasHeightForWidth())
        self._lineLabel.setSizePolicy(sizePolicy)
        self._lineLabel.setMinimumSize(QtCore.QSize(500, 1))
        self._lineLabel.setMaximumSize(QtCore.QSize(16777215, 10))
        self._lineLabel.setMouseTracking(True)
        self._lineLabel.setToolTip(_fromUtf8("Information"))
        self._lineLabel.setWhatsThis(_fromUtf8("We will apply this changes on sytem..."))
        self._lineLabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self._lineLabel.setFrameShape(QtWidgets.QFrame.HLine)
        self._lineLabel.setFrameShadow(QtWidgets.QFrame.Plain)
        self._lineLabel.setLineWidth(1)
        self._lineLabel.setText(_fromUtf8(""))
        self._lineLabel.setAlignment(QtCore.Qt.AlignCenter)
        self._lineLabel.setWordWrap(False)
        self._lineLabel.setMargin(0)
        self._lineLabel.setIndent(0)
        self._lineLabel.setObjectName(_fromUtf8("_lineLabel"))
        self._vbox.addWidget(self._lineLabel)

        # Size Label

        self._sizelabel = QtWidgets.QLabel("", self)
        
        # Size Label Style start
        
        self._sizelabel.setGeometry(QtCore.QRect(10, 250, 500, 35))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._sizelabel.sizePolicy().hasHeightForWidth())
        self._sizelabel.setSizePolicy(sizePolicy)
        self._sizelabel.setMinimumSize(QtCore.QSize(500, 20))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("FreeSans"))
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self._sizelabel.setFont(font)
        self._sizelabel.setCursor(QtGui.QCursor(QtCore.Qt.WhatsThisCursor))
        self._sizelabel.setMouseTracking(True)
        self._sizelabel.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self._sizelabel.setFrameShadow(QtWidgets.QFrame.Plain)
        self._sizelabel.setLineWidth(2)
        self._sizelabel.setWordWrap(True)
        self._sizelabel.setMargin(5)
        self._sizelabel.setIndent(0)
        self._sizelabel.setObjectName(_fromUtf8("_sizelabel"))
        # Size Label Style end

        self._vbox.addWidget(self._sizelabel)

        self._confirmbbox = QtWidgets.QWidget(self)
        layout = QtWidgets.QHBoxLayout(self._confirmbbox)
        layout.setSpacing(10)
        layout.addStretch(1)
        #self._confirmbbox = QtGui.QWidget(self)
        #self._confirmbbox.setGeometry(QtCore.QRect(20, 210, 351, 80))
        #self._confirmbbox.setObjectName("widget")
        self._confirmbbox.setMinimumSize(QtCore.QSize(500, 50))

        self._vbox.addWidget(self._confirmbbox)

#        self.frame = QtWidgets.QFrame(Dialog)
#        self.frame.setGeometry(QtCore.QRect(10, 230, 361, 61))
#        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
#        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
#        self.frame.setObjectName("frame")

        self._okbutton = QtWidgets.QPushButton(_("OK"), self._confirmbbox)
        self._okbutton.setGeometry(QtCore.QRect(10, 10, 90, 26))
        self._okbutton.setObjectName(_fromUtf8("_okbutton"))
#        self._okbutton.setGeometry(QtCore.QRect(10, 20, 90, 26))
        self._okbutton.clicked[()].connect(self.accept)
        self._cancelbutton = QtWidgets.QPushButton(_("Cancel"), self._confirmbbox)
        self._cancelbutton.setGeometry(QtCore.QRect(110, 10, 90, 26))
        #self._cancelbutton.setGeometry(QtCore.QRect(110, 20, 90, 26))
        self._cancelbutton.setObjectName(_fromUtf8("_cancelbutton"))
        self._cancelbutton.clicked[()].connect(self.reject)

        self._closebbox = QtWidgets.QWidget(self)
        layout = QtWidgets.QHBoxLayout(self._closebbox)
        layout.setSpacing(10)
        layout.addStretch(1)
        self._vbox.addWidget(self._closebbox)

        self._closebutton = QtWidgets.QPushButton(_("Close"), self._closebbox)
        self._closebutton.clicked[()].connect(self.close)
        
    def showChangeSet(self, changeset, keep=None, confirm=False, label=None):

        report = Report(changeset)
        report.compute()
        
        class Sorter(unicode):
            ORDER = [_("Remove"), _("Downgrade"), _("Reinstall"),
                     _("Install"), _("Upgrade")]
            def _index(self, s):
                i = 0
                for os in self.ORDER:
                    if os.startswith(s):
                        return i
                    i += 1
                return i
            def __cmp__(self, other):
                return cmp(self._index(unicode(self)), self._index(unicode(other)))
            def __lt__(self, other):
                return cmp(self, other) < 0

        packages = {}

        if report.install:
            install = {}
            reinstall = {}
            upgrade = {}
            downgrade = {}
            lst = report.install.keys()
            lst.sort()
            for pkg in lst:
                package = {}
                done = {}
                if pkg in report.upgrading:
                    for upgpkg in report.upgrading[pkg]:
                        package.setdefault(_("Upgrades"), []).append(upgpkg)
                        done[upgpkg] = True
                if pkg in report.downgrading:
                    for dwnpkg in report.downgrading[pkg]:
                        package.setdefault(_("Downgrades"), []).append(dwnpkg)
                        done[dwnpkg] = True
                if pkg in report.requires:
                    for reqpkg in report.requires[pkg]:
                        package.setdefault(_("Requires"), []).append(reqpkg)
                if pkg in report.requiredby:
                    for reqpkg in report.requiredby[pkg]:
                        package.setdefault(_("Required By"), []).append(reqpkg)
                if pkg in report.conflicts:
                    for cnfpkg in report.conflicts[pkg]:
                        if cnfpkg in done:
                            continue
                        package.setdefault(_("Conflicts"), []).append(cnfpkg)
                if pkg.installed:
                    reinstall[pkg] = package
                elif pkg in report.upgrading:
                    upgrade[pkg] = package
                elif pkg in report.downgrading:
                    downgrade[pkg] = package
                else:
                    install[pkg] = package
            if reinstall:
                packages[Sorter(_("Reinstall (%d)") % len(reinstall))] = reinstall
            if install:
                packages[Sorter(_("Install (%d)") % len(install))] = install
            if upgrade:
                packages[Sorter(_("Upgrade (%d)") % len(upgrade))] = upgrade
            if downgrade:
                packages[Sorter(_("Downgrade (%d)") % len(downgrade))] = downgrade

        if report.removed:
            remove = {}
            lst = report.removed.keys()
            lst.sort()
            for pkg in lst:
                package = {}
                done = {}
                if pkg in report.requires:
                    for reqpkg in report.requires[pkg]:
                        package.setdefault(_("Requires"), []).append(reqpkg)
                if pkg in report.requiredby:
                    for reqpkg in report.requiredby[pkg]:
                        package.setdefault(_("Required By"), []).append(reqpkg)
                if pkg in report.conflicts:
                    for cnfpkg in report.conflicts[pkg]:
                        if cnfpkg in done:
                            continue
                        package.setdefault(_("Conflicts"), []).append(cnfpkg)
                remove[pkg] = package
            if remove:
                packages[Sorter(_("Remove (%d)") % len(report.removed))] = remove

        if keep:
            packages[Sorter(_("Keep (%d)") % len(keep))] = keep

        dsize = report.getDownloadSize()
        size = report.getInstallSize() - report.getRemoveSize()
        sizestr = ""
        if dsize:
            sizestr += _("%s of package files are needed. ") % sizeToStr(dsize)
        if size > 0:
            sizestr += _("%s will be used.") % sizeToStr(size)
        elif size < 0:
            size *= -1
            sizestr += _("%s will be freed.") % sizeToStr(size)
        if dsize or size:
            self._sizelabel.setText(sizestr)
            self._sizelabel.show()
        else:
            self._sizelabel.hide()

        if confirm:
            self._confirmbbox.show()
            self._closebbox.hide()
            self._okbutton.setDefault(True)
        else:
            self._closebbox.show()
            self._confirmbbox.hide()
            self._closebutton.setDefault(True)

        if label:
            self._label.set_text(label)
            self._label.show()
        else:
            self._label.hide()

        self._pv.setPackages(packages, changeset)

        # Expand first level
        self._pv.setExpanded([(x,) for x in packages])

        self._result = False
        self.show()
        dialogResult = self.exec_()
        self._result = (dialogResult == QtWidgets.QDialog.Accepted)

        return self._result


