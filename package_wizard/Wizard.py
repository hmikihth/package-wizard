#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import gtk
import gtk.glade
import time
import commands
import common; _ = common._
import string
from common import * 
from ProgressIndicator import *

ICON_X = 48
ICON_Y = 48

DIR = commands.getoutput('echo ${HOME}') + '/.rpmanager/'
commands.getoutput('mkdir ' + DIR)
FLAGFILE = DIR + 'flagfile'

def WaitProc():
  while True:
    try:
      file = open(FLAGFILE, 'r')
      file.close()
      commands.getoutput('rm '+FLAGFILE)
      time.sleep(0.1)
      break
    except:
      time.sleep(0.1)

def iconsize(iconpath):
    comm = 'file ' + iconpath
    filestring = commands.getoutput(comm)
    a = filestring.find(',')+1
    filestring = filestring[a:]
    a = filestring.find(',')
    filestring = filestring[:a]
    i = 0
    l = len(filestring)
    v0 = ''
    v1 = ''
    flag = False
    while i < l:
      if filestring[i] in string.digits:
        if flag:
          v1 += filestring[i]
        else:
          v0 += filestring[i]
      if filestring[i] in string.letters:
        flag = True
      i += 1
    return [int(v0), int(v1)]

def iconchooser (iconlist):
    l = len(iconlist)
    i = 0
    ret = ''
    while i < l:
      sl = iconsize(iconlist[i])
      if sl[0] == ICON_X and sl[1] == ICON_Y:
        ret = iconlist[i]
        break
      i += 1
    return ret

def get_rpm_unerrored_output(command):
    output = commands.getoutput(command).strip()
    if output != '(contains no files)':
      lines = output.splitlines()
    else:
      lines = []
    newlines = []
    for line in lines:
      if not line.startswith("warning"):
        newlines.append(line)
    newoutput = "\n".join(newlines)
    newoutput = newoutput.strip()
    return newoutput

def IntVersion(Str):
    if Str[0] in string.letters:
      return (-1)
    ReturnValue = 0
    i = 0
    l = len(Str)
    while i < l:
      a = Str[i]
      if a == '.':
        ReturnValue = ReturnValue * 1000
      elif a in string.digits:
        ReturnValue = ReturnValue * 10
        ReturnValue += int(a)
      else:
        pass
      i += 1
    return ReturnValue
    
def SlitText(Text):
    if Text == '':
      Text = 'None\n\n'
    PrimaryLineSize = 45
    SecondaryLineSize = 60
    lsf = False
    LineSize = PrimaryLineSize
    EndChars = ['\n',' ','\t']
    flag = False
    i = 0
    j = 0
    Word = ''
    Line = ''
    ReturnString = ''
    l = len(Text)
    while True:
      a = Text[i]
      if a in EndChars:
        b = len(Line) + len(Word)
        if b > LineSize:
          ReturnString += Line + '\n'
          Line = ''
          if not lsf:
            LineSize = SecondaryLineSize
            lsf = True
        else:
          Line += Word + ' '
          Word = ''
      else:
        Word += a
      i += 1
      if i == l:
        if b <= LineSize:
          ReturnString += Line + Word
        break
    return ReturnString

def ps():
    pstr = commands.getoutput('ps --no-header -Ao comm')
    l = len(pstr)
    i = 0
    com = ''
    ret = []
    while i < l:
      a = pstr[i]
      if a != '\n':
        com += a
      else:
        ret.append(com)
        com = ''
      i += 1
    return ret

def WaitXsec(sec):
    ST = time.time()
    while True:
      a = time.time() - ST
      if a == sec:
          break

class RPMPackage:
	Packagename = None
	Version = None
	Filename = None
	InstalledSize = None
	Installed = False
	Description = None
	source_package = False
	new_package = 0
	Provides = ''
	Dependencies = ''
	Files = ''

