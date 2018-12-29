# -*- coding: utf-8 -*-
#
import gettext
_ = gettext.gettext

import os
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import subprocess, sys
from fusionlogic.ScreenWidget import ScreenWidget
from fusionlogic.packagewizard.multipleinstallator import Ui_multipleInstallator

class Widget(QWidget, ScreenWidget):
    title = _("Package Installation")
    desc = _("Package Installation")

    def __init__(self, *args):
        QWidget.__init__(self,None)
        self.ui = Ui_multipleInstallator()
        self.ui.setupUi(self)
        

    def execute(self):
       return True
