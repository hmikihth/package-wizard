%global __requires_exclude perl\\(*

Summary:	Quick graphical package installer tool
Summary(hu):	Gyors grafikus csomagtelepítő eszköz
Name:		rpmanager
Version:	0.29
Release:	%mkrel 5
Source0:	%{name}-20150722.tar.xz
Source2:	programkezelo
Source3:	programtelepito
Source4:	mozilla-hack
Source5:	edit-repos
Source10:	rpmanager.png
Source11:	rpmanager-wizard.png
URL:		http://www.blackpanther.hu/
License:	Free
Group:		System/Configuration/Packaging
BuildRoot:	 %_tmppath/%name-%version-buildroot
BuildArch:	 noarch
Distribution:	blackPanther OS.
Vendor:    	blackPanther Europe

Provides: 	rpmmanager
Provides:	programkezelo
Requires:	python >= 2.6.1 python-base >= 2.6.1-1bP pygtk2.0 >= 2.4.1 pygtk2.0-libglade >= 2.4.1 
Requires:	gurpmi %name-common = %version


%description -l hu
Szoftvercsomag kezelő és telepítő blackPanther OS 
rendszerekhez.

Ez az eszköz egy roppant könnyen használható program.
Kattintson, olvasson és telepítsen bármilyen csomagot.
Az alapértelmezett csomagkezelő motor az urpmi vagy a 
smart

%description 
Software package manager and installer for 
blackPanther OS distributions. 

This tool very easy to use application. 
Click , read description and install any packages. 
Default packages engine urpmi or smart.

%files
#-f ../file.list.%{name}
%doc
%defattr(-,root,root,0755)
%_bindir/programkezelo
%_bindir/rpmanager
%_sbindir/edit-repos
%_datadir/%name/edit-repos/*
%_datadir/%name/programkezelo
%_datadir/%name/progressbar.pyc
%_datadir/%name/rpmanager
%_datadir/applications/blackPanther-%{name}.desktop
#%_datadir/%name/rpmanager_hth.py
%_iconsdir/*/%name.png
%_iconsdir/%name.png
%_datadir/%name/gui/gnome-stock-trash.png
%_datadir/%name/gui/messages.po
%_datadir/%name/gui/newlangs.pot
%_datadir/%name/gui/pixmaps
%_datadir/%name/gui/left-arrow-small.png
%_datadir/%name/gui/power-up.png
%_datadir/%name/gui/refresh.png
%_datadir/%name/gui/remove.png

%package common
Group:   System/Configuration/Packaging
Summary: Common package for RPManager
Requires: rpmmanager

%description common
Common package for blackPanther RPManager

%files common
%defattr(-,root,root)
%_datadir/%name/gui/application.png
%_datadir/%name/gui/cdrom.png
%_datadir/%name/gui/cancel.png
%_datadir/%name/gui/edit.png
%_datadir/%name/gui/install.png
%_datadir/%name/gui/rpmanager.png
%_datadir/%name/gui/upgradable.png
%_datadir/%name/gui/installed.png
%_datadir/%name/gui/install.gif
%_datadir/%name/gui/not-installed.png
%_datadir/%name/gui/not-upgradable.png
%_datadir/%name/gui/multiple.png
%_datadir/%name/gui/single.png
%_datadir/%name/gui/upgradable.png
%_datadir/%name/gui/library.png
%_datadir/%name/gui/*.glade
%_datadir/%name/gui/*.gladep
%_datadir/%name/gui/%name-logo.jpg
%_datadir/%name/gui/search.gif
%_datadir/%name/gui/internet.png
%_datadir/%name/conflicts/
%_datadir/%name/locale/
%_datadir/%name/Application.pyc
%_datadir/%name/PackagePool.pyc
%_datadir/%name/Package.pyc
%_datadir/%name/PackageView.pyc
%_datadir/%name/ProgressIndicator.coverage
%_datadir/%name/ProgressIndicator.pyc
%_datadir/%name/findsu
%_datadir/%name/Category.pyc
%_datadir/%name/Child.pyc
%_datadir/%name/common.pyc
%_datadir/%name/Pixbufs.pyc
%_datadir/%name/singletons.pyc
%_datadir/%name/Source.pyc
%_datadir/%name/StoreRow.pyc
%_datadir/%name/rpmanager.py*
%_datadir/%name/rpmanager.py


#******************************************************************
%package wizard
Group:   System/Configuration/Packaging
Summary:  Graphically RPM package install wizard
Requires: %name-common 
Provides: rpmmanager

%description wizard
RPM installer wizard for blackPanther OS 

%files wizard
%defattr(-,root,root)
%_bindir/programtelepito
%_bindir/rpmanager-wizard
%_datadir/rpmanager/Wizard.pyc
%_datadir/rpmanager/sh*
%_datadir/applications/blackPanther-programtelepito.desktop
%_datadir/%name/gui/wizard-small.png
%_datadir/%name/gui/right-arrow.png
%_datadir/%name/gui/install-small.png
%_datadir/%name/gui/cancel-small.png
%_datadir/%name/gui/remove-small.png
%_datadir/%name/programtelepito
%_datadir/%name/rpmanager-wizard
%_iconsdir/*/%name-wizard.png
%_iconsdir/%name-wizard.png



# ************************************************************
%prep
%setup -q -n %{name}

%build
rm -f *.pyc
python -m compileall .
mv rpmanager.py ../
mv shcomm.py ../
rm -f *.old messages* *.backup *.e3* make* *.sh *.py TODO gurpmi ChangeLog
rm -f gui/*.bak
rm -rf test
mv ../rpmanager.py .
mv ../shcomm.py .
find . -type f -name "*.xcf" | xargs rm -rf
find . -type f -name "rpmanager2.*" | xargs rm -rf
find . -type f -name "*.ui*" | xargs rm -rf
find . -type f -name "*-logo.png" | xargs rm -rf

%install
rm -rf $RPM_BUILD_ROOT
rm -rf ../file.list.%{name}
mkdir -p %buildroot/%_datadir
mkdir -p %buildroot/%_bindir
cp -rf ../%name %buildroot/%_datadir
# icons
%__mkdir_p %buildroot{%_liconsdir,%_iconsdir,%_miconsdir}
convert -scale 48x48 %SOURCE10 %buildroot/%_liconsdir/%{name}.png
convert -scale 32x32 %SOURCE10 %buildroot/%_iconsdir/%{name}.png
convert -scale 16x16 %SOURCE10 %buildroot/%_miconsdir/%{name}.png

# icons
%__mkdir_p %buildroot{%_liconsdir,%_iconsdir,%_miconsdir}
convert -scale 48x48 %SOURCE11 %buildroot/%_liconsdir/%{name}-wizard.png
convert -scale 32x32 %SOURCE11 %buildroot/%_iconsdir/%{name}-wizard.png
convert -scale 16x16 %SOURCE11 %buildroot/%_miconsdir/%{name}-wizard.png

#cp -f /tmp/%{name}.tar.bz2 $SOURCEDIR
#bunzip2 -cd $RPM_BUILD_DIR/%{name}.tar.bz2 | tar -C %buildroot/%_datadir/ -xf-
#bunzip2 -cd %SOURCE0 | tar -C %buildroot/%_datadir/ -xf-

#cp -rf * %buildroot/%_datadir/%{name}
#ln -s  %_datadir/%{name}/%{name}.py %buildroot%_bindir/programkezelo 
# display manager entry
install -m 0755 %SOURCE2 %buildroot/%_bindir/programkezelo
#install -m 0755 %SOURCE3 %buildroot/%_bindir/programtelepito
install -m 0755 %SOURCE4 %buildroot/%_bindir/programtelepito
install -m 0755 -D %SOURCE5 %buildroot/%_sbindir/edit-repos

#mkdir -p %buildroot/%{_bindir}/programkezelo

#rm -rf %buildroot/%_datadir/%{name}/gui/*.bak 

#chmod 0755 %buildroot/%_datadir/%{name}/gui
#chmod 0755 %buildroot/%_bindir/programkezelo
#chmod 0755 %buildroot/%_bindir/programtelepito

install -d %buildroot/%_datadir/kde4/services/ServiceMenus/
#install -m 644 %SOURCE3 %buildroot/%_datadir/kde4/services/ServiceMenus/

mkdir -p %buildroot%_datadir/applications
cat > %buildroot%_datadir/applications/blackPanther-programtelepito.desktop << EOF
[Desktop Entry]
Name=Software Installer Wizard
Name[hu]=Szoftver telepítővarázsló
Comment=Graphical front end to install RPM files
Comment[hu]=Grafikus felületű RPM csomagtelepítő
Exec=%{_bindir}/programtelepito "%%F"
Terminal=false
Icon=%{name}-wizard
Type=Application
StartupNotify=true
Categories=GTK;X-blackPantherOS-.hidden;
MimeType=application/x-rpm;application/x-urpmi;
EOF

#mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/blackPanther-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=RPManager
Name[hu]=RPManager
GenericName=Application packages management
GenericName[hu]=Programcsomagok kezelése
Comment=blackPanther OS applications manager
Comment[hu_HU]=blackPanther OS programokcsomagok kezelése
Exec=%{_bindir}/programkezelo
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=GTK;System;Packaging;X-blackPantherOS;PackageManager;Settings;
EOF

rm -r %buildroot%_datadir/%name/gui/rpmanager.glade.*
#rm -r %buildroot%_datadir/%name/gui/rpmanager.glade.2
#rm -r %buildroot%_datadir/%name/gui/rpmanager.glade.h
#rm -r %buildroot%_datadir/%name/gui/rpmanager.glade.simple
rm -r %buildroot%_datadir/%name/bookmark*
rm -r %buildroot%_datadir/%name/distri*

rm -f %buildroot%_datadir/%name/Wiz.diff
rm -f %buildroot%_datadir/%name/Wiz*-old

ln -sf programkezelo %buildroot%_bindir/rpmanager
ln -sf programtelepito %buildroot%_bindir/rpmanager-wizard


cd $RPM_BUILD_ROOT

find . -type d -fprint $RPM_BUILD_DIR/file.list.%{name}.dirs
find . -type f -fprint $RPM_BUILD_DIR/file.list.%{name}.files.tmp
sed '/\/man\//s/$/.bz2/g' $RPM_BUILD_DIR/file.list.%{name}.files.tmp > $RPM_BUILD_DIR/file.list.%{name}.files
find . -type l -fprint $RPM_BUILD_DIR/file.list.%{name}.libs
sed '1,2d;s,^\.,\%attr(-\,root\,root) \%dir ,' $RPM_BUILD_DIR/file.list.%{name}.dirs > $RPM_BUILD_DIR/file.list.%{name}
sed 's,^\.,\%attr(-\,root\,root) ,' $RPM_BUILD_DIR/file.list.%{name}.files >> $RPM_BUILD_DIR/file.list.%{name}
sed 's,^\.,\%attr(-\,root\,root) ,' $RPM_BUILD_DIR/file.list.%{name}.libs >> $RPM_BUILD_DIR/file.list.%{name}


%pre
if [ ! -f /etc/blackPanther-release ];then
           [ -n "$DISPLAY" ] && zenity --info --text "This is the system not a blackPanther OS, please download and try it: www.blackpanther.hu"
           [ ! -n "$DISPLAY" ] && echo -n "This is the system not a blackPanther OS, please download and try it: www.blackpanther.hu"
fi

######## This function Copyright(c) use Only blackPanrher OS packages
if [ -f /etc/blackPanther-release ] && [ -f /usr/bin/programkezelo ]; then
    touch /tmp/.rpm%{name}
fi



%post 
######## This function Copyright(c) use Only blackPanrher OS 

if [ -f /usr/share/applications/blackPanther-gurpmi.desktop ]; then
    mv /usr/share/applications/blackPanther-gurpmi.desktop /usr/share/rpmanager
fi


%postun
if [ -f /usr/share/rpmanager/blackPanther-gurpmi.desktop ]; then
    mv -f /usr/share/rpmanager/blackPanther-gurpmi.desktop /usr/share/applications/ 
fi
######## This function Copyright(c) Only blackPanrher OS
if [ -f /etc/blackPanther-release ] && [ -f /tmp/.X0-lock ];then
    if [ -f /usr/bin/programkezelo ]; then
    echo "exit"
      else
      # remove desktop icons
	for D in /home/*;do
	if [ -d $D ];then
	 rm -rf $D/Desktop/%name.desktop
	fi
	done
    fi
fi


%clean
rm -rf $RPM_BUILD_ROOT/*
rm -rf $RPM_BUILD_DIR/%{name}
rm -rf ../file.list.%{name}




%changelog
* Wed Jul 22 2015 Charles Barcza <info[x]blackpanther.hu> 0.29-5bP
- build for blackPanther OS v14.x
------------------------------------------------------------------

* Fri Sep 02 2011 Charles Barcza <info[x]blackpanther.hu> 0.29-4bP
- bugfix for install status check by Hmiki
---------------------------------------------------------
* Fri Sep 02 2011 Charles Barcza <info[x]blackpanther.hu> 0.29-3bP
- bugfix release for broken package install
---------------------------------------------------------

* Wed Mar 02 2011 Charles Barcza <info[x]blackpanther.hu> 0.29-2bP
- rebuild for blackPanther OS v11.x
---------------------------------------------------------

* Wed Dec 02 2009 Charles Barcza <info[x]blackpanther.hu> 0.29-1bP
- rebuild for blackPanther OS v10.x
- update to new
- fixed wizard start
---------------------------------------------------------

* Tue Dec 1 2009 Charles Barcza <info[x]blackpanther.hu> 0.28-1bP
- rebuild for blackPanther OS v10.x
- change Wizard
- create main common wizard pack
---------------------------------------------------------
* Mon Nov 30 2009 Charles Barcza <info[x]blackpanther.hu> 0.27-2bP
- rebuild for blackPanther OS v10.x
---------------------------------------------------------

* Wed Sep 30 2009 Karoly Barcza <kbarcza[x]blackpanther.hu>
- 0.27
- bugfix release
---------------------------------------------------------
* Thu Aug 20 2009 Karoly Barcza <kbarcza[x]blackpanther.hu>
- new revision
- add refresher support
---------------------------------------------------------
* Tue Jun 28 2009 Karoly Barcza <kbarcza[x]blackpanther.hu>
- new revision
---------------------------------------------------------
* Sat Jun 26 2009 Karoly Barcza <kbarcza[x]blackpanther.hu>
- new revision
- add rpmanager access
- add source editor access
---------------------------------------------------------
* Sat Jun 20 2009 Karoly Barcza <kbarcza[x]blackpanther.hu>
- new revision
---------------------------------------------------------
* Wed Jun 17 2009 Karoly Barcza <kbarcza[x]blackpanther.hu>
- new revision
---------------------------------------------------------
* Tue Jun 16 2009 Karoly Barcza <kbarcza[x]blackpanther.hu>
- change programtelepito to mozilla-hack
---------------------------------------------------------
* Tue Jun 16 2009 Karoly Barcza <kbarcza[x]blackpanther.hu>
- new release
---------------------------------------------------------
* Mon Jun 15 2009 Karoly Barcza <kbarcza[x]blackpanther.hu>
- new release
---------------------------------------------------------
* Sat Jun 13 2009 Karoly Barcza <kbarcza[x]blackpanther.hu>
- new release
---------------------------------------------------------
* Tue Jun 09 2009 Karoly Barcza <kbarcza[x]blackpanther.hu>
- new release
---------------------------------------------------------
* Mon Jun 08 2009 Karoly Barcza <kbarcza[x]blackpanther.hu>
- dependency check
---------------------------------------------------------
* Fri Jun 05 2009 Karoly Barcza <kbarcza[x]blackpanther.hu>
- fixate dialog size
- fix design
- update localisation
----------------------------------------------------------
* Thu Jun 04 2009 Karoly Barcza <kbarcza[x]blackpanther.hu>
- redesigned wizard 
- new release for v9.1
----------------------------------------------------------
* Mon Nov 03 2008 Karoly Barcza <kbarcza[x]blackpanther.hu>
- add more design
- add detect conflict
- add uninstall button to wizard dialog
- more designes items
- fix install-upgrade method
- update translations

* Wed Oct 29 2008 Karoly Barcza <kbarcza[x]blackpanther.hu>
- fix Wizard window
- add icon in progress window
- replace startup scripts
- add desktop file
- update translation

* Tue Sep 1 2005 Karoly Barcza <kbarcza[x]blackpanther.hu>
- fixed long filename by mondalaci
- add fixed startup scripts
- fix wizard dialog
- fix translation
- first witout dev release

* Mon Aug 29 2005 Karoly Barcza <kbarcza[x]blackpanther.hu>
- new dev version 

* Thu Jun 28 2005 Karoly Barcza <kbarcza[x]blackpanther.hu>
- fix fileinfo

* Mon Jun 27 2005 Karoly Barcza <kbarcza[x]blackpanther.hu>
- modified gui
- new icon
- new menu
* Sat Jun 12 2005 Karoly Barcza <kbarcza[x]blackpanther.hu>
- new devolper version for testers

* Thu Apr 19 2005 Karoly Barcza <kbarcza[x]blackpanther.hu>
- new version




