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

def update_messages():
    # Create empty directory
    os.system("rm -rf .tmp")
    os.makedirs(".tmp")
    # Collect UI files
    for filename in glob.glob1("modules_uic", "*.ui"):
        os.system("pyuic5 -o .tmp/ui_%s.py modules_uic/%s" % (filename.split(".")[0], filename))
    # Collect Python files
    for filename in glob.glob1("modules_uic", "*.py"):
        shutil.copy("modules_uic/%s" % filename, ".tmp")
    # Generate POT file
    os.system("xgettext --default-domain=%s --keyword=_ --keyword=i18n --keyword=ki18n -o po/%s.pot .tmp/*" % (about.catalog, about.catalog))
    # Update PO files
    for item in os.listdir("po"):
        if item.endswith(".po"):
            os.system("msgmerge -q -o .tmp/temp.po po/%s po/%s.pot" % (item, about.catalog))
            os.system("cp .tmp/temp.po po/%s" % item)
    # Remove temporary directory
    os.system("rm -rf .tmp")

def makeDirs(dir):
    try:
        os.makedirs(dir)
    except OSError:
        pass

def have_gettext():
    return subprocess.getoutput("pyuic5 --help").find("--gettext") > -1
    
class Build(build):
    def run(self):
        os.system("rm -rf build")
        os.system("mkdir -p build/fusionlogic/packagewizard")
        print ("Copying PYs Src...")
        os.system("cp src/*.py build/fusionlogic/packagewizard")
        print ("Generating UIs...")
        for filename in glob.glob1("modules_uic", "*.ui"):
            if have_gettext():
                os.system("pyuic5 -g -o build/fusionlogic/packagewizard/%s.py modules_uic/%s" % (filename.split(".")[0], filename))
            else:
                os.system("pyuic5 -o build/fusionlogic/packagewizard/%s.py modules_uic/%s" % (filename.split(".")[0], filename))
        print ("Generating RCs for build...")
        for filename in glob.glob1("./", "*.qrc"):
            os.system("pyrcc5 %s -o build/%s_rc.py" % (filename, filename.split(".")[0]))
            print ("Generating RCs for tests...")
            os.system("pyrcc5 %s -o test/%s_rc.py" % (filename, filename.split(".")[0]))
        for filename in glob.glob1("./", "*.in"):
            os.system("cat %s > build/%s.py" % (filename, filename.split(".")[0]))


class Install(install):
    def run(self):
        os.system("./setup.py build")
        if self.root:
            kde_dir = "%s/usr" % self.root
        bin_dir = os.path.join(kde_dir, "bin")
        locale_dir = os.path.join(kde_dir, "share/locale")
        autostart_dir = os.path.join(kde_dir, "share/autostart")
        project_dir = os.path.join(kde_dir, "share/apps", about.appName)
        # Make directories
        print ("Making directories...")
        sys.exit()
        makeDirs(bin_dir)
        #makeDirs(locale_dir)
        makeDirs(autostart_dir)
        makeDirs(project_dir)
        # Install desktop files
        print ("Installing desktop files...")
        for filename in glob.glob1("data", "*.desktop"):
            shutil.copy("data/%s" % filename, autostart_dir)
        # Install codes
        print ("Installing codes...")
        os.system("cp -R build/* %s/" % project_dir)
        # Install locales
        print ("Installing locales...")
        for filename in glob.glob1("po", "*.po"):
            lang = filename.rsplit(".", 1)[0]
            os.system("msgfmt po/%s.po -o po/%s.mo" % (lang, lang))
            try:
                os.makedirs(os.path.join(locale_dir, "%s/LC_MESSAGES" % lang))
            except OSError:
                pass
            shutil.copy("po/%s.mo" % lang, os.path.join(locale_dir, "%s/LC_MESSAGES" % lang, "%s.mo" % about.catalog))
        # Rename
        print ("Renaming application.py...")
        #shutil.move(os.path.join(project_dir, "application.py"), os.path.join(project_dir, "%s.py" % about.appName))
        # Modes
        print ("Changing file modes...")
        os.chmod(os.path.join(project_dir, "%s.py" % about.appName), "0755")
        # Symlink
        try:
            if self.root:
                os.symlink(os.path.join(project_dir.replace(self.root, ""), "%s.py" % about.appName), os.path.join(bin_dir, about.appName))
            else:
                os.symlink(os.path.join(project_dir, "%s.py" % about.appName), os.path.join(bin_dir, about.appName))
        except OSError:
            pass


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

    packages=["packagewizard"],
#    scripts=["bin/package-wizard"],
    install_requires = ["argparse", "configparser"],
    cmdclass = {
            'build': Build,
            'install': Install,
                }
)
