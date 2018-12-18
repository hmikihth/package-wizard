# -*- coding: utf-8 -*-
#
import gettext
_ = gettext.gettext

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from fusionlogic.packagewizard.ScreenWidget import ScreenWidget
from fusionlogic.packagewizard.welcomeWidget import Ui_welcomeWidget

import os, shutil, subprocess

class Widget(QWidget, ScreenWidget):
    title = _("Welcome")
    desc = _("Welcome to Package Wizard")

    def __init__(self, *args):
        QWidget.__init__(self,None)
        self.ui = Ui_welcomeWidget()
        self.ui.setupUi(self)

        self.release = self.getRelease().split()[0] + " " + self.getRelease().split()[1]
        self.ext = ""

        if self.release.__len__() > 2:
            self.ext = self.getRelease().split()[3]

        #welcomeStr = "Welcome to " + self.release + " " + self.ext
        relStr = self.ext
        self.ui.label_2.setText(relStr)

    def getRelease(self):
        try:
            p = subprocess.Popen(["cat","/etc/blackPanther-release"], stdout=subprocess.PIPE)
            release, err = p.communicate()
            return str(release)

        except:
            return "blackPanther OS"

        self.autofile = os.path.expanduser("~/.config/autostart/blackPanther-profiler.desktop")
        self.gautofile = "/usr/share/applications/blackPanther-profiler.desktop"

        self.ui.checkAutostart.setChecked(True)

    def shown(self):
        pass
