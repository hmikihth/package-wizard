#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
#*********************************************************************************************************
#*   __     __               __     ______                __   __                      _______ _______   *
#*  |  |--.|  |.---.-..----.|  |--.|   __ \.---.-..-----.|  |_|  |--..-----..----.    |       |     __|  *
#*  |  _  ||  ||  _  ||  __||    < |    __/|  _  ||     ||   _|     ||  -__||   _|    |   -   |__     |  *
#*  |_____||__||___._||____||__|__||___|   |___._||__|__||____|__|__||_____||__|      |_______|_______|  *
#*http://www.blackpantheros.eu | http://www.blackpanther.hu - kbarcza[]blackpanther.hu * Charles K Barcza*
#*************************************************************************************(c)2002-2019********
#	    Initial code written by Charles K Barcza in december of 2018 
#          The maintainer of the PackageWizard: Miklos Horvath * hmiki[]blackpantheros.eu

import os
import glob
import shutil
import sys
#import about

from distutils.core import setup
from distutils.cmd import Command
from distutils.command.build import build
from distutils.command.install import install
from setuptools import setup
import subprocess
    
with open("README.md", "r") as fh:
    long_description = fh.read()

def have_gettext():
    return subprocess.getoutput("pyuic5 --help").find("--gettext") > -1

def update_messages():
    # Create empty directory
    pkgname="fusionlogic-common"
    os.system("rm -rf .tmp")
    os.makedirs(".tmp")
    # Collect UI files
    for filename in glob.glob1("modules_uic", "*.ui"):
        if have_gettext():
            os.system("pyuic5 -g -o .tmp/ui_%s.py modules_uic/%s" % (filename.split(".")[0], filename))
        else:
            os.system("pyuic5 -o .tmp/ui_%s.py modules_uic/%s" % (filename.split(".")[0], filename))
    # Collect Python files
    for filename in glob.glob1("modules_uic", "*.py"):
        shutil.copy("modules_uic/%s" % filename, ".tmp")
    # Generate POT file
    os.system("xgettext --default-domain=%s --keyword=_ --keyword=i18n --keyword=ki18n -o po/%s.pot .tmp/* src/*.py" % (pkgname,pkgname))
    # Update PO files
    for item in os.listdir("po"):
        if item.endswith(".po"):
            os.system("msgmerge -q -o .tmp/temp.po po/%s po/%s.pot" % (item,pkgname))
            os.system("cp .tmp/temp.po po/%s" % item)
    # Remove temporary directory
    os.system("rm -rf .tmp")
    
class Build(build):
    def run(self):
        os.system("rm -rf build")
        os.system("mkdir -p build/lib/fusionlogic/packagewizard")
        os.system("mkdir -p build/scripts-3.7")
        print ("Copying PYs Src...")
        os.system("cp src/*.py build/lib/fusionlogic/packagewizard")
        print ("Generating UIs...")
        for filename in glob.glob1("modules_uic", "*.ui"):
            if have_gettext():
                os.system("pyuic5 -g -o build/lib/fusionlogic/packagewizard/%s.py modules_uic/%s" % (filename.split(".")[0], filename))
            else:
                os.system("pyuic5 -o build/lib/fusionlogic/packagewizard/%s.py modules_uic/%s" % (filename.split(".")[0], filename))
        os.system("sed -i 's/import raw_rc/from fusionlogic import raw_rc\\nfrom fusionlogic.packagewizard import raw_rc/g' build/lib/fusionlogic/packagewizard/packagewizardMain.py")
        print ("Generating RCs for build...")
        for filename in glob.glob1("./", "*.qrc"):
            os.system("pyrcc5 %s -o build/lib/fusionlogic/packagewizard/%s_rc.py" % (filename, filename.split(".")[0]))
#            print ("Generating RCs for tests...")
#            os.system("pyrcc5 %s -o test/%s_rc.py" % (filename, filename.split(".")[0]))
        for filename in glob.glob1("./", "*.py"):
            if filename not in ["setup.py"]:
                os.system("cat %s > build/scripts-3.7/%s" % (filename, filename[:-3]))


class Install(install):
    def run(self):
        install.run(self)

if "update_messages" in sys.argv:
    update_messages()
    sys.exit(0)

setup(
    name="fusionlogic-packagewizard",

    version="0.0.1",

    description="The FusionLogic-PackageWizard is a PyQt5 package installer.",
    long_description = """
    The FusionLogic-PackageWizard is a PyQt5 based package installer via PackageKit.
    Project idea and design: Charles K. Barcza
    Maintainer: Miklos Horvath 
    """,
    
    url="https://github.com/blackPantherOS/package-wizard",

    author="Charles Barcza, Miklos Horvath",
    maintainer="Miklos Horvath <hmiki@blackpantheros.eu>",
    
    license="GPLv3+",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",

        "Topic :: Desktop Environment",
        "Topic :: Desktop Environment :: K Desktop Environment (KDE)",
        "Topic :: System :: Software Distribution",
        "Environment :: X11 Applications :: Qt",
        
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

        "Operating System :: POSIX :: Linux",
        "Operating System :: POSIX :: BSD :: FreeBSD",
        "Operating System :: POSIX :: BSD :: OpenBSD",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],

    package_dir={"fusionlogic":"build/lib/fusionlogic"},
    packages=["fusionlogic"],
    scripts=["build/scripts-3.7/packagewizard"],
    data_files  = [('/'.join(['usr']+e.split('/')[1:-1]), [e]) for e in subprocess.getoutput("find build/locale").split() if ".mo" in e],
    install_requires = ["argparse", "configparser","fusionlogic-common"],
    cmdclass = {
        'build': Build,
        'install': Install,
    }
)
