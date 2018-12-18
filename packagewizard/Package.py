#!/usr/bin/env python
# -*- coding: iso-8859-2 -*-

import time
import os

import singletons
from common import *
import common; _ = common._
from StoreRow import *
from Pixbufs import *

class Package(StoreRow):
    """This class describes a single package."""
    
    AGE_OLDER = 0
    AGE_INSTALLED = 1
    AGE_CONCURRENT = 2
    AGE_NEWER = 3
    AGE_NEWEST = 4
    AGE_NONINSTALLED = 5
    
    age_num_to_str = {
        AGE_OLDER: _('Older'),
        AGE_INSTALLED: _('Installed'),
        AGE_CONCURRENT: _('Concurrent'),
        AGE_NEWER: _('Newer'),
        AGE_NEWEST: _('Newest')
    }
    
    def GetAge(self):
        return self.age_num_to_str[self.age]
    
    def __init__(self):
        self.sources = []  # the list of sources that have the package

    def __repr__(self):
        return '<Package ' + self.longname + '>'

    def __str__(self):
        return self.longname

    def IsPackage(self):
        return True
    
    def AddSource(self, source):
        """Add 'source' to the list of sources of the package."""
        self.sources.append(source)

    def GetStoreRow(self):
        row = [False, ] * (self.STORE_LAST_ITEM)
        
        if self.is_library:
            row[self.STORE_TYPE_ICON] = Pixbufs.LIBRARY
        else:
            row[self.STORE_TYPE_ICON] = Pixbufs.APPLICATION
        
        row[self.STORE_TYPE_STATE] = self.is_library
        
        # STORE_CHECKBOX defaults False
        
        if self.is_installed:
            row[self.STORE_INSTALLED_ICON] = Pixbufs.INSTALLED
        else:
            row[self.STORE_INSTALLED_ICON] = Pixbufs.NOT_INSTALLED
        
        row[self.STORE_INSTALLED_STATE] = self.is_installed
        
        if self.is_upgradable:
            row[self.STORE_UPGRADABLE_ICON] = Pixbufs.UPGRADABLE
        else:
            row[self.STORE_UPGRADABLE_ICON] = Pixbufs.NOT_UPGRADABLE
        
        row[self.STORE_UPGRADABLE_STATE] = self.is_upgradable
        
        if len(self.sources) > 1:
            row[self.STORE_MULTIPLE_ICON] = Pixbufs.MULTIPLE
        else:
            row[self.STORE_MULTIPLE_ICON] = Pixbufs.SINGLE
        
        row[self.STORE_MULTIPLE_STATE] = len(self.sources) > 1
        
        row[self.STORE_NAME] = self.longname
        
        if self.time == -1:
            time_str = ''
        else:
            time_tuple = time.localtime(self.time)
            time_str = time.strftime('%Y-%m-%d %H:%M:%S', time_tuple)
        
        row[self.STORE_DATE_STRING] = time_str
        
        row[self.STORE_DATE_VALUE] = self.time
        
        row[self.STORE_SIZE_STRING] = get_human_readable_size(self.size)
        
        row[self.STORE_SIZE_VALUE] = self.size
        
        row[self.STORE_OBJECT] = self
        
        return row
    
    def GetVersion(self):
        prefix_len = len(self.shortname) + 1
        postfix_len = 5
        version = self.longname[prefix_len:-postfix_len]
        return version
    
    def GetCommandOutput(self, command, filter='', filter2 = ''):
        s = ''
        add_mode = filter == ''
        file = os.popen(command)
        for line in file:
            just_turned_on = False
            if filter and line.find(filter) == 0:
                just_turned_on = True
                add_mode = True
            if filter2 and line.find(filter2) == 0:
                add_mode = False
            if add_mode and not just_turned_on:
                s += line
        return s

    def GetInfo(self, detailed):
        infos = [
            (_('Type'), _('Package')),
            (_('Name'), self.shortname),
            (_('Version'), self.GetVersion()),
            (_('Category'), self.category),
            (_('Size'), get_human_readable_size(self.size))
        ]
        
        info_active = singletons.application.info_checkbutton.get_active()
        
        if not info_active:
            return infos
        
        if self.is_installed:
            command_infos = 'rpmquery -i ' + self.longname
        else:
            command_infos = 'urpmq -i ' + self.shortname
        
        debug(DEBUG_FORKS, command_infos)
        output_desc = self.GetCommandOutput(command_infos, 'Description :', 'Name        :')
        infos +=[('\n'+_('Description'), '\n'+output_desc)]
        
        if not detailed:
            return infos
            
        if self.is_installed:
            command_files = 'rpm -ql ' + self.longname
            command_changes = 'rpm -q --changelog ' + self.shortname
        else:
            command_files = 'urpmq -l ' + self.longname
            command_changes = 'urpmq --changelog ' + self.shortname
        
        debug(DEBUG_FORKS, command_changes)
        debug(DEBUG_FORKS, command_files)
        
        output_files = self.GetCommandOutput(command_files)
        output_changes = self.GetCommandOutput(command_changes)
            
        infos += [
            ('\n'+_('Change log'), '\n'+output_changes),
            ('\n'+_('File list'), '\n'+output_files)
        ]
                
        return infos
