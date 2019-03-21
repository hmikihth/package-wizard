#*********************************************************************************************************
#*   __     __               __     ______                __   __                      _______ _______   *
#*  |  |--.|  |.---.-..----.|  |--.|   __ \.---.-..-----.|  |_|  |--..-----..----.    |       |     __|  *
#*  |  _  ||  ||  _  ||  __||    < |    __/|  _  ||     ||   _|     ||  -__||   _|    |   -   |__     |  *
#*  |_____||__||___._||____||__|__||___|   |___._||__|__||____|__|__||_____||__|      |_______|_______|  *
#*http://www.blackpantheros.eu | http://www.blackpanther.hu - kbarcza[]blackpanther.hu * Charles K Barcza*
#*************************************************************************************(c)2002-2019********
#	Design, FugionLogic idea and Initial code written by Charles K Barcza in december of 2018 
#       The maintainer of the PackageWizard: Miklos Horvath * hmiki[]blackpantheros.eu
#		(It's not allowed to delete this about label for free usage under GLP3)
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
from fusionlogic.packagewizard.errorsWidget import Ui_errorsWidget

class Widget(QWidget, ScreenWidget):
    title = _("Errors")
    desc = _("Errors")

    def __init__(self, *args):
        QWidget.__init__(self,None)
        self.ui = Ui_errorsWidget()
        self.ui.setupUi(self)
        
    def execute(self):
       return True
