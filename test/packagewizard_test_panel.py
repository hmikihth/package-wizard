#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'modules_uic/welcomeWidget.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class Ui_welcomeWidget(object):
    def setupUi(self, welcomeWidget):
        welcomeWidget.setObjectName("welcomeWidget")
        welcomeWidget.resize(569, 495)
        welcomeWidget.setStyleSheet("")
        self.gridLayout = QtWidgets.QGridLayout(welcomeWidget)
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.label = QtWidgets.QLabel(welcomeWidget)
        font = QtGui.QFont()
        font.setFamily("URW Gothic L")
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(welcomeWidget)
        self.label_2.setMinimumSize(QtCore.QSize(34, 0))
        font = QtGui.QFont()
        font.setFamily("FreeSans")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 2, 1, 1, QtCore.Qt.AlignTop)
        spacerItem1 = QtWidgets.QSpacerItem(25, 30, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 1, 3, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 50, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem2, 2, 1, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 30, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem3, 3, 0, 1, 1)
        self.labelProfilerIntro = QtWidgets.QLabel(welcomeWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelProfilerIntro.sizePolicy().hasHeightForWidth())
        self.labelProfilerIntro.setSizePolicy(sizePolicy)
        self.labelProfilerIntro.setMinimumSize(QtCore.QSize(351, 0))
        self.labelProfilerIntro.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("URW Gothic L")
        font.setPointSize(11)
        self.labelProfilerIntro.setFont(font)
        self.labelProfilerIntro.setStyleSheet("color: rgb(234, 225, 228);")
        self.labelProfilerIntro.setFrameShadow(QtWidgets.QFrame.Raised)
        self.labelProfilerIntro.setWordWrap(True)
        self.labelProfilerIntro.setObjectName("labelProfilerIntro")
        self.gridLayout.addWidget(self.labelProfilerIntro, 3, 1, 1, 2)
        spacerItem4 = QtWidgets.QSpacerItem(25, 30, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 3, 3, 1, 1)
        self.frame_3 = QtWidgets.QFrame(welcomeWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 90))
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_3.setObjectName("frame_3")
        self.labelStatus = QtWidgets.QLabel(self.frame_3)
        self.labelStatus.setGeometry(QtCore.QRect(400, 0, 90, 90))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelStatus.sizePolicy().hasHeightForWidth())
        self.labelStatus.setSizePolicy(sizePolicy)
        self.labelStatus.setMinimumSize(QtCore.QSize(90, 90))
        self.labelStatus.setMaximumSize(QtCore.QSize(90, 90))
        self.labelStatus.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.labelStatus.setAutoFillBackground(False)
        self.labelStatus.setStyleSheet("")
        self.labelStatus.setLineWidth(0)
        self.labelStatus.setText("")
        self.labelStatus.setPixmap(QtGui.QPixmap("module_gui/pics/logo2010.png"))
        self.labelStatus.setScaledContents(True)
        self.labelStatus.setOpenExternalLinks(False)
        self.labelStatus.setObjectName("labelStatus")
        self.frame_2 = QtWidgets.QFrame(self.frame_3)
        self.frame_2.setGeometry(QtCore.QRect(0, 40, 240, 40))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setMinimumSize(QtCore.QSize(240, 40))
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame_2.setObjectName("frame_2")
        self.checkAutostart = QtWidgets.QCheckBox(self.frame_2)
        self.checkAutostart.setGeometry(QtCore.QRect(10, 10, 221, 21))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkAutostart.sizePolicy().hasHeightForWidth())
        self.checkAutostart.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("URW Gothic L")
        font.setBold(True)
        font.setWeight(75)
        self.checkAutostart.setFont(font)
        self.checkAutostart.setObjectName("checkAutostart")
        self.frame = QtWidgets.QFrame(self.frame_3)
        self.frame.setGeometry(QtCore.QRect(0, 10, 411, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setFrameShape(QtWidgets.QFrame.HLine)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setObjectName("frame")
        self.gridLayout.addWidget(self.frame_3, 4, 1, 1, 2)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem5, 5, 1, 1, 1)

        self.retranslateUi(welcomeWidget)
        QtCore.QMetaObject.connectSlotsByName(welcomeWidget)

    def retranslateUi(self, welcomeWidget):
        _translate = QtCore.QCoreApplication.translate
        welcomeWidget.setWindowTitle(_translate("welcomeWidget", "Welcome"))
        self.label.setStyleSheet(_translate("welcomeWidget", "color: rgb(234, 225, 228);"))
        self.label.setText(_translate("welcomeWidget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'URW Gothic L\'; font-size:25pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:22pt;\">Welcome to blackPanther OS </span></p></body></html>"))
        self.label_2.setText(_translate("welcomeWidget", "v18.x"))
        self.labelProfilerIntro.setText(_translate("welcomeWidget", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'URW Gothic L\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">The blackPanther OS is a reliable, secure, fast and user friendly operating system. <br /><br />With blackPanther, you can connect to the internet, read your e-mails, work with your office documents, watch movies, play music, develop applications, play games and much more! <br /><br /><span style=\" font-weight:600;\">Wizard</span> will help you personalize your blackPanther workspace easily and quickly. Please click <span style=\" font-weight:600;\">next</span> in order to begin.</p></body></html>"))
        self.labelStatus.setToolTip(_translate("welcomeWidget", "blackPanther OS"))
        self.checkAutostart.setText(_translate("welcomeWidget", "Run Profiler on System Startup"))

class PackageWizard(QtWidgets.QWidget, Ui_welcomeWidget):
    def __init__(self):
        super().__init__()


app = QApplication(sys.argv)
packagewizard = PackageWizard()
packagewizard.setupUi(packagewizard)
packagewizard.show()
sys.exit(app.exec_())

