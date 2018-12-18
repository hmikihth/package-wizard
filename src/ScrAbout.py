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
from fusionlogic.packagewizard.ScreenWidget import ScreenWidget
from fusionlogic.packagewizard.aboutWidget import Ui_aboutWidget

class Widget(QWidget, ScreenWidget):
    title = _("About")
    desc = _("Program Informations & Developers")

    def __init__(self, *args):
        QWidget.__init__(self,None)
        self.ui = Ui_aboutWidget()
        self.ui.setupUi(self)
        

    def execute(self):
       return True


