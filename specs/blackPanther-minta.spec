#Copyright#######################################################################
#										#
#  Sample spec written by Charles K Barcza forblackPanther OS ..	  	#
#										#
#################################################################################

# debug csomagot létre kell hozni 1 nem kell létrehozni 0
%define build_debug	0

# régi formátum - debug csomagot létre kell hozni 1 nem kell létrehozni 0
%define _enable_debug_packages 0

# hagyja ki a függőságek közül az ocaml( kezdetü csomagokat
%global __requires_exclude %{?__requires_exclude|}ocaml\\(*

# hagyja ki a biztosítja listábaól a perl\\(xy csomagokat
%global __provides_exclude perl\\(DebugTexinfo|perl\\(Texinfo|perl\\(Unicode

# az EVRD definiálása (14.x-től már nincs rá szükség)
%define EVRD %{?epoch:%{epoch}:}%{?version:%{version}}%{?release:-%{release}}%{?distepoch::%{distepoch}}

%define groups 	Applications/Games/Arcade

Summary:	build from tar archive to rpm pack
Summary(hu):	csinaltuk tar csomaból rpm-et
Name:		minta
Version:	0.0.1
Release:	%mkrel 1
## a 4.1 blackPanther csomag 'release' formátuma már "bP" a 4.0nál még "BPL" volt 
Source0:	%{name}.tar.bz2
URL:		http://www.blackpanther.hu/
License:	GPL
Group:		%{groups}
BuildRoot:	 %_tmppath/%name-%version-buildroot #telepitesi könyvtár definiálása
#BuildArch:	 noarch  (ha nincs megadva automatikusan i586 optim)
Distribution:	blackPanther OS
Vendor:    	blackPanther Europe
Packager:  	Karoly Barcza <kbarcza@blackpanther.hu> 

%description -l hu
rpmbuild spec hogyan
  ******************************************************************************
 *										*
 *  A minta scriptet Barcza Károly írta a blackPanther OS.-hez 			*
 *										*
  ******************************************************************************


%description 
rpmbuild spec hotwo
  ******************************************************************************
 *										*
 *  Sample script written by Charles K. Barcza, for blackPanther OS. ...  	*
 *										*
  ******************************************************************************

%prep
%setup -q  
# -q a csendes mód

%build
#export PARAMATEREK 
%configure2_5x --prefix=%_prefix

####### ilyen formában a make paraméterezve is van -j CPUSZÁM -O2 
%make_build

%install
## töröljük a korábbi állományokat
rm -rf $RPM_BUILD_ROOT
## standard install
%make_install


#MENU########################################################################
%define  nameicon PATH/AHOL/EGY/HASZNALHATO/KEP/VAN.png
mkdir -p -m755 %{buildroot}{%_liconsdir,%_iconsdir,%_miconsdir}
convert -scale 48x48 %{nameicon} %{buildroot}/%{_liconsdir}/%{name}.png
convert -scale 32x32 %{nameicon} %{buildroot}/%{_iconsdir}/%{name}.png
convert -scale 16x16 %{nameicon} %{buildroot}/%{_miconsdir}/%{name}.png

# ez hamarosan változni fog az SVG képekre való teljes átállás után. (végre)

#Menu entry for blackPanther 6.x előtt! Ezt követően nem kell.
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}): needs="x11" section="%groups" \
title="Igy jelenik meg a menuben" \
longtitle="Minta ...." command="parancs " \
icon="warning" terminal="false"
EOF

## 10.x felett pótöljuk a menüelemet ha hiányzik
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/blackPanther-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=%name
Comment=
Exec=%{_bindir}/%{name} %U
Icon=%{name}
Terminal=false
Type=Application
StartupNotify=true
Categories=EREDETI;GTK;KETEGORIA;X-blackPantherOS-MoreApplications-Games-Arcade;Game;ArcadeGame;
EOF

#MENU END ###################################################################

%pre
# a csomag telepítése előtt futó műveletek


%post 
# a csomag telepítése után futó műveletek

# makrók
# frissítések (már nem kell ert triggerből megy)
%update_menus
%update_desktop_database
%update_mime_database
######## This function Copyright(c) blackPanrher OS packages
if [ -f /etc/blackPanther-release ] && [ -f /tmp/.X0-lock ];then
 if [ -f /tmp/.rpm%{name} ]; then
    bubblemsg upgrade %{name}
    rm -f /tmp/.rpm%{name}
      else
     bubblemsg install %{name}
    fi

fi

%preun
# a csomag törlése előtt futó műveletek

%postun
# a csomag törlése után futó műveletek

# makrók
# frissítések (már nem kell ert triggerből megy)
%clean_menus
%clean_desktop_database
%clean_mime_database

######## Feleslegessé vált asztali ikon törlése - Copyright(c) blackPanrher OS packages
if [ -f /etc/blackPanther-release ] ;then
    if [ -f /usr/bin/%{name} ]; then
    echo "exit"
      else
      # remove desktop icons
	for D in /home/*;do
	if [ -d $D ];then
	 rm -rf $D/Desktop/%name.desktop
	fi
	done
	[ -x /usr/bin/bubblemsg ]&&bubblemsg uninstall %{name}
    fi
fi

%files
%doc README COPYRIGHT stb... és bekerülnek a /usr/share/doc/csomagneve-verzió/alá
%defattr(-,root,root,0755)
%_menudir/*
#lehet ilyen formában
%{_menudir}/%{name}
# vagy ilyen formában ábrázolni
%_datadir/pixmaps/*

###TAKARÍTÁS
%clean
rm -rf $RPM_BUILD_ROOT/*
rm -rf $RPM_BUILD_DIR/%{name}


%changelog
* Mon Jul 19 2004 Karoly Barcza <kbarcza@blackpanther.hu>
- leírása annak hogy mi történt a csomaggal vagy milyen verzió. stb

