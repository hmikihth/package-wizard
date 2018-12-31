#!/usr/bin/python3
# -*- coding: utf-8 -*-

import gettext
gettext.install("fusionlogic-common", "/usr/share/locale")
#gettext.install("fusionlogic-packagewizard", "/usr/share/locale")

import sys, getopt
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import subprocess, os, dbus

from fusionlogic.packagewizard.packagewizardMain import Ui_packagewizardUI
from fusionlogic import ScrWelcome as welcomeWidget
from fusionlogic import ScrAbout as aboutWidget
from fusionlogic.packagewizard import ScrInstallator as installatorWidget
from fusionlogic.packagewizard import ScrMultipleInstallator as mInstallatorWidget
from fusionlogic.packagewizard import ScrInstallProgress as InstallProgressWidget
from fusionlogic.packagewizard.InstallerQueries import get_rpm_file_info, get_deb_file_info, get_package_info
from fusionlogic.packagewizard.InstallerThreads import PKConInstallerThread

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument("--install", dest="pkg_install", help=_("Install packages with pkcon"), metavar=_("package [package] [package] ..."), nargs='*')
parser.add_argument("--uninstall", dest="pkg_uninstall", help=_("Uninstall packages with pkcon"), metavar=_("package [package] [package] ..."), nargs='*')
parser.add_argument("--noninteractive", dest="pkg_noninteractive", help=_("pkcon --noninteractive"), action='store_true')
parser.add_argument("--only-download", dest="pkg_only_download", help=_("pkcon --only-download"), action='store_true')
parser.add_argument("--allow-downgrade", dest="pkg_allow_downgrade", help=_("pkcon --allow-downgrade"), action='store_true')
parser.add_argument("--allow-reinstall", dest="pkg_allow_reinstall", help=_("pkcon --allow-reinstall"), action='store_true')
parser.add_argument("--allow-untrusted", dest="pkg_allow_untrusted", help=_("pkcon --allow-untrusted"), action='store_true')
#parser.add_argument("--background", dest="pkg_background", help=_("pkcon --background"), action='store_true')
#parser.add_argument("--filter", dest="pkg_filter", help=_("pkcon --filter"), metavar=_("<filter>"), nargs=1)
arguments = parser.parse_args()


if arguments.pkg_uninstall or len(arguments.pkg_install)>1:
    availableScreens = [mInstallatorWidget, InstallProgressWidget, aboutWidget]
else:
    availableScreens = [installatorWidget, InstallProgressWidget, aboutWidget]