class InfoCache(RPMPackage):
    def __init__(self, a):
        self.a = a
        self.run()
    def run(self):
        TimeInit = time.time()
        rpmq = get_rpm_unerrored_output('rpm -qp --queryformat \"%{Name}<br>%{Version}<br>%{Release}<br>%{Summary}<br>%{Size}<br>%{Description}\" '+self.a.package_path).split('<br>')
        self.Name = rpmq[0]
        l = len(self.Name)
        i = 0
        while True:
          if self.Name[i] in string.digits or self.Name[i] == '-':
            break
          i += 1
          if i == l:
            i = -1
            break
        if i != -1:
          self.Name2 = self.Name[:i]
        else:
          self.Name2 = self.Name
        self.Version = rpmq[1]
        self.Release = rpmq[2]
 	self.Summary = rpmq[3].replace('<','(').replace('>',')').replace('&','and')
	self.Size = rpmq[4] 
	self.InstalledSize = int(self.Size) / 1024      
	self.Description =  rpmq[5].replace('<','(').replace('>',')').replace('&','and')
	self.Description =  SlitText(self.Description)
	self.DescriptionCache = self.Description    
	filename = os.path.basename(self.a.package_path)[:-4]
	if filename[-3:] == 'src':
	  self.source_package = True
	self.Packagename = filename
        self.Installed = False
        self.new_package = 0
	try:
          rpmq = get_rpm_unerrored_output('rpm -q --queryformat \"%{Name}<br>%{Version}<br>%{Release}\" '+self.Name)
	  if 'is not installed' not in rpmq:
	    rpmq = rpmq.split("<br>")
      	    self.InstVersion = rpmq[1]
  	    Inst =  IntVersion(self.InstVersion)
  	    Rel = rpmq[2]
  	    Pack =  IntVersion(self.Version)
  	    self.InstRelease = Rel
          else:
            Inst = 0
	  if Inst == 0:
	    pass
	  elif Inst == Pack:
            self.Installed = True
	    if Rel != self.Release:
	      if commands.getoutput('rpm -U --test ' + self.a.package_path).find('which is newer') == -1:
	        self.new_package = 1
              else:
	        self.new_package = -1
          elif Pack > Inst:
            self.Installed = True
            self.new_package = 1
            print 'Upgradable package: ', rpmq[0]
          else:
            self.Installed = True
            self.new_package = -1
        except:
          print 'Error 244 H'
#        rpmq = get_rpm_unerrored_output('rpm -qp --queryformat \"%{Packager}<br>%{Distribution}<br>%{BuildTime:date}<br>%{License}<br>%{Url}\" '+self.a.package_path).split('<br>')
#	self.MoreInfoCache = _('<b>Name:\t</b>') + self.Name + '\n'      
#	self.MoreInfoCache += _('<b>Version:\t</b>') + self.Version      
#	self.MoreInfoCache += _('<b>\t\tRelease:\t</b>') + self.Release + '\n'
#	self.MoreInfoCache += _('<b>\nPackager:\t</b>') + rpmq[0].replace('<','(').replace('>',')') + '\n'      
#	self.MoreInfoCache += _('<b>Package to:\t</b>') + rpmq[1] + '\n'      
#	self.MoreInfoCache += _('<b>Build Date:\t</b>') + rpmq[2] + '\n'
#	self.MoreInfoCache += _('<b>Size:\t\t</b>') + self.Size+ ' byte\n'
#	self.MoreInfoCache += _('<b>License:\t\t</b>') + rpmq[3] + '\n'      
#	self.MoreInfoCache += _('<b>Webpage:\t</b>') + rpmq[4] + '\n'
#	self.MoreInfoCache += _('<b>\nDescription:\t</b>') + self.Description
        print 'InfoCache(): ', time.time() - TimeInit
	
