# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'modules_uic/packagewizardMain.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
#from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QApplication)
import sys


class Ui_packagewizardUI(object):
    def setupUi(self, packagewizardUI):
        packagewizardUI.setObjectName("packagewizardUI")
        packagewizardUI.resize(790, 570)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(packagewizardUI.sizePolicy().hasHeightForWidth())
        packagewizardUI.setSizePolicy(sizePolicy)
        packagewizardUI.setMinimumSize(QtCore.QSize(790, 570))
        packagewizardUI.setMaximumSize(QtCore.QSize(790, 570))
        font = QtGui.QFont()
        font.setFamily("URW Gothic L")
        font.setPointSize(10)
        packagewizardUI.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/raw/pics/cr64-app-profiler.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        packagewizardUI.setWindowIcon(icon)
        packagewizardUI.setStyleSheet("#packagewizard{\n"
"    background-image: url(:/raw/pics/bg.png);\n"
"       background-repeat: no-repeat;\n"
"       background-position: left top;\n"
"       background-color: #642437;\n"
"       alternate-background-color: gray;\n"
"       selection-background-color: gray;\n"
"}\n"
"")
        self.gridLayout_3 = QtWidgets.QGridLayout(packagewizardUI)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.packagewizard = QtWidgets.QWidget(packagewizardUI)
        self.packagewizard.setObjectName("packagewizard")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.packagewizard)
        self.gridLayout_2.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_2.setSpacing(6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.labelMenu = QtWidgets.QLabel(self.packagewizard)
        font = QtGui.QFont()
        font.setFamily("URW Gothic L")
        font.setPointSize(11)
        self.labelMenu.setFont(font)
        self.labelMenu.setAutoFillBackground(False)
        self.labelMenu.setStyleSheet("color: rgb(36, 42, 58);\n"
"padding-top: 10px;")
        self.labelMenu.setLineWidth(2)
        self.labelMenu.setText("")
        self.labelMenu.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.labelMenu.setIndent(20)
        self.labelMenu.setObjectName("labelMenu")
        self.gridLayout.addWidget(self.labelMenu, 1, 0, 3, 2)
        spacerItem = QtWidgets.QSpacerItem(180, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 80, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout.addItem(spacerItem1, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.mainStack = QtWidgets.QStackedWidget(self.packagewizard)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.mainStack.sizePolicy().hasHeightForWidth())
        self.mainStack.setSizePolicy(sizePolicy)
        self.mainStack.setStyleSheet("QStackedWidget#mainStack{background-color:rgba(255, 255, 255,0);\n"
"margin: 0px;\n"
"border-radius: 0px;\n"
"color: white;\n"
"}")
        self.mainStack.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.mainStack.setFrameShadow(QtWidgets.QFrame.Plain)
        self.mainStack.setLineWidth(0)
        self.mainStack.setObjectName("mainStack")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.mainStack.addWidget(self.page)
        self.verticalLayout_4.addWidget(self.mainStack)
        self.gridLayout_2.addLayout(self.verticalLayout_4, 0, 1, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(0, 0, -1, 0)
        self.horizontalLayout_2.setSpacing(1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.buttonCancel = QtWidgets.QPushButton(self.packagewizard)
        font = QtGui.QFont()
        font.setFamily("URW Gothic L")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.buttonCancel.setFont(font)
        self.buttonCancel.setCheckable(False)
        self.buttonCancel.setFlat(False)
        self.buttonCancel.setObjectName("buttonCancel")
        self.horizontalLayout_2.addWidget(self.buttonCancel)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.buttonBack = QtWidgets.QPushButton(self.packagewizard)
        font = QtGui.QFont()
        font.setFamily("URW Gothic L")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.buttonBack.setFont(font)
        self.buttonBack.setCheckable(False)
        self.buttonBack.setFlat(False)
        self.buttonBack.setObjectName("buttonBack")
        self.horizontalLayout_2.addWidget(self.buttonBack)
        self.buttonNext = QtWidgets.QPushButton(self.packagewizard)
        font = QtGui.QFont()
        font.setFamily("URW Gothic L")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.buttonNext.setFont(font)
        self.buttonNext.setCheckable(False)
        self.buttonNext.setFlat(False)
        self.buttonNext.setObjectName("buttonNext")
        self.horizontalLayout_2.addWidget(self.buttonNext)
        self.buttonFinish = QtWidgets.QPushButton(self.packagewizard)
        font = QtGui.QFont()
        font.setFamily("URW Gothic L")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.buttonFinish.setFont(font)
        self.buttonFinish.setStyleSheet("color: rgb(255, 255, 255);")
        self.buttonFinish.setCheckable(False)
        self.buttonFinish.setFlat(False)
        self.buttonFinish.setObjectName("buttonFinish")
        self.horizontalLayout_2.addWidget(self.buttonFinish)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 2)
        self.gridLayout_3.addWidget(self.packagewizard, 0, 0, 1, 1)

        self.retranslateUi(packagewizardUI)
        self.mainStack.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(packagewizardUI)

    def retranslateUi(self, packagewizardUI):
        _translate = QtCore.QCoreApplication.translate
        packagewizardUI.setWindowTitle(_translate("packagewizardUI", "Wizard Desktop"))
        self.buttonCancel.setStyleSheet(_translate("packagewizardUI", "color: rgb(255, 255, 255);"))
        self.buttonCancel.setText(_translate("packagewizardUI", "Cancel"))
        self.buttonBack.setStyleSheet(_translate("packagewizardUI", "color: rgb(255, 255, 255);"))
        self.buttonBack.setText(_translate("packagewizardUI", "Back"))
        self.buttonNext.setStyleSheet(_translate("packagewizardUI", "color: rgb(255, 255, 255);"))
        self.buttonNext.setText(_translate("packagewizardUI", "Next"))
        self.buttonFinish.setText(_translate("packagewizardUI", "Finish"))

import raw_rc

class PackageWizard(QtWidgets.QWidget, Ui_packagewizardUI):
    def __init__(self):
#        self.ui = Ui_welcomeWidget()
        super().__init__()


app = QApplication(sys.argv)
packagewizard = PackageWizard()
packagewizard.setupUi(packagewizard)
packagewizard.show()
sys.exit(app.exec_())