class PackageWizard(QWidget):
    def __init__(self):
        super().__init__()
        
        self.install_started = False
        self.details_visible = False
        self.ui = Ui_packagewizardUI()

        self.ui.setupUi(self)
        self.screens = availableScreens
        self.screenData = None
        self.moveInc = 1
        self.menuText = ""
        #self.config = KConfig("packagewizardrc")
        self.createWidgets(self.screens)


        self.ui.labelMenu.setText(self.menuText)

        self.ui.buttonNext.clicked.connect(self.slotNext)
        self.ui.buttonBack.clicked.connect(self.slotBack)
        self.ui.buttonFinish.clicked.connect(self.close)
        self.ui.buttonCancel.clicked.connect(self.close)
        
        self.load_package_info(self.ui.mainStack.currentWidget().ui)

    def load_package_info(self, ui):
        info = {}
        if len(arguments.pkg_install)==1:
            if arguments.pkg_install[0].endswith('.rpm'):
                info = get_rpm_file_info(arguments.pkg_install[0])
            elif arguments.pkg_install[0].endswith('.deb'):
                info = get_deb_file_info(arguments.pkg_install[0])
            else:
                info = get_package_info(arguments.pkg_install[0])
        ui.packageName.setText("{}".format(info["Name"]))
        ui.labelSummary.setText("Version: {} Release: {} Architecture: {}".format(info["Version"],info["Release"],info['Architecture']))
        ui.label.setText("{}".format(info["Summary"]))
        ui.packagedescription.setText(_('{}\nSize: {} License: {}\nURL: {}').format(
                info["Description"], info["Size"], info["License"], info["URL"]))

    def set_progressbar(self, value, text):
        self.progress_ui.progressBar.setFormat(text + " (%p%)")
        self.progress_ui.progressBar.setValue(value)
    
    def installer_sent_message(self, message):
        if message.startswith("Downloaded") or message.startswith("Installed"):
            self.progress_ui.statusLabel.setText(message)
        self.progress_ui.textBrowser.insertHtml(message)
        sb = self.progress_ui.textBrowser.verticalScrollBar()
        sb.setValue(sb.maximum())

    def installer_ask(self, question):
        self.progress_ui.questionLabel.setText(question)
        self.showYesNo()
        
    def installer_finished(self):
        self.enableBack()
        self.enableNext()
        self.showBackNext()

    def clear_label(self):
        self.progress_ui.questionLabel.setText("")

    def detailsPressed(self):
        if self.details_visible:
            self.details_visible = False
            self.progress_ui.textBrowser.hide()
        else:
            self.details_visible = True
            self.progress_ui.textBrowser.show()

    def startInstallProgress(self):
        if not self.install_started:
            self.install_started = True
            self.disableBack()
            self.disableNext()
            self.progress_ui = self.ui.mainStack.currentWidget().ui
            self.progress_ui.yesButton.clicked.connect(self.yesPressed)
            self.progress_ui.noButton.clicked.connect(self.noPressed)
            self.progress_ui.detailsButton.clicked.connect(self.detailsPressed)
            self.hideYesNo()
            self.hideBackNext()

            self.installer_thread = PKConInstallerThread(self)
            self.installer_thread.start()
            self.progress_ui.textBrowser.setHidden(True)
            env = os.environ
            env["LC_ALL"] = "C"
            pkcon_args = ['pkcon','-p']
            if arguments.pkg_install:
                if ".rpm" in arguments.pkg_install[0]:
                    pkcon_args += ["install-local"]
                else:
                    pkcon_args += ["install"]
            if arguments.pkg_uninstall: pkcon_args += ["remove"]
            if arguments.pkg_noninteractive: pkcon_args += ["--noninteractive"]
            if arguments.pkg_only_download: pkcon_args += ["--only-download"]
            if arguments.pkg_allow_downgrade: pkcon_args += ["--allow-downgrade"]
            if arguments.pkg_allow_reinstall: pkcon_args += ["--allow-reinstall"]
            if arguments.pkg_allow_untrusted: pkcon_args += ["--allow-untrusted"]
