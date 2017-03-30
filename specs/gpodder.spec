Name: 	 	gpodder
Summary: 	A graphical podcast catcher
Summary(hu): 	Egy grafikus podcast lekapó program
Version: 	3.7.0
Release: 	%mkrel 2
Source:		http://gpodder.org/src/%{name}-%{version}.tar.gz
URL:		http://gpodder.org/
License:	GPLv3+ and LGPLv2+
Group:		Networking/News
BuildArch:	noarch
BuildRequires:	python-devel
BuildRequires:	python-feedparser >= 5.0.1
BuildRequires:	python-mygpoclient
BuildRequires:	imagemagick
BuildRequires:	desktop-file-utils
BuildRequires:	help2man
BuildRequires:	intltool
Requires:	pygtk2.0 >= 2.6
Requires:	python-feedparser >= 5.0.1
Requires:	python-mygpoclient >= 1.4
Requires:	python-dbus
Suggests:	python-gpod
Suggests:	python-eyed3
Requires:	python-webkitgtk
Suggests:	bluez-utils bluez-gnome

%description

gPodder is a Podcast reciever/catcher written in Python, using GTK. It manages
podcast feeds for you and automatically downloads all podcasts from as many
feeds as you like.

%description -l hu
KEDVES ANDRÁS IDE KELL A SZÖVEGT LEFORDÍTANI

%prep
%setup -q
%autopatch -p1

rm -rf share/gpodder/extensions/ubuntu_*.py

%install
%makeinstall_std

%find_lang %{name}

desktop-file-install --vendor="" \
  --add-category="GTK;Network;News" \
  --dir %{buildroot}%{_datadir}/applications \
		%{buildroot}%{_datadir}/applications/*

%files -f %{name}.lang
%doc README
%{_bindir}/*
%{_datadir}/dbus-1/services/org.gpodder.service
%{_datadir}/%{name}/
%{py_puresitedir}/%{name}/
%{py_puresitedir}/*.egg-info
%{_mandir}/man1/*
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*/apps/gpodder.*


%changelog
* Sun Mar 13 2016 Charles Barcza <info@blackpanther.hu> 3.7.0-2bP
- build for blackPanther OS v16.x
- fix requires after test
------------------------------------------------------------------

* Sun Mar 13 2016 Charles Barcza <info@blackpanther.hu> 3.7.0-1bP
- build for blackPanther OS v14.x
--------------------------------------------------------------