class Wizard:
    def __init__(self):
        TimeInit = time.time()
    	self.progress_indicator = ProgressIndicator()
        ctasks = os.listdir('/usr/share/rpmanager/conflicts/')
        tasks = ps()
        l = len(ctasks)
        i = 0
        c = 0
        while i < l:
          if ctasks[i] in tasks:
            c += 1
          i += 1
        if c != 0:
          self.IndicateProgress(True, l)
          i = 0
          while i < l:
            if ctasks[i] in tasks:
              self.DisplayProgress(_('Conflict: ') + ctasks[i] + _(' is running'))
              while True:
                tasks = ps()
                if ctasks[i] not in tasks:
                  break
            else:
              self.DisplayProgress(ctasks[i] + _(' is not running'))
            i += 1
          self.IndicateProgress(False)            
    	self.install_flag = False
    	self.uninstall_flag = False
    	self.loadcache_flag = False
    	self.active_progress = False
        self.wizard1_window_signals = {
            'on_next_button_clicked': self.OnNextPage,
            'on_file_chooser_button_clicked': self.OnFileChooserButtonClicked,
            'on_package_filename_entry_changed':  self.OnPackageFilenameEntryChanged,
            'on_source_button_clicked': self.OnSourceButtonClicked,
            'on_quit1_button_clicked': gtk.main_quit,
            'on_wizard1_window_destroy': gtk.main_quit
        }
        self.wizard2_window_signals = {
            'on_prev_button_clicked': self.OnPrevPage,
            'on_install_button_clicked': self.OnInstallButtonClicked,
            'on_uninstall_button_clicked': self.OnUninstallButtonClicked,
            'on_checkbutton1_pressed': self.OnCheckButton1Pressed,
            'on_checkbutton2_pressed': self.OnCheckButton2Pressed,
            'on_checkbutton3_pressed': self.OnCheckButton3Pressed,
            'on_checkbutton4_pressed': self.OnCheckButton4Pressed,
            'on_quit2_button_clicked': gtk.main_quit,
            'on_wizard2_window_destroy': gtk.main_quit
        }
        self.wizard3_window_signals = {
            'on_install_new_button_clicked': self.OnInstallNewButtonClicked,
            'on_quit3_button_clicked': gtk.main_quit,
            'on_wizard3_window_destroy': gtk.main_quit
        }
        glade_xml_wizard3_window = gtk.glade.XML(GLADE_FILENAME, 'wizard3_window')
        self.wizard3_window = glade_xml_wizard3_window.get_widget('wizard3_window')
        glade_xml_wizard3_window.signal_autoconnect(self.wizard3_window_signals)
        l = len(sys.argv)
	if l > 2:
            self.MultipleInfo = ''
            self.MultipleSize = 0
	    i = 1
	    self.package_filename = ''
	    package_filename = ''
            self.IndicateProgress(True, l)
	    while i < l:
              self.package_filename = sys.argv[i]
              self.DisplayProgress(self.package_filename)
              self.GetPackageInfo()
              self.MultipleSize += int(self.InfoCache.Size)
              if i != 1:
                self.MultipleInfo += '\n\n\n'
                package_filename += ' '
              package_filename += self.package_filename
              self.MultipleInfo += _('<i><b>File:</b> ') + ' <u>' + self.package_filename[self.package_filename.rfind('/')+1:] + '</u></i>\n\n'
              self.PackageStatus()
              self.MultipleInfo += _('<b>Status:</b> ') + self.status + '\n\n'
              self.MultipleInfo += self.InfoCache.MoreInfoCache
              i += 1
            self.IndicateProgress(False)
            self.package_filename = package_filename              
        elif l == 2:
            self.package_filename = sys.argv[1]
	    self.GetPackageInfo()
        else:
            self.package_filename = ''
            glade_xml_wizard1_window = gtk.glade.XML(GLADE_FILENAME, 'wizard1_window')
            self.wizard1_window = glade_xml_wizard1_window.get_widget('wizard1_window')
            glade_xml_wizard1_window.signal_autoconnect(self.wizard1_window_signals)
            self.package_filename_entry = glade_xml_wizard1_window.get_widget('package_filename_entry')
            self.next_button = glade_xml_wizard1_window.get_widget('next_button')
        self.glade_xml_wizard2_window	= gtk.glade.XML(GLADE_FILENAME, 'wizard2_window')
        self.wizard2_window 		= self.glade_xml_wizard2_window.get_widget('wizard2_window')
        self.glade_xml_wizard2_window.signal_autoconnect(self.wizard2_window_signals)
        self.install_button 	= self.glade_xml_wizard2_window.get_widget('install_button')
        self.uninstall_button 	= self.glade_xml_wizard2_window.get_widget('uninstall_button')
        self.package_info_rpmview 	= self.glade_xml_wizard2_window.get_widget('package_info_rpmview')
        self.checkbutton1		= self.glade_xml_wizard2_window.get_widget('checkbutton1')
        self.checkbutton2		= self.glade_xml_wizard2_window.get_widget('checkbutton2')
        self.checkbutton3		= self.glade_xml_wizard2_window.get_widget('checkbutton3')
        self.checkbutton4		= self.glade_xml_wizard2_window.get_widget('checkbutton4')
        self.prev_button		= self.glade_xml_wizard2_window.get_widget('prev_button')
        self.package_status		= self.glade_xml_wizard2_window.get_widget('packagestatus')
        if l >= 2:
            self.wizard2_window.show_all()
            self.display_rpm_info()
        print '__init__(): ', time.time() - TimeInit
        gtk.main()

    def SOL(self, il):
        ret = []
        str = ''
        i = 0
        l = len(il)
        while True:
          if il[i] == '|':
            ret.append(str)
            str = ''
          else:
            str += il[i]
          i += 1
          if i == l:
            ret.append(str)
            break
        return ret

    def IsInstalled(self, inp):
        if inp in self.InfoCache.List:
          return True
        else:
          return False

    def DependencyFind(self):
        TimeInit = time.time()
        self.LoadCache()
        b = self.InfoCache.Dependencies.split()
        c = ''
        l = len (b)
        i = 0
        while i < l:
          x = b[i].find('|')
          if x == -1:
            if not self.IsInstalled(b[i]):
              c += b[i]
              c += '\n'
          elif x != -1:
            ol = self.SOL(b[i])
            l2 = len(ol)
            j = 0
            flag = True
            while j < l2:
              if self.IsInstalled(ol[j]):
                flag = False
                break
              j += 1
            if flag:
              c += b[i]
              c += '\n'
          i += 1
        print 'DependencyFind(): ', time.time() - TimeInit
        return c
    
    def OnNextPage(self, widget):
        TimeInit = time.time()
	self.GetPackageInfo()
	if self.uninstall_flag:
	  self.uninstall_flag = False
	  self.InfoCache = InfoCache(self)
	self.display_rpm_info()
	self.ChangeWindow(self.wizard1_window, self.wizard2_window)
        print 'OnNextPage(): ', time.time() - TimeInit
 
    def OnPrevPage(self, widget):
        self.CheckButtonClear(0)
	self.ChangeWindow(self.wizard2_window, self.wizard1_window)

    def OnFileChooserButtonClicked(self, widget):
	new_package_filename = self.GetPackageName(self.package_filename)
	self.package_filename = new_package_filename        
	if new_package_filename:
	  self.package_filename_entry.set_text(conv(new_package_filename))
    
    def OnPackageFilenameEntryChanged(self, widget):
	has_text = bool(widget.get_text())
	self.next_button.set_sensitive(has_text)
    
    def OnSourceButtonClicked(self, widget):
        os.execlp('./rpmanager', './rpmanager')

    def OnOkButtonClicked(self, widget):
        print 'OnOkButtonClicked()'
        self.q = True
    
    def OnInstallButtonClicked(self, widget):
      TimeInit = time.time()
      self.CheckButtonClear(0)
      if (len(sys.argv) < 3 or self.install_flag) and not self.undefined_error_flag:
        self.InfoCache = InfoCache(self)
        self.loadcache_flag = False
        if not self.InfoCache.Installed or self.InfoCache.source_package or self.InfoCache.new_package != 0:
	  package_filename = self.package_filename.replace(' ', '\ ')
	  if self.InfoCache.new_package != -1:
	    command = ['/usr/bin/gurpmi2', package_filename, FLAGFILE]
          else:
	    command = ['rpm', '-U', '--oldpackage', package_filename,  FLAGFILE]   
            ID = commands.getoutput('id -u')
            if ID != '0':
              command.insert(0, './findsu')
          command.insert(0, './shcomm.py')
          os.spawnvp(os.P_NOWAIT, command[0], command)
          if self.InfoCache.Name == 'refresher':
            self.ChangeWindow(self.wizard2_window, self.wizard3_window)
          else:
            WaitProc()
          if self.InfoCache.source_package != True or self.InfoCache.new_package != 0:
	    try:
	      Inst =  IntVersion(get_rpm_unerrored_output('rpm -q --queryformat \"%{Version}\" ' + self.InfoCache.Name))
	      Pack =  IntVersion(self.InfoCache.Version)
	      Rel = get_rpm_unerrored_output('rpm -q --queryformat \"%{Release}\" ' + self.InfoCache.Name)
	      if Inst == Pack and Rel == self.InfoCache.Release:
	        self.ChangeWindow(self.wizard2_window, self.wizard3_window)
              else:
                deps = self.DependencyFind()
                if deps != '':
                  self.desc.set_markup(_('<b><big>Failed dependencies:</big></b>\n\n') + deps)
                  self.glade_xml_wizard2_window.get_widget("label159").set_text(_("Force"))
                  self.force_install_mode_flag = True
                  self.uninstall_button.set_sensitive(True)
                  self.install_button.set_sensitive(False)
                else:
                  self.desc.set_markup(_('<b><big>Undefined error</big>\n\n If you\'re versed user, press Details button for details!\n(It\'s where the Install button used to be.)</b>'))    
                  self.glade_xml_wizard2_window.get_widget("label159").set_text(_("Force"))
                  self.force_install_mode_flag = True
                  self.uninstall_button.set_sensitive(True)
                  self.undefined_error_flag = Trueq
                  self.glade_xml_wizard2_window.get_widget("label43").set_text(_("Details"))
                  self.error_log = 'error 1'
            except:
              self.desc.set_markup(_('<b><big>Undefined error</big>\n\n If you\'re versed user, press Details button for details!\n(It\'s where the Install button used to be.)</b>'))
              self.undefined_error_flag = True
              self.glade_xml_wizard2_window.get_widget("label43").set_text(_("Details"))
              self.error_log = 'error 2'
          else:
            self.ChangeWindow(self.wizard2_window, self.wizard3_window)
      elif self.undefined_error_flag:
        self.install_button.set_sensitive(False)
        self.desc.set_markup(SlitText(self.error_log))			        
      else:
        command = '/usr/bin/gurpmi2 ' + self.package_filename
        err = commands.getoutput(command)
        self.ChangeWindow(self.wizard2_window, self.wizard3_window)
      print 'OnInstallButtonClicked(): ', time.time() - TimeInit

    def OnUninstallButtonClicked(self, widget):
