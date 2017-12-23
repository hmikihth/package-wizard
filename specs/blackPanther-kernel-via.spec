%define __spec_install_post /usr/lib/rpm/brp-compress || :
%define debug_package %{nil}

Name: kernel
Summary: The Linux Kernel
Version: 4.8.12_1bP_via
Release: %mkrel 2
License: GPL
Group: System Environment/Kernel
Vendor: blackPanther Europe
Packager: Charles K. Barcza
URL: http://www.blackpantehros.eu
Source: kernel-4.8.12_1bP_via.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{PACKAGE_VERSION}-root
Provides:  kernel-4.8.12-1bP-via

%description
The Linux Kernel, the operating system core itself

%package headers
Summary: Header files for the Linux kernel for use by glibc
Group: Development/System
Obsoletes: kernel-headers
Provides: kernel-headers = %{version}
%description headers
Kernel-headers includes the C header files that specify the interface
between the Linux kernel and userspace libraries and programs.  The
header files define structures and constants that are needed for
building most standard programs and are also needed for rebuilding the
glibc package.

%package devel
Summary: Development package for building kernel modules to match the 4.8.12_1bP_via kernel
Group: System Environment/Kernel
AutoReqProv: no
%description -n kernel-devel
This package provides kernel headers and makefiles sufficient to build modules
against the 4.8.12_1bP_via kernel package.

%prep
%setup -q

%build
make clean && make %{?_smp_mflags}

%install
KBUILD_IMAGE=$(make image_name)
%ifarch ia64
mkdir -p $RPM_BUILD_ROOT/boot/efi $RPM_BUILD_ROOT/lib/modules
%else
mkdir -p $RPM_BUILD_ROOT/boot $RPM_BUILD_ROOT/lib/modules
%endif
mkdir -p $RPM_BUILD_ROOT/lib/firmware/4.8.12-1bP-via
INSTALL_MOD_PATH=$RPM_BUILD_ROOT make %{?_smp_mflags} KBUILD_SRC= mod-fw= modules_install
INSTALL_FW_PATH=$RPM_BUILD_ROOT/lib/firmware/4.8.12-1bP-via
make INSTALL_FW_PATH=$INSTALL_FW_PATH firmware_install
%ifarch ia64
cp $KBUILD_IMAGE $RPM_BUILD_ROOT/boot/efi/vmlinuz-4.8.12-1bP-via
ln -s efi/vmlinuz-4.8.12-1bP-via $RPM_BUILD_ROOT/boot/
%else
%ifarch ppc64
cp vmlinux arch/powerpc/boot
cp arch/powerpc/boot/$KBUILD_IMAGE $RPM_BUILD_ROOT/boot/vmlinuz-4.8.12-1bP-via
%else
cp $KBUILD_IMAGE $RPM_BUILD_ROOT/boot/vmlinuz-4.8.12-1bP-via
%endif
%endif
make %{?_smp_mflags} INSTALL_HDR_PATH=$RPM_BUILD_ROOT/usr KBUILD_SRC= headers_install
cp System.map $RPM_BUILD_ROOT/boot/System.map-4.8.12-1bP-via
cp .config $RPM_BUILD_ROOT/boot/config-4.8.12-1bP-via
%ifnarch ppc64
bzip2 -9 --keep vmlinux
mv vmlinux.bz2 $RPM_BUILD_ROOT/boot/vmlinux-4.8.12-1bP-via.bz2
%endif
rm -f $RPM_BUILD_ROOT/lib/modules/4.8.12-1bP-via/{build,source}
mkdir -p $RPM_BUILD_ROOT/usr/src/kernels/4.8.12-1bP-via
EXCLUDES="--exclude SCCS --exclude BitKeeper --exclude .svn --exclude CVS --exclude .pc --exclude .hg --exclude .git --exclude .tmp_versions --exclude=*vmlinux* --exclude=*.o --exclude=*.ko --exclude=*.cmd --exclude=Documentation --exclude=firmware --exclude .config.old --exclude .missing-syscalls.d"
tar $EXCLUDES -cf- . | (cd $RPM_BUILD_ROOT/usr/src/kernels/4.8.12-1bP-via;tar xvf -)
cd $RPM_BUILD_ROOT/lib/modules/4.8.12-1bP-via
ln -sf /usr/src/kernels/4.8.12-1bP-via build
ln -sf /usr/src/kernels/4.8.12-1bP-via source

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -x /sbin/installkernel -a -r /boot/vmlinuz-4.8.12-1bP-via -a -r /boot/System.map-4.8.12-1bP-via ]; then
cp /boot/vmlinuz-4.8.12-1bP-via /boot/.vmlinuz-4.8.12-1bP-via-rpm
cp /boot/System.map-4.8.12-1bP-via /boot/.System.map-4.8.12-1bP-via-rpm
rm -f /boot/vmlinuz-4.8.12-1bP-via /boot/System.map-4.8.12-1bP-via
/sbin/installkernel 4.8.12-1bP-via /boot/.vmlinuz-4.8.12-1bP-via-rpm /boot/.System.map-4.8.12-1bP-via-rpm
rm -f /boot/.vmlinuz-4.8.12-1bP-via-rpm /boot/.System.map-4.8.12-1bP-via-rpm
fi

%preun
if [ -x /sbin/new-kernel-pkg ]; then
new-kernel-pkg --remove 4.8.12-1bP-via --rminitrd --initrdfile=/boot/initramfs-4.8.12-1bP-via.img
fi

%postun
if [ -x /sbin/update-bootloader ]; then
/sbin/update-bootloader --remove 4.8.12-1bP-via
fi

%files
%defattr (-, root, root)
/lib/modules/4.8.12-1bP-via
%exclude /lib/modules/4.8.12-1bP-via/build
%exclude /lib/modules/4.8.12-1bP-via/source
/lib/firmware/4.8.12-1bP-via
/boot/*

%files headers
%defattr (-, root, root)
/usr/include

%files devel
%defattr (-, root, root)
/usr/src/kernels/4.8.12-1bP-via
/lib/modules/4.8.12-1bP-via/build
/lib/modules/4.8.12-1bP-via/source

%changelog