#            if arguments.pkg_background: pkcon_args += ["--background"]
#            if arguments.pkg_filter: pkcon_args += ["--filter", arguments.pgk_filter]
            if arguments.pkg_install: pkcon_args += arguments.pkg_install
            if arguments.pkg_uninstall: pkcon_args += arguments.pkg_uninstall
            self.installer_thread.set_job(pkcon_args, env)

    def hideBackNext(self):
        self.ui.buttonNext.hide()
        self.ui.buttonBack.hide()

    def showBackNext(self):
        self.ui.buttonNext.show()
        self.ui.buttonBack.show()

    def hideYesNo(self):
        self.progress_ui.yesButton.hide()
        self.progress_ui.noButton.hide()
        
    def showYesNo(self):
        self.progress_ui.yesButton.show()
        self.progress_ui.noButton.show()

    def yesPressed(self):
        self.hideYesNo()
        self.installer_thread.yes_sig.emit()

    def noPressed(self):
        self.hideYesNo()
        self.installer_thread.no_sig.emit()
        
    def slotFinished(self):
        QtGui.qApp.quit()

    # returns the id of current stack
    def getCur(self, d):
        new   = self.ui.mainStack.currentIndex() + d
        total = self.ui.mainStack.count()
        if new < 0: new = 0
        if new > total: new = total
        return new

    # move to id numbered step
    def setCurrent(self, id=None):
        if id:
            self.stackMove(id)

    # execute next step
    def slotNext(self,dryRun=False):
        self.menuText = ""
        curIndex = self.ui.mainStack.currentIndex() +1

        for each in self.screenId:
            i = self.screenId.index(each)
            if  curIndex < len(self.screenId):
                if i == curIndex:
                    self.menuText += self.putBold(self.screenId[i])
                else:
                    self.menuText += self.putBr(self.screenId[i])

        self.ui.labelMenu.setText(self.menuText)

        _w = self.ui.mainStack.currentWidget()
        ret = _w.execute()
        if ret:
            self.stackMove(self.getCur(self.moveInc))
            self.moveInc = 1
        if curIndex == 1:
            self.startInstallProgress()

    # execute previous step
    def slotBack(self):
        self.menuText = ""
        curIndex = self.ui.mainStack.currentIndex()
        for each in self.screenId:
            i = self.screenId.index(each)
            if i <= len(self.screenId) and not i == 0:
                if i == curIndex:
                    self.menuText += self.putBold(self.screenId[i -1])
                else:
                    self.menuText += self.putBr(self.screenId[i -1])

        self.menuText += self.putBr(self.screenId[-1])
        self.ui.labelMenu.setText(self.menuText)

        _w = self.ui.mainStack.currentWidget()
        _w.backCheck()
        self.stackMove(self.getCur(self.moveInc * -1))
        self.moveInc = 1

    #def putBr(self, item):
    #    return unicode("  ") + item + "<br>"
    #
    #def putBold(self, item):
    #    return "<b>" + unicode("  ") + item + "</b><br>"

    def putBr(self, item):
        return "» " + item + "<br>"
        #return unicode("» ", encoding='utf-8') + item + "<br>"

    def putBold(self, item):
        return "<b>  " + item + " »" + "</b><br>"
        #return "<b><u>" +  item + unicode(" »", encoding='utf-8') +"</u></b><br>"

    # move to id numbered stack
    def stackMove(self, id):
        if not id == self.ui.mainStack.currentIndex() or id==0:
            self.ui.mainStack.setCurrentIndex(id)
            _w = self.ui.mainStack.currentWidget()
            #_w.update()
            #_w.shown()

        if self.ui.mainStack.currentIndex() == len(self.screens)-1:
            self.ui.buttonNext.hide()
            self.ui.buttonFinish.show()
        else:
            self.ui.buttonNext.show()
            self.ui.buttonFinish.hide()

        if self.ui.mainStack.currentIndex() == 0:
            self.ui.buttonBack.hide()
        else:
            self.ui.buttonBack.show()

    # create all widgets and add inside stack
    def createWidgets(self, screens=[]):

        self.screenId = []

        self.ui.mainStack.removeWidget(self.ui.page)
        for screen in screens:
            _scr = screen.Widget()
            title = _scr.windowTitle()
            self.screenId.append(title)

            if self.screens.index(screen) == 0:
                self.menuText += self.putBold(title)
            else:
                self.menuText += self.putBr(title)
            self.ui.mainStack.addWidget(_scr)

        self.stackMove(0)

    def disableNext(self):
        self.ui.buttonNext.setEnabled(False)

    def disableBack(self):
        self.ui.buttonBack.setEnabled(False)

    def enableNext(self):
        self.ui.buttonNext.setEnabled(True)

    def enableBack(self):
        self.ui.buttonBack.setEnabled(True)

    def isNextEnabled(self):
        return self.ui.buttonNext.isEnabled()

    def isBackEnabled(self):
        return self.ui.buttonBack.isEnabled()

    #def __del__(self):
    #    group = self.config.group("General")
    #    group.writeEntry("RunOnStart", "False")


if __name__ == "__main__":

    homePage    = ""
    bugEmail    = ""

    aboutData   = ""
    
    if not sys.argv[1:]:
    	sysarg = sys.argv
    else:
    	sysarg = sys.argv[1:]
        
#        for opt in optlist[1:]:
#    	    if "-m" in opt:
#                sysarg = sys.argv[1:]
#    	    else:
#                sysarg = sys.argv

    if not dbus.get_default_main_loop():
        from dbus.mainloop.pyqt5 import DBusQtMainLoop
        DBusQtMainLoop(set_as_default = True)

    app = QApplication(sys.argv)
    packagewizard = PackageWizard()
    packagewizard.show()
    #rect  = QtGui.QDesktopWidget().screenGeometry()
    #packagewizard.move(rect.width()/2 - packagewizard.width()/2, rect.height()/2 - packagewizard.height()/2)
    app.exec_()

