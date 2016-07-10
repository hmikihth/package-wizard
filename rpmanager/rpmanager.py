#!/usr/bin/env python
# -*- coding: iso-8859-2 -*-

import pygtk
pygtk.require('2.0')
import os

import singletons
from common import *
from Pixbufs import *
from StoreRow import *
from Source import *
from Category import *
from Package import *
from Child import *
from Wizard import *
from PackagePool import *
from PackageView import *
from Application import *
import common; _ = common._

program_name =  os.path.basename(sys.argv[0])

if program_name == 'rpmanager':
    singletons.package_pool = PackagePool()
    singletons.application = Application()
    singletons.application.Init()
elif program_name == 'programkezelo':
    singletons.package_pool = PackagePool()
    singletons.application = Application()
    singletons.application.Init()
elif program_name == 'rpmanager-wizard':
    wizard = Wizard()
elif program_name == 'programtelepito':
    wizard = Wizard()
elif len(sys.argv) == 2:
    if sys.argv[1] == 'child':
        child = Child()
else:
    print _('You have to run this program either using the "rpmanager" or the ' \
        '"rpmanager-wizard" command.')
