#-*- coding: utf-8 -*-
#
# Copyright (c) 2015 blackPanther OS - Charles Barcza
# GPL
#
from smart.interfaces.qt5 import getPixmap
from smart import *
from PyQt5 import QtGui as QtGui, QtWidgets

from PyQt5 import QtCore as QtCore, QtWidgets


class QtLegend(QtWidgets.QDialog):

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)

        self.setWindowIcon(QtGui.QIcon(getPixmap("smart")))
        self.setWindowTitle(_("Icon Legend"))

        layout = QtWidgets.QVBoxLayout(self)

        self._vbox = QtWidgets.QWidget(self)
        QtWidgets.QVBoxLayout(self._vbox)
        self._vbox.layout().setMargin(10)
        self._vbox.layout().setSpacing(10)

        layout.addWidget(self._vbox)

        label = QtWidgets.QLabel("<b>" + _("The following icons are used to indicate\nthe current status of a package:").replace("\n", "<br>") + "</b>", self._vbox)
        label.show()
        self._vbox.layout().addWidget(label)

        grid = QtWidgets.QWidget(self)
        QtWidgets.QGridLayout(grid)
        grid.layout().setSpacing(5)
        grid.layout().setMargin(5)
        grid.layout().setColumnStretch(1, 1)
        grid.show()
        self._vbox.layout().addWidget(grid)
  
        row = 0
        for icon, legend in [
        (getPixmap("package-install"),            _("Marked for installation")),
        (getPixmap("package-reinstall"),          _("Marked for re-installation")),
        (getPixmap("package-upgrade"),            _("Marked for upgrade")),
        (getPixmap("package-downgrade"),          _("Marked for downgrade")),
        (getPixmap("package-remove"),             _("Marked for removal")),
        (getPixmap("package-available"),          _("Not installed")),
        (getPixmap("package-new"),                _("Not installed (new)")),
        (getPixmap("package-available-locked"),   _("Not installed (locked)")),
        (getPixmap("package-installed"),          _("Installed")),
        (getPixmap("package-installed-outdated"), _("Installed (upgradable)")),
        (getPixmap("package-installed-locked"),   _("Installed (locked)")),
        (getPixmap("package-broken"),             _("Broken")),
        ]:
            image = QtWidgets.QLabel("", grid)
            image.setPixmap(icon)
            image.show()
            grid.layout().addWidget(image, row, 0, QtCore.Qt.AlignLeft)
            label = QtWidgets.QLabel(legend, grid)
            label.show()
            grid.layout().addWidget(label, row, 1, QtCore.Qt.AlignLeft)
            row = row + 1
        
        self._buttonbox = QtWidgets.QWidget(self._vbox)
        QtWidgets.QHBoxLayout(self._buttonbox)
        self._buttonbox.layout().setSpacing(10)
        self._buttonbox.layout().addStretch(1)
        self._buttonbox.show()
        self._vbox.layout().addWidget(self._buttonbox)

        self._closebutton = QtWidgets.QPushButton(_("Close"), self._buttonbox)
        self._closebutton.show()
        self._closebutton.clicked[()].connect(self.hide)
        self._buttonbox.layout().addWidget(self._closebutton)

    def isVisible(self):
        return QtWidgets.QDialog.isVisible(self)