#      if len(sys.argv) < 3 or self.install_flag:
        TimeInit = time.time()        
        self.CheckButtonClear(0)
        if not self.force_install_mode_flag and not self.force_uninstall_mode_flag:
          self.IndicateProgress(True, 2)
	  package_filename = self.package_filename.replace(' ', '\ ')	
          ID = commands.getoutput('id -u')
          self.DisplayProgress(' ')
          if ID != '0':
	    command = './findsu rpm -e ' + self.InfoCache.Name + '-' + self.InfoCache.InstVersion + '-' + self.InfoCache.InstRelease
          else:
	    command = 'rpm -e ' + self.InfoCache.Name + '-' + self.InfoCache.InstVersion + '-' + self.InfoCache.InstRelease
          output = commands.getoutput(command)
          self.DisplayProgress(' ')
          Inst =  get_rpm_unerrored_output('rpm -q --queryformat \"%{Version}\" ' + self.InfoCache.Name)
          self.DisplayProgress(' ')
          Rel = get_rpm_unerrored_output('rpm -q --queryformat \"%{Release}\" ' + self.InfoCache.Name)
          self.IndicateProgress(False)
          if Inst != self.InfoCache.Version:
            self.package_status.set_markup(_("Installable"))
            self.glade_xml_wizard2_window.get_widget("label43").set_text(_("Install"))
            self.InfoCache.new_package = 0
            self.glade_xml_wizard2_window.get_widget("diskspacelabel").set_text(_("Required disk space:"))
            self.install_button.set_sensitive(True)
            self.uninstall_button.set_sensitive(False)
            self.uninstall_flag = True
            self.desc.set_markup(_('<b>Uninstall done.</b>'))
          else:
            self.desc.set_markup(_('<b>Uninstall failed:</b>\n\n%s') % output)
            self.glade_xml_wizard2_window.get_widget("label159").set_text(_("Force"))
            self.force_uninstall_mode_flag = True
        elif self.force_install_mode_flag:
            self.IndicateProgress(True, 4)
	    package_filename = self.package_filename.replace(' ', '\ ')
            ID = commands.getoutput('id -u')
            self.DisplayProgress(' ')
            if self.InfoCache.new_package == 0:
              if ID != '0':
	        command = './findsu rpm -i --nodeps ' + package_filename
              else:
	        command = 'rpm -i --nodeps ' + package_filename   
              self.DisplayProgress(' ')
            elif self.InfoCache.new_package == 1:
	      if ID != '0':
	        command = './findsu rpm -U --nodeps ' + package_filename
              else:
	        command = 'rpm -U --nodeps ' + package_filename   
              self.DisplayProgress(' ')
            elif self.InfoCache.new_package == -1:
	      if ID != '0':
	        command = './findsu rpm -U --oldpackage --nodeps ' + package_filename
              else:
	        command = 'rpm -U --oldpackage --nodeps ' + package_filename   
              self.DisplayProgress(' ')
	    err = commands.getoutput(command)
            self.DisplayProgress(' ')
            Inst =  IntVersion(get_rpm_unerrored_output('rpm -q --queryformat \"%{Version}\" ' + self.InfoCache.Packagename))
            self.DisplayProgress(' ')
            Pack =  IntVersion(self.InfoCache.Version)
            self.DisplayProgress(' ')
	    Rel = get_rpm_unerrored_output('rpm -q --queryformat \"%{Release}\" ' + self.InfoCache.Name)
            self.IndicateProgress(False)
            if Inst == Pack and Rel == self.InfoCache.Release:
              self.ChangeWindow(self.wizard2_window, self.wizard3_window)
            else:
              self.desc.set_markup(_('<b><big>Force install failed!</big></b>'))
              self.install_button.set_sensitive(False)
              self.uninstall_button.set_sensitive(False)
        else:
            self.IndicateProgress(True, 2)
	    package_filename = self.package_filename.replace(' ', '\ ')
	    ID = commands.getoutput('id -u')
            self.DisplayProgress(' ')
            options = '--nodeps '
	    if ID != '0':
	      command = './findsu rpm -e ' + options  + self.InfoCache.Name + '-' + self.InfoCache.InstVersion + '-' + self.InfoCache.InstRelease
            else:
	      command = 'rpm -e '+ options + self.InfoCache.Name + '-' + self.InfoCache.InstVersion + '-' + self.InfoCache.InstRelease
	    err = commands.getoutput(command)
            self.DisplayProgress(' ')
            Inst = get_rpm_unerrored_output('rpm -q --queryformat \"%{Version}\" ' + self.InfoCache.Packagename)
            self.DisplayProgress(' ')
	    Rel = get_rpm_unerrored_output('rpm -q --queryformat \"%{Release}\" ' + self.InfoCache.Name)
            self.IndicateProgress(False)
            if Inst != self.InfoCache.Version:
              self.package_status.set_markup(_("Installable"))
              self.InfoCache.new_package = 0
              self.glade_xml_wizard2_window.get_widget("label43").set_text(_("Install"))
              self.glade_xml_wizard2_window.get_widget("diskspacelabel").set_text(_("Required disk space:"))
              self.install_button.set_sensitive(True)
              self.uninstall_button.set_sensitive(False)
              self.uninstall_flag = True
              self.desc.set_markup(_('<b>Uninstall done.</b>'))
            else:
              self.desc.set_markup(_('<b><big>Force uninstall failed:</big></b>\n\n') + err)
              self.install_button.set_sensitive(False)
              self.uninstall_button.set_sensitive(False)
        print 'OnUninstallButtonClicked(): ', time.time() - TimeInit
