#!/usr/bin/python3
# -*- coding: utf-8 -*-

import gettext
gettext.install("fusionlogic", "/usr/share/locale")

import sys, getopt
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


import subprocess, os, dbus
#import package_wizard

from fusionlogic.packagewizard.packagewizardMain import Ui_packagewizardUI
# FOR ANOTHER TEST 
#import modules.welcomeWidget as welcomeWidget
# END
import fusionlogic.packagewizard.ScrWelcome as welcomeWidget
import fusionlogic.packagewizard.ScrAbout as aboutWidget
#import fusionlogic.packagewizard.ScrRecommend  as recommendWidget
#import fusionlogic.packagewizard.ScrGoodbye  as goodbyeWidget

#def usage() :
#      print """ -m <module1> <module2> <module3> <module4> <module5> """  % (sys.argv[0],sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])

def loadFile(_file):
    try:
        f = file(_file)
        d = [a.strip() for a in f]
        d = (x for x in d if x and x[0] != "#")
        f.close()
        return d
    except:
        return []

def isLiveCD():
    try:
        liveCDcheck = open('/var/run/blackPanther')
    except IOError:
        return False

    return True

if isLiveCD():
    availableScreens = [welcomeWidget, keyboardWidget, mouseWidget, menuWidget, wallpaperWidget, networkWidget, summaryWidget, goodbyeWidget]
#elif profileSended():
#    availableScreens = [welcomeWidget, mouseWidget, styleWidget, menuWidget, wallpaperWidget, searchWidget, networkWidget, packageWidget, summaryWidget, goodbyeWidget]
#elif paramGet():
    # ide be lehet allitani majd, hogy csak a választott dialogok jelenjenek meg
#    availableScreens = [recommendWidget, goodbyeWidget]
else:
    availableScreens = [welcomeWidget, aboutWidget]
    #availableScreens = []

class PackageWizard(QWidget):
    def __init__(self):
        super().__init__()
        
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

    def slotFinished(self):
        if wallpaperWidget.Widget.selectedWallpaper:
            #config =  KConfig("plasma-desktop-appletsrc")
            #group = config.group("Containments")
            #for each in list(group.groupList()):
            #    subgroup = group.group(each)
            #    subcomponent = subgroup.readEntry('plugin')
            #    if subcomponent == 'desktop' or subcomponent == 'folderview':
            #        subg = subgroup.group('Wallpaper')
            #        subg_2 = subg.group('image')
            #        subg_2.writeEntry("wallpaper", wallpaperWidget.Widget.selectedWallpaper)
            self.killPlasma()
            QtGui.qApp.quit()
        else:
            QtGui.qApp.quit()

    def killPlasma(self):
        p = subprocess.Popen(["pidof", "-s", "plasmashell"], stdout=subprocess.PIPE)
        out, err = p.communicate()
        pidOfPlasma = int(out)

        try:
            os.kill(pidOfPlasma, 15)
            self.startPlasma()
        except:
#        except OSError, e:
#            print 'WARNING: failed os.kill: %s' % e
#            print "Trying SIGKILL"
            os.kill(pidOfPlasma, 9)
            self.startPlasma()

    def startPlasma(self):
        p = subprocess.Popen(["plasmashell"], stdout=subprocess.PIPE)

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
        self.buttonNext.setEnabled(False)

    def disableBack(self):
        self.buttonBack.setEnabled(False)

    def enableNext(self):
        self.buttonNext.setEnabled(True)

    def enableBack(self):
        self.buttonBack.setEnabled(True)

    def isNextEnabled(self):
        return self.buttonNext.isEnabled()

    def isBackEnabled(self):
        return self.buttonBack.isEnabled()

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