#      else:
#        pass #Ha több csomagot akarnank eltavolitani!!!!!!!!!!!!!!!!!!!!!!!!

    def OnInstallNewButtonClicked(self, widget):
        TimeInit = time.time()
	if self.install_flag == False and len(sys.argv) >= 2:
          self.package_filename = ''
          glade_xml_wizard1_window = gtk.glade.XML(GLADE_FILENAME, 'wizard1_window')
          self.wizard1_window = glade_xml_wizard1_window.get_widget('wizard1_window')
          self.ChangeWindow(self.wizard3_window, self.wizard1_window)
          glade_xml_wizard1_window.signal_autoconnect(self.wizard1_window_signals)
          self.package_filename_entry = glade_xml_wizard1_window.get_widget('package_filename_entry')
          self.next_button = glade_xml_wizard1_window.get_widget('next_button')
	else:
 	  self.ChangeWindow(self.wizard3_window, self.wizard1_window)
        self.install_flag = True
	self.package_filename_entry.set_text('')
        print 'OnInstallNewButtonClicked(): ', time.time() - TimeInit

    def CheckButtonFlagClear(self):
        self.checkbutton1_pressed_flag = False
        self.checkbutton2_pressed_flag = False
        self.checkbutton3_pressed_flag = False
        self.checkbutton4_pressed_flag = False    		

    def CheckButtonClear(self, a):
    	if self.checkbutton1.state and a != 1:
	  self.checkbutton1.set_active(False)
	  self.checkbutton1_pressed_flag = False
    	if self.checkbutton2.state and a != 2:
	  self.checkbutton2.set_active(False)
	  self.checkbutton2_pressed_flag = False
    	if self.checkbutton3.state and a != 3:
	  self.checkbutton3.set_active(False)
	  self.checkbutton3_pressed_flag = False
    	if self.checkbutton4.state and a != 4:
	  self.checkbutton4.set_active(False)
	  self.checkbutton4_pressed_flag = False

    def IndicateProgress(self, bool, phases=0):
      self.active_progress = bool
      self.phases = phases
      self.counter = 0.0
      if bool:
        pipe1_fd_in, pipe1_fd_out = os.pipe()
        pipe2_fd_in, pipe2_fd_out = os.pipe()
        self.pipe_file_out = os.fdopen(pipe1_fd_out, 'w')
        self.pipe_file_in  = os.fdopen(pipe2_fd_in,  'r')
        child = not os.fork()
        if child:
          os.dup2(pipe1_fd_in, 0)
          os.dup2(pipe2_fd_out, 1)
          os.execlp('./rpmanager.py','./rpmanager.py','child')
        else:
          self.pipe_file_in.readline()
      else:
        self.SendCloseMessage()

    def DisplayProgress(self, message):
      progress = self.counter / self.phases
      self.pipe_file_out.write(str(progress) + ' ' + message + '\n')
      self.pipe_file_out.flush()
      self.counter += 1
      
    def SendCloseMessage(self):
      self.SendMessage('1 quit\n')
      
    def SendMessage(self, message):
      self.pipe_file_out.write(message)
      self.pipe_file_out.flush()

    def LoadCache(self):
      TimeInit = time.time()
      if not self.loadcache_flag:
        self.IndicateProgress(True, 2)
        self.DisplayProgress('Start LoadCache')
        self.InfoCache.Files = get_rpm_unerrored_output('rpm -qpl ' + self.package_path).strip()
        self.InfoCache.FileList = self.InfoCache.Files.split()
        rpmq = get_rpm_unerrored_output('rpm -qp --queryformat \"%{Packager}<br>%{Distribution}<br>%{BuildTime:date}<br>%{License}<br>%{Url}\" '+self.package_path).split('<br>')
	self.InfoCache.MoreInfoCache = _('<b>Name:\t</b>') + self.InfoCache.Name + '\n'      
	self.InfoCache.MoreInfoCache += _('<b>Version:\t</b>') + self.InfoCache.Version      
	self.InfoCache.MoreInfoCache += _('<b>\t\tRelease:\t</b>') + self.InfoCache.Release + '\n'
	self.InfoCache.MoreInfoCache += _('<b>\nPackager:\t</b>') + rpmq[0].replace('<','(').replace('>',')') + '\n'      
	self.InfoCache.MoreInfoCache += _('<b>Package to:\t</b>') + rpmq[1] + '\n'      
	self.InfoCache.MoreInfoCache += _('<b>Build Date:\t</b>') + rpmq[2] + '\n'
	self.InfoCache.MoreInfoCache += _('<b>Size:\t\t</b>') + self.InfoCache.Size+ ' byte\n'
	self.InfoCache.MoreInfoCache += _('<b>License:\t\t</b>') + rpmq[3] + '\n'      
	self.InfoCache.MoreInfoCache += _('<b>Webpage:\t</b>') + rpmq[4] + '\n'
	self.InfoCache.MoreInfoCache += _('<b>\nDescription:\t</b>') + self.InfoCache.Description
        self.InfoCache.Provides = get_rpm_unerrored_output('urpmq --Provides ' + self.package_path)
        self.DisplayProgress('Provides request done')
        self.InfoCache.Dependencies = get_rpm_unerrored_output('urpmq -f --Requires-recursive ' + self.package_path)
        self.InfoCache.List = get_rpm_unerrored_output('urpmq -f --list ' + self.package_path).split()
        self.InfoCache.List.append(get_rpm_unerrored_output('urpmq -f ' + self.package_path))
        self.DisplayProgress('Dependency request done')
        self.loadcache_flag = True 
        self.IndicateProgress(False)
      print 'LoadCache(): ', time.time() - TimeInit

    def OnCheckButton1Pressed(self, widget):
        TimeInit = time.time()
        self.CheckButtonClear(1)
    	if self.loadcache_flag == False:
          self.LoadCache()
        if self.checkbutton1_pressed_flag == False:
 	  self.desc.set_markup(self.InfoCache.MoreInfoCache)
	  self.checkbutton1_pressed_flag = True
	else:
 	  self.desc.set_markup(self.InfoCache.DescriptionCache)
	  self.checkbutton1_pressed_flag = False
        print 'OnCheckButton1Pressed(): ', time.time() - TimeInit

    def OnCheckButton2Pressed(self, widget):
        TimeInit = time.time()
        self.CheckButtonClear(2)
    	if self.loadcache_flag == False:
          self.LoadCache()
        if self.checkbutton2_pressed_flag == False:
 	  self.desc.set_markup(self.InfoCache.Provides)
	  self.checkbutton2_pressed_flag = True
	else:
 	  self.desc.set_markup(self.InfoCache.DescriptionCache)
	  self.checkbutton2_pressed_flag = False
        print 'OnCheckButton2Pressed(): ', time.time() - TimeInit

    def OnCheckButton3Pressed(self, widget):
        TimeInit = time.time()
        self.CheckButtonClear(3)
    	if self.loadcache_flag == False:
    	  self.LoadCache()
        if self.checkbutton3_pressed_flag == False:
 	  self.desc.set_markup(self.InfoCache.Dependencies)
	  self.checkbutton3_pressed_flag = True
	else:
 	  self.desc.set_markup(self.InfoCache.DescriptionCache)
	  self.checkbutton3_pressed_flag = False
        print 'OnCheckButton3Pressed(): ', time.time() - TimeInit

    def OnCheckButton4Pressed(self, widget):
        TimeInit = time.time()
        self.CheckButtonClear(4)
        if self.checkbutton4_pressed_flag == False:
 	  self.desc.set_markup(self.InfoCache.Files)
	  self.checkbutton4_pressed_flag = True
	else:
 	  self.desc.set_markup(self.InfoCache.DescriptionCache)
	  self.checkbutton4_pressed_flag = False
        print 'OnCheckButton4Pressed(): ', time.time() - TimeInit

    def GetPackageInfo(self):
        TimeInit = time.time()
	package_path = self.package_filename.replace(' ', '\ ')
	self.package_path = package_path
        self.InfoCache = InfoCache(self)
	filename = self.package_filename
	if not os.path.exists(filename):
	  print "Missed:", filename
	filename = os.path.basename(filename)
	self.InfoCache.Filename = filename
        print 'GetPackageInfo(): ', time.time() - TimeInit
	
    def GetPackageName(self, filename):
        dirname = os.path.dirname(filename)
        filefilter = gtk.FileFilter()
        filefilter.add_pattern('*.rpm')
        filechooserdialog = gtk.FileChooserDialog (_('Please select a package'), buttons= (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT, gtk.STOCK_CANCEL, gtk.RESPONSE_REJECT))
        filechooserdialog.set_current_folder(dirname)
        filechooserdialog.set_filter(filefilter)
        response = filechooserdialog.run()
        filename = filechooserdialog.get_filename()
        filechooserdialog.destroy()        
        if response == gtk.RESPONSE_ACCEPT:
            return filename
        else:
            return None

    def ChangeWindow(self, old_window, new_window):
        TimeInit = time.time()
        pos_x, pos_y = old_window.get_position()
        width, height = old_window.get_size()
        new_window.move(pos_x, pos_y)
        new_window.resize(width, height)        
        new_window.show_all()
        old_window.hide_all()
        print 'ChangeWindow(): ', time.time() - TimeInit

    def PackageStatus(self):
        if self.InfoCache.source_package:
          self.status = _("Source package")
        elif self.InfoCache.Installed and self.InfoCache.new_package == 0:
          self.status = _("Installed")
        elif self.InfoCache.Installed and self.InfoCache.new_package == 1:
          self.status = _("Upgradable")
        elif self.InfoCache.Installed and self.InfoCache.new_package == -1:
          self.status = _("Downgradable")
        else:
          self.status = _("Installable")

    def display_rpm_info(self):
      TimeInit = time.time()
      if len(sys.argv) < 3 or self.install_flag:
        self.checkbutton1.set_sensitive(True)
        self.checkbutton2.set_sensitive(True)
        self.checkbutton3.set_sensitive(True)
        self.checkbutton4.set_sensitive(True)
        self.force_install_mode_flag = False
        self.force_uninstall_mode_flag = False
        self.undefined_error_flag = False
        self.loadcache_flag = False
        self.CheckButtonFlagClear()
        self.CheckButtonClear(0)
        if len(sys.argv) > 1 and not self.install_flag:
	  self.prev_button.set_sensitive(False)
        else:
	  self.prev_button.set_sensitive(True)
        if not self.InfoCache.Installed:
	  self.uninstall_button.set_sensitive(False)
          self.install_button.set_sensitive(True)
        elif self.InfoCache.new_package == 0:
          self.install_button.set_sensitive(False)
          self.uninstall_button.set_sensitive(True)
        else:
          self.install_button.set_sensitive(True)
          self.uninstall_button.set_sensitive(True)        
        self.PackageStatus()
        self.package_status.set_markup(self.status)
        self.glade_xml_wizard2_window.get_widget('title').set_markup(_("<b><big><big>%s %s %s</big></big></b>\n%s")%(self.InfoCache.Name,self.InfoCache.Version,self.InfoCache.Release,self.InfoCache.Summary))
        self.glade_xml_wizard2_window.get_widget("wizard2_window").set_title(_("Package: %s %s %s")%(self.InfoCache.Name,self.InfoCache.Version,self.InfoCache.Release))

        rpmsize = int (commands.getoutput('ls -s ' + self.package_filename).split()[0])
        icon_flag = False
        ics = 1
        if rpmsize < 10000: ### ITT javitani az ikon dolgot!
          rif = commands.getoutput('echo \'' + self.InfoCache.Files + '\' | grep \'.png\' | grep ' + str(ICON_X) + 'x' + str(ICON_Y) + ' | grep ' + self.InfoCache.Name2 +' | head -n 1')
          if rif != '':
            icon_flag = True
            home = commands.getoutput('echo ${HOME}')
            iconpath = home + '/.rpmanagericon.png'
            commands.getoutput('rpm2cpio ' + self.package_path + ' | cpio --to-stdout -i .' + rif + ' >' + iconpath)
            ics = int(commands.getoutput('du ' + iconpath).split()[0])
            print 'HTH ', ics
        if not icon_flag and ics:
          iconpaths = commands.getoutput('find /usr/share/icons/ -type f -name "*'+self.InfoCache.Name+'*" | grep png').split()
          iconpath = iconchooser(iconpaths)
        if iconpath != '' and ics:
          icon = gtk.gdk.pixbuf_new_from_file(iconpath)
          self.glade_xml_wizard2_window.get_widget('wizard2_window').set_icon(icon)            
        self.glade_xml_wizard2_window.get_widget("diskspace").set_markup(_("%d kilobytes")%(self.InfoCache.InstalledSize))
        self.desc = self.glade_xml_wizard2_window.get_widget("description")
        self.desc.set_markup("%s"%(self.InfoCache.DescriptionCache))
        if self.InfoCache.Installed:
          self.glade_xml_wizard2_window.get_widget("diskspacelabel").set_text(_("Already disk space used:"))
        if self.InfoCache.new_package == 1:
          self.glade_xml_wizard2_window.get_widget("label43").set_text(_("Upgrade"))
        if self.InfoCache.new_package == -1:
          self.glade_xml_wizard2_window.get_widget("label43").set_text(_("Downgrade"))
      else:
        self.prev_button.set_sensitive(False)
        self.uninstall_button.set_sensitive(False)
        self.checkbutton1.set_sensitive(False)
        self.checkbutton2.set_sensitive(False)
        self.checkbutton3.set_sensitive(False)
        self.checkbutton4.set_sensitive(False)
        self.package_status.set_markup(_("Multiple"))
        self.glade_xml_wizard2_window.get_widget('title').set_markup(_("<b><big><big>Multiple packages selected</big></big></b>"))
        self.glade_xml_wizard2_window.get_widget("wizard2_window").set_title(_("Multiple packages selected"))
        self.glade_xml_wizard2_window.get_widget("diskspace").set_markup(_("%d kilobytes")%(self.MultipleSize))
        self.desc = self.glade_xml_wizard2_window.get_widget("description")
        self.desc.set_markup(self.MultipleInfo)
      print 'display_rpm_info(): ', time.time() - TimeInit
