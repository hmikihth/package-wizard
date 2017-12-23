###
# Definitions
###
%define major	4
%define sublevel 12
%define stabrel	5
%define buildrel 1
%define codename Aviator

# Don't automatically clean up build dirs post building (sometimes useful for debugging)
%define dontclean	0

###
# Lets deal with our options and the resulting kernel 'appends' and names
###
%define bname		kernel
%define kname		%{bname}
%define kappend		bP

%define tar_vers 	%{major}.%{sublevel}.%{stabrel}
#%%define tar_vers 	%%{major}.%%{sublevel}
%define realrelease	%{kappend}%{buildrel}
%define rpmversion 	1
%define rpmrelease 	%mkrel 1

%if %stabrel
%define realversion	%{major}.%{sublevel}.%{stabrel}
%define patches_ver	%{major}.%{sublevel}.%{stabrel}-%{kappend}%{buildrel}
%else
%define realversion	%{major}.%{sublevel}
%define patches_ver	%{major}.%{sublevel}-%{kappend}%{buildrel}
%endif

%define kverrel 	%{realversion}-%{realrelease}

%define top_dir_name 	%{kname}-build
%define build_dir 	${RPM_BUILD_DIR}/%{top_dir_name}
%define src_dir 	%{build_dir}/linux-%{tar_vers}


# disable debug rpms
%define _enable_debug_packages 	%{nil}
%define debug_package 		%{nil}

###
# Our various kernel build definitions
###
%define build_source 1
%define build_doc	0
%define build_k8	0
%define build_server	0
%define build_linus	0
%define build_bfs	0
%define build_bfs_pae	0


%{?_without_source: %global build_source 0}
%{?_without_doc: %global build_doc 0}
%{?_without_server: %global build_server 0}
%{?_without_k8: %global build_k8 0}
%{?_without_linus: %global build_linus 0}
%{?_without_bfs: %global build_bfs 0}
%{?_without_bfs_pae: %global build_bfs_pae 0}

%{?_with_source: %global build_source 1}
%{?_with_doc: %global build_doc 1}
%{?_with_server: %global build_server 1}
%{?_with_k8: %global build_k8 1}
%{?_with_linus: %global build_linus 1}
%{?_with_bfs: %global build_bfs 1}
%{?_with_bfs_pae: %global build_bfs_pae 1}

# Parallelize xargs invocations on smp machines
%define kxargs xargs %([ -z "$RPM_BUILD_NCPUS" ] \\\
	&& RPM_BUILD_NCPUS="`/usr/bin/getconf _NPROCESSORS_ONLN`"; \\\
	[ "$RPM_BUILD_NCPUS" -gt 1 ] && echo "-P $RPM_BUILD_NCPUS")

	
# various defines for build options
%define preempt_full	0
%define preempt_vol	1
%define k8ops		0
%define pae_on		0
%define hz_100		0
%define hz_250		0
%define xen_guest	0

%if %(if [ -z "$CC" ] ; then echo 0; else echo 1; fi)
%define kmake %make CC="$CC"
%else
%define kmake %make 
%endif
# there are places where parallel make don't work
%define smake make

# Alias for x86_64 builds
%define target_arch	%(echo %{_arch} | sed -e "s/amd64/x86_64/")

###
# Our various kernel builds
###
#default kernel summary
%define summary The blackPanther OS kernel

# i686 server kernel
%if %build_server
%define build_source	0
%define build_doc	0
%define summary		blackPanther OS (pae enabled)
%define kname 		%{bname}
%define realrelease 	%{kappend}%{buildrel}.pae
%define pae_on		1
%endif

# linus kernel
%if %build_linus
#i686 build
%define summary	blackPanther OS (no extra patches)
%define summary	'Linus' blackPanther OS (no extra patches) for %{_arch} arch
%define kname 		kernel-linus
%define kverrel 	%{realversion}
%define hz_250		1
%endif

# AMD64 / Opteron x86 build K8 optimised kernel
%if %build_k8
%define build_source	0
%define build_doc	0
%define summary		AMD64/Opteron (K8) optimised blackPanther OS for x86 arch
%define kname 		%{bname}
%define optflags 	%__common_cflags_with_ssp -fomit-frame-pointer -march=athlon64 -fasynchronous-unwind-tables
%define realrelease 	%{kappend}%{buildrel}.a64
%define k8ops		1
%endif

# bfs kernel
%if %build_bfs
%define build_source	0
%define build_doc	0
%define summary		blackPanther OS with the BFS scheduler
%define kname 		%{bname}
%define realrelease 	%{kappend}%{buildrel}.bfs
%define preempt_vol	0
%define preempt_full	1
%endif

#arrrgh my brain!
%if %build_bfs_pae
%define build_source	1
%define build_doc	0
%define summary		blackPanther OS pae bfs scheduler
%define kname 		%{bname}
%define realrelease 	%{kappend}%{buildrel}.pae.bfs
%define preempt_vol	0
%define preempt_full	1
%define pae_on		1
%endif


###
# Generic rpm defines
###
Summary: 		%{summary}
Name: 			%{kname}-%{kverrel}
Version:		%{rpmversion}
Release:		%{rpmrelease}
License: 		GPL
Group:			System/Kernel and hardware
ExclusiveArch: 	%{ix86} x86_64
URL: 			http://www.kernel.org/

###
# Deal with our sources
###
# Do you want the src.rpm to build with no kernel source?
%define build_nosrc 0
%{?_with_nosrc: %global build_nosrc 1}
# Due to nosrc.rpm we should check for and if required download the appropriate kernel sources
%(if [ ! -f %_sourcedir/linux-%{tar_vers}.tar.xz ]; then cd %_sourcedir/ && wget http://www.kernel.org/pub/linux/kernel/v4.x/linux-%{tar_vers}.tar.xz; fi)
# This is for full SRC RPM
Source0: linux-%{tar_vers}.tar.xz
#Source1: linux-%{realversion}.tar.xz

# This is for disabling *config, mrproper, prepare, scripts on -devel rpms
Source2: 	pclos-disable-mrproper-prepare-scripts-configs-in-devel-rpms-4.11.1.patch

# This is for stripped SRC RPM
%if %build_nosrc
Nosource: 0
%endif
Source99: build-kernels.sh
Source100: linux-%{patches_ver}.tar.xz

###
# Generic rpm Requires and BuildRequires
###
BuildRoot:	%{_tmppath}/%{name}-build
Provides:	kernel = %{kverrel}, %{kname} = %{kverrel}
Provides:	alsa = 1.0.24
Provides:	should-restart = system
Requires:	module-init-tools, mkinitrd, bootloader-utils, sysfsutils, kernel-firmware, lz4
Requires:	glibc >= 2.20
BuildRequires:	gcc module-init-tools wget lz4
Requires:	%{kname}-devel = %{kverrel}
Provides:	dkms-ndiswrapper
Provides:	dkms-lzma
Provides:	dkms-squashfs-lzma
Conflicts:	dkms-crystalhd < 0-0.20100702.2
Conflicts:	dkms-psb < 4.41.1-2
Conflicts:	dkms-sn9c20x < 20100330-2
Conflicts:	dkms-rt3090 < 2.1.0.0-2
Conflicts:	dkms-r8192se < 0015.0127.2010-2
# updated for 3.4.25-pclos1
Conflicts:	dkms-virtualbox < 4.1.4
Conflicts:	dkms-vboxadditions < 4.1.1
Conflicts:	dkms-madwifi < 0.9.4-14
Conflicts:	dkms-fusion < 8.4.0-2
Conflicts:	dkms-broadcom-wl < 5_100_82_112-4
Conflicts:	dkms-fglrx < 9.012-2
Conflicts:	dkms-fglrx-current < 9.012-4
Conflicts:	dkms-nvidia-current < 310.44-2
Conflicts:	dkms-nvidia304 < 304.88-2
Conflicts:	dkms-nvidia173
Conflicts:	dkms-nvidia96xx 
Conflicts:	dkms-fglrx-legacy


%ifarch %{ix86}	
Conflicts:	arch(x86_64)
%endif

###
# Kernel rpm descriptions
###
%description
This is the default kernel for blackPanther OS.

%if %{build_server}
%description
This is the default kernel for blackPanther OS.
%endif

%if %{build_linus}
%description
This is the default kernel for blackPanther OS.
%endif

%if %{build_k8}
%description
This is the default kernel for blackPanther OS.
%endif

%if %{build_bfs}
%description
This is the default kernel for blackPanther OS.
%endif

%if %{build_bfs_pae}
%description
This is the default kernel for blackPanther OS.
%endif


###
# kernel source packages:
###
%if %build_source
%package -n	%{kname}-source-%{kverrel}
Version:	%{rpmversion}
Release:	%{rpmrelease}
Provides:	kernel-source = %{kverrel}
Requires:	glibc-devel, ncurses-devel, make, gcc, perl
Summary:	The %{kname}-%{kverrel} source code.
Group:		Development/Kernel
AutoReqProv:	no
%ifarch %{ix86}	
Conflicts:	arch(x86_64)
%endif

%description -n %{kname}-source-%{kverrel}
The kernel-source package contains the source code files for the Linux kernel.
These source files are needed to build most C programs, since
they depend on the constants defined in the source code. The source
files can also be used to build a custom kernel that is better tuned to
your particular hardware, if you are so inclined (and you know what you're
doing).
%endif

%package -n	%{kname}-devel-%{kverrel}
Version:	%{rpmversion}
Release:	%{rpmrelease}
Provides:	kernel-devel = %{kverrel}
Requires(pre):	%{kname}-%{kverrel}
Requires:	glibc-devel, ncurses-devel, make, gcc, perl
Summary:	The %{kname}-%{kverrel} kernel headers
Group:		Development/Kernel
AutoReqProv:	no
%ifarch %{ix86}	
Conflicts:	arch(x86_64)
%endif
Provides:	devel(linux-vdso(64bit))

%description -n %{kname}-devel-%{kverrel}
This package contains the kernel header files for the linux kernel.
This is a stripped down version of the full kernel-source that only holds the
kernel headers, Makefiles, KConfig files and some needed binaries. This package
should be sufficient to build most external drivers against. If you want to build 
your own kernel from source, then you need to install the main kernel-source package.



###
# kernel-doc: documentation for the Linux kernel
###
%if %build_doc
%package -n	%{kname}-doc-%{kverrel}
Version:	%{rpmversion}
Release:	%{rpmrelease}
Summary:	Various documentation found in the kernel source
Group:		Development/Kernel
AutoReqProv: no

%description -n %{kname}-doc-%{kverrel}
This package contains only documentation files from the kernel source. Various
bits of information about the Linux kernel and the device drivers shipped
with it are documented in these files. Install this package if you need a reference to
the options that can be passed to kernel modules at load time. This package is NOT
required if you have the kernel-source rpm already installed.
%endif

#
# kernel-latest: virtual rpm
#
%package -n	%{kname}-latest
%if %build_linus
Version:	%{kverrel}
%else
Version:	%{realversion}.%{realrelease}
%endif
Release:	%{rpmrelease}
Summary:	Virtual rpm for latest %{kname}
Group:		System/Kernel and hardware
Requires:	%{kname}-%{kverrel}
AutoReqProv:	no
%ifarch %{ix86}	
Conflicts:	arch(x86_64)
%endif

%description -n %{kname}-latest
This package is a virtual rpm that aims to make sure you always have the
latest kernel installed.


#
# kernel-latest-devel: virtual rpm
#
%package -n	%{kname}-devel-latest
%if %build_linus
Version:	%{kverrel}
%else
Version:	%{realversion}.%{realrelease}
%endif
Release:	%{rpmrelease}
Summary:	Virtual rpm for latest %{kname}
Group:		System/Kernel and hardware
Provides:	kernel-devel-latest = %{kverrel}
Requires:	%{kname}-devel-%{kverrel}
AutoReqProv:	no

%description -n %{kname}-devel-latest
This package is a virtual rpm that aims to make sure you always have the
latest kernel development headers installed.


###
# Apply our various patches
###
%prep
%setup -q -n %top_dir_name -c
%setup -q -n %top_dir_name -D -T -a100
cd %src_dir

%define patches_dir %{build_dir}/%{patches_ver}

# Apply stable series patches first (if any) -- Galen (moved to last patch)
#LC_ALL=C %%{patches_dir}/scripts/apply_patches --patch_dir=%%{build_dir}/%%{patches_ver}/patches-stable/

%if ! %build_linus
    # now apply the rest of them
    LC_ALL=C %{patches_dir}/scripts/apply_patches
#   LC_ALL=C %{patches_dir}/scripts/apply_patches --patch_dir=%{build_dir}/%{patches_ver}/patches-bfq/
    LC_ALL=C %{patches_dir}/scripts/apply_patches --patch_dir=%{build_dir}/%{patches_ver}/patches-aufs4/
%endif

    LC_ALL=C %{patches_dir}/scripts/apply_patches --patch_dir=%{build_dir}/%{patches_ver}/patches-fc20
    LC_ALL=C %{patches_dir}/scripts/apply_patches --patch_dir=%{build_dir}/%{patches_ver}/patches-mga
    LC_ALL=C %{patches_dir}/scripts/apply_patches --patch_dir=%{build_dir}/%{patches_ver}/patches-pclos
#    LC_ALL=C %{patches_dir}/scripts/apply_patches --patch_dir=%{build_dir}/%{patches_ver}/patches-stable
   
# get rid of unwanted files
find . -name '*~' -o -name '*.orig' -o -name '*.append' |xargs rm -f

# install the defconfig
install %{patches_dir}/configs/config-x86_64 %{src_dir}/arch/x86/configs/x86_64_defconfig
install %{patches_dir}/configs/config-x86 %{src_dir}/arch/x86/configs/i386_defconfig

%if %build_bfs_pae
install %{patches_dir}/configs/config-%{tar_vers}.pae.bfs %{src_dir}/arch/x86/configs/i386_defconfig
%endif

%if %build_bfs
install %{patches_dir}/configs/config-x86_64-%{tar_vers}.bfs %{src_dir}/arch/x86/configs/x86_64_defconfig
install %{patches_dir}/configs/config-%{tar_vers}.bfs %{src_dir}/arch/x86/configs/i386_defconfig
%endif

%if %build_server
install %{patches_dir}/configs/config-%{tar_vers}.pae %{src_dir}/arch/x86/configs/i386_defconfig
%endif

# Apply stable series patches last (if any)
LC_ALL=C %%{patches_dir}/scripts/apply_patches --patch_dir=%%{build_dir}/%%{patches_ver}/patches-stable/


###
# Kernel defconfig modifications for the various kernel builds
###

KERN_CONFIG=%{src_dir}/arch/x86/configs/%{target_arch}_defconfig

#enable kernel config function
enable_y()
{
perl -pi -e "s!# CONFIG_$1 is not set!CONFIG_$1=y!" $KERN_CONFIG
}

#disable kernel config function
disable()
{
perl -pi -e "s!CONFIG_$1=y!# CONFIG_$1 is not set!" $KERN_CONFIG
perl -pi -e "s!CONFIG_$1=m!# CONFIG_$1 is not set!" $KERN_CONFIG
}


# AMD64/Opteron x86 K8 kernel optimisation
%if %k8ops
    disable M686
    disable X86_GENERIC
    enable_y MK8
%endif

# enable voluntary preemption
%if %preempt_vol
    disable PREEMPT_NONE
    enable_y PREEMPT_VOLUNTARY
    enable_y PREEMPT_BKL
%endif

# enable full kernel preemption
%if %preempt_full
    disable PREEMPT_NONE
    enable_y PREEMPT
    enable_y PREEMPT_BKL
%endif

# enable PAE support
%if %pae_on
    disable HIGHMEM4G
    enable_y HIGHMEM64G
    enable_y X86_PAE
%endif

# enable HZ_100
%if %hz_100
    disable HZ_1000
    enable_y HZ_100
%endif

# enable HZ_250
%if %hz_250
    disable HZ_1000
    enable_y HZ_250
%endif

# enable xen guest support
%if %xen_guest
    enable_y XEN
%endif




###
# Prepare our kernel for building
###
%build

# common target directories
%define _kerneldir /usr/src/linux-%{kverrel}
%define _bootdir /boot
%define _modulesdir /lib/modules
%define _develdir /usr/src/%{kname}-devel-%{kverrel}

# directory definitions needed for building
%define temp_root %{build_dir}/temp-root
%define temp_source %{temp_root}%{_kerneldir}
%define temp_boot %{temp_root}%{_bootdir}
%define temp_modules %{temp_root}%{_modulesdir}
%define temp_devel %{temp_root}%{_develdir}

# set up our kernel name and release
cd %src_dir

%smake -s mrproper

# make sure kernel EXTRAVERSION and NAME say what we want it to say
%if ! %build_linus
#    %%if %%stabrel
#	LC_ALL=C perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = .%%{stabrel}-%%{realrelease}/" Makefile
#    %%else
	LC_ALL=C perl -p -i -e "s/^EXTRAVERSION.*/EXTRAVERSION = -%{realrelease}/" Makefile
#    %%endif
    LC_ALL=C perl -p -i -e "s/^NAME.*/NAME =%{codename}/" Makefile
%endif

# fetch our kernel .config
cp arch/x86/configs/%{target_arch}_defconfig .config
%smake oldconfig



###
# Build our kernel
###
%kmake all
# start installing stuff
install -d %{temp_boot}
install -m 644 System.map %{temp_boot}/System.map-%{kverrel}
install -m 644 .config %{temp_boot}/config-%{kverrel}
cp -f arch/%{target_arch}/boot/bzImage %{temp_boot}/vmlinuz-%{kverrel}
# modules
install -d %{temp_modules}/%{kverrel}
%smake INSTALL_MOD_PATH=%{temp_root} KERNELRELEASE=%{kverrel} modules_install 

# remove firmware blobs as we provide an external kernel-firmware rpm
rm -rf %{temp_root}/lib/firmware

# create kernel rpm file list
output=../kernel_files.%{kverrel}
echo "%defattr(-,root,root)" > $output
echo "%{_bootdir}/config-%{kverrel}" >> $output
echo "%{_bootdir}/vmlinuz-%{kverrel}" >> $output
echo "%{_bootdir}/System.map-%{kverrel}" >> $output
echo "%dir %{_modulesdir}/%{kverrel}/" >> $output
echo "%{_modulesdir}/%{kverrel}/kernel" >> $output
echo "%{_modulesdir}/%{kverrel}/modules.*" >> $output



###
# Create kernel-devel rpm tree
###

mkdir -p %{temp_devel}
for i in $(find . -name 'Makefile*'); do cp -R --parents $i %{temp_devel};done
for i in $(find . -name 'Kconfig*' -o -name 'Kbuild*'); do cp -R --parents $i %{temp_devel};done
cp -fR include %{temp_devel}
cp -fR scripts %{temp_devel}
cp -fR arch/x86/kernel/asm-offsets.{c,s} %{temp_devel}/arch/x86/kernel/
cp -fR arch/x86/kernel/asm-offsets_{32,64}.c %{temp_devel}/arch/x86/kernel/
cp -fR arch/x86/include %{temp_devel}/arch/x86/

# needed for generation of kernel/bounds.s
cp -fR kernel/bounds.c %{temp_devel}/kernel/

# needed for lguest
cp -fR drivers/lguest/lg.h %{temp_devel}/drivers/lguest/
cp -fR .config %{temp_devel}
cp -fR Module.symvers %{temp_devel}

# needed for truecrypt build
cp -fR drivers/md/dm.h %{temp_devel}/drivers/md/

# needed for external dvb tree
cp -fR drivers/media/dvb-core/*.h %{temp_devel}/drivers/media/dvb-core/
cp -fR drivers/media/dvb-frontends/*.h %{temp_devel}/drivers/media/dvb-frontends/

# needed for fglrx build (2.6.29)
cp -fR drivers/acpi/acpica/*.h %{temp_devel}/drivers/acpi/acpica/

# aufs2 has a special file needed
# restore when aufs works again
cp -fR fs/aufs/magic.mk %{temp_devel}/fs/aufs

# needed for external mac80211 builds
cp -fR drivers/base/core.c %{temp_devel}/drivers/base/

# disable mrproper in -devel rpms
patch -p1 --fuzz=0 -d %{temp_devel} -i %{SOURCE2}

# Clean the scripts tree, and make sure everything is ok (sanity check)
# running prepare+scripts (tree was already "prepared" in build)
pushd %{temp_devel} >/dev/null
%smake -s prepare scripts
%smake -s clean
popd >/dev/null
rm -f %{temp_devel}/.config.old


# clean out config split dirs
rm -f %{temp_devel}/include/config/*.{h,cmd}
find %{temp_devel}/include/config/* -type d -print | %kxargs /bin/rm -rf

# Fix permissions
chmod -R a+rX %{temp_devel}


# Prepare the kernel-sources for packaging
%if %build_source
    cd %src_dir
    %smake -s mrproper
%endif

###
# Install the beast
###
%install

cd %src_dir
# Directories definition needed for installing
%define target_source %{buildroot}/%{_kerneldir}
%define target_boot %{buildroot}%{_bootdir}
%define target_modules %{buildroot}%{_modulesdir}
%define target_devel %{buildroot}%{_develdir}




# We want to be able to test several times the install part
rm -rf %{buildroot}
cp -a %{temp_root} %{buildroot}

%if %build_source
    # create directories infastructure
    install -d %{target_source} 
    tar cf - . | tar xf - -C %{target_source}
    chmod -R a+rX %{target_source}
    # delete other misc files
    rm -f %{target_source}/{.gitattributes,.config.old,.config.cmd,.mailmap,.missing-syscalls.d,.gitignore,arch/.gitignore,firmware/.gitignore}
    cp -fR %{temp_devel}/.config %{target_source}
%endif



# we remove all the source files that we dont need
for i in arc arm arm64 cris metag mips mips64 parisc ppc64 s390 s390x score sh sh64 sparc sparc64 arm26 h8300 m68knommu v850 m32r ppc alpha ia64 m68k frv xtensa powerpc avr32 blackfin mn10300 microblaze nios2 hexagon openrisc unicore32 ; do
    rm -rf %{target_source}/arch/$i
    rm -rf %{target_devel}/arch/$i
    rm -rf %{target_source}/include/asm-$i
    rm -rf %{target_devel}/include/asm-$i

# other misc files
rm -f %{target_source}/{.missing-syscalls.d,arch/.gitignore,firmware/.gitignore,.cocciconfig}

done

# compressing modules
find %{target_modules} -name "*.ko" | %kxargs xz -6e

for i in %{target_modules}/*; do rm -f $i/build $i/source;done

# we really need the depmod -ae here to make sure
pushd %{target_modules}
for i in *; do
    /sbin/depmod -u -ae -b %{buildroot} -r -F %{target_boot}/System.map-$i $i
    echo $?
done

#create our module descriptions
for i in *; do
    pushd $i
    echo "Creating module.description for $i"
    modules=`find . -name "*.ko.[g,x]z"`
    echo $modules | %kxargs /sbin/modinfo \
    | perl -lne 'print "$name\t$1" if $name && /^description:\s*(.*)/; $name = $1 if m!^filename:\s*(.*)\.k?o!; $name =~ s!.*/!!' > modules.description
    popd
done
popd



###
# Clean up
###
%if %dontclean
%clean
%else
%clean
rm -rf %{buildroot}
rm -rf %{build_dir}
%endif


###
# Pre and post install scripts
###
%preun
/sbin/installkernel -R %{kverrel}
exit 0

%post
/sbin/installkernel %{kverrel}

%postun
/sbin/kernel_remove_initrd %{kverrel}

#clean up after oursleves
rm -rf /lib/modules/%{kverrel}
#dkms: if using dkms, get rid of old dkms kernel baggage
if [ -d /var/lib/dkms ]; then 
	%ifarch %{ix86}
	    find /var/lib/dkms -name kernel-%{kverrel}-i586 -type l -print | %kxargs /bin/rm -rf
	%else
	    find /var/lib/dkms -name kernel-%{kverrel}-x86_64 -type l -print | %kxargs /bin/rm -rf
	%endif
	find /var/lib/dkms -name %{kverrel} -type d -print | %kxargs /bin/rm -rf
fi

%if %build_source
%postun -n %{kname}-source-%{kverrel}
#clean up after oursleves
rm -rf %{_kerneldir}
exit 0
%endif


%post -n %{kname}-devel-%{kverrel}
rm -f /usr/src/linux
ln -snf %{_develdir} /usr/src/linux

# Please note: draktools is creating nasty soft links pointing to
# the incorrect kernel header dirs at kernel install time.
# We need to delete them here first, before re-creating the correct links.
for i in /lib/modules/%{kverrel}/{build,source}; do
    if [ -L $i ]; then
	rm -f $i
    fi
done

# Now re-create the correct links
ln -sf %{_develdir} /lib/modules/%{kverrel}/build
ln -sf %{_develdir} /lib/modules/%{kverrel}/source


%postun -n %{kname}-devel-%{kverrel}
if [ -L /usr/src/linux ]; then 
    if [ "$(readlink /usr/src/linux)" = "/usr/src/%{kname}-devel-%{kverrel}" ]; then
	rm -f /usr/src/linux
    fi
fi

# we need to delete <modules>/{build,source} at unsinstall
for i in /lib/modules/%{kverrel}/{build,source}; do
    if [ -L $i ]; then
	rm -f $i
    fi
done

#clean up after oursleves
rm -rf %{_develdir}
exit 0



###
# Package lists
###

# kernel
%files -f kernel_files.%{kverrel}

# full source
%if %build_source
%files -n %{kname}-source-%{kverrel}
%defattr(-,root,root)
%dir %{_kerneldir}
%dir %{_kerneldir}/arch
%dir %{_kerneldir}/include
%{_kerneldir}/.config
%{_kerneldir}/COPYING
%{_kerneldir}/CREDITS
%{_kerneldir}/Documentation
%{_kerneldir}/MAINTAINERS
%{_kerneldir}/Makefile
%{_kerneldir}/README
%{_kerneldir}/Kbuild
%{_kerneldir}/arch/x86
%{_kerneldir}/arch/um
%{_kerneldir}/arch/tile
%{_kerneldir}/block
%{_kerneldir}/crypto
%{_kerneldir}/drivers
%{_kerneldir}/firmware
%{_kerneldir}/fs
%{_kerneldir}/init
%{_kerneldir}/ipc
%{_kerneldir}/kernel
%{_kerneldir}/lib
%{_kerneldir}/mm
%{_kerneldir}/net
%{_kerneldir}/samples
%{_kerneldir}/security
%{_kerneldir}/scripts
%{_kerneldir}/sound
%{_kerneldir}/tools
%{_kerneldir}/usr
%{_kerneldir}/virt
%{_kerneldir}/Kconfig
%{_kerneldir}/arch/Kconfig
#%{_kerneldir}/include/Kbuild
%{_kerneldir}/include/acpi
%{_kerneldir}/include/asm-generic
%{_kerneldir}/include/crypto
%{_kerneldir}/include/clocksource
%{_kerneldir}/include/drm
%{_kerneldir}/include/dt-bindings
%{_kerneldir}/include/keys
%{_kerneldir}/include/linux
%{_kerneldir}/include/math-emu
%{_kerneldir}/include/memory
%{_kerneldir}/include/net
%{_kerneldir}/include/pcmcia
%{_kerneldir}/include/scsi
%{_kerneldir}/include/sound
%{_kerneldir}/include/video
%{_kerneldir}/include/media
%{_kerneldir}/include/rxrpc
%{_kerneldir}/include/rdma
%{_kerneldir}/include/trace
%{_kerneldir}/include/uapi
%{_kerneldir}/include/xen
%{_kerneldir}/include/misc
%{_kerneldir}/include/ras
%{_kerneldir}/arch/c6x/*
%{_kerneldir}/include/target
%{_kerneldir}/include/kvm
%{_kerneldir}/include/soc
%{_kerneldir}/.get_maintainer.ignore
%{_kerneldir}/certs


%endif


# kernel-devel
%files -n %{kname}-devel-%{kverrel}
%defattr(-,root,root)
%dir %{_develdir}
%dir %{_develdir}/arch
%dir %{_develdir}/include
%{_develdir}/.config
%{_develdir}/Documentation
%{_develdir}/Kbuild
%{_develdir}/Makefile
%{_develdir}/Module.symvers
%{_develdir}/arch/c6x
%{_develdir}/arch/Kconfig
%{_develdir}/arch/x86
%{_develdir}/arch/um
%{_develdir}/arch/tile
%{_develdir}/block
%{_develdir}/crypto
%{_develdir}/drivers
%{_develdir}/firmware
%{_develdir}/fs
#%{_develdir}/include/Kbuild
%{_develdir}/include/acpi
%{_develdir}/include/asm-generic
%{_develdir}/include/clocksource
%{_develdir}/include/config
%{_develdir}/include/crypto
%{_develdir}/include/drm
%{_develdir}/include/dt-bindings
%{_develdir}/include/keys
%{_develdir}/include/linux
%{_develdir}/include/math-emu
%{_develdir}/include/net
%{_develdir}/include/pcmcia
%{_develdir}/include/ras
%{_develdir}/include/rdma
%{_develdir}/include/scsi
%{_develdir}/include/sound
%{_develdir}/include/trace
%{_develdir}/include/uapi
%{_develdir}/include/video
%{_develdir}/include/media
%{_develdir}/include/memory
%{_develdir}/include/rxrpc
%{_develdir}/include/xen
%{_develdir}/include/misc
%{_develdir}/init
%{_develdir}/ipc
%{_develdir}/kernel
%{_develdir}/lib
%{_develdir}/mm
%{_develdir}/net
%{_develdir}/samples
%{_develdir}/scripts
%{_develdir}/security
%{_develdir}/sound
%{_develdir}/tools
%{_develdir}/usr
%{_develdir}/virt
%{_develdir}/include/generated
%{_develdir}/Kconfig
%{_develdir}/include/target
%{_develdir}/include/soc
%{_develdir}/include/kvm
%{_develdir}/certs

%if %build_doc
#kernel documentation
%files -n %{kname}-doc-%{kverrel}
%defattr(-,root,root)
%doc linux-%{tar_vers}/Documentation/*
%endif


%changelog
* Mon Aug 07 2017 Charles Barcza <info@blackpanther.hu>
- build for blackPanther OS v16.x
- new 12. release
- enable BFS scheduler for performance tests
------------------------------------------------------------------
* Thu Aug 03 2017 Charles Barcza <info@blackpanther.hu> 4.9.40-1bP
- build for blackPanther OS v16.2SE
- new version
------------------------------------------------------------------
* Wed Apr 19 2017 Charles Barcza <info@blackpanther.hu> 4.9.20-1bP
- build for blackPanther OS v16.x
- new version
------------------------------------------------------------------
* Sun Mar 19 2017 Charles Barcza <info@blackpanther.hu> 4.9.15-1bP
- build for blackPanther OS v16.x
- new version
------------------------------------------------------------------
* Thu Jan 26 2017 Charles Barcza <info@blackpanther.hu> 4.9.5-1bP
- build for blackPanther OS v16.x
- fixed console logo
- new version
------------------------------------------------------------------
* Sun Jan 08 2017 Charles Barcza <info@blackpanther.hu> 4.9.1-1bP
- build for blackPanther OS v16.x
--------------------------------------------------------------
* Wed Dec 07 2016 Charles Barcza <info@blackpanther.hu> 4.8.12-1bP
- build for blackPanther OS v16.x
--------------------------------------------------------------
* Sat Oct 22 2016 Charles Barcza <info@blackpanther.hu> 4.8.3-1bP
- Dirty COW (CVE 2016-5195)
- net: add recursion limit to GRO (CVE-2016-7039)
- rtlwifi: fix regression caused by 'rtlwifi: rtl818x: constify local structures'
- sched/fair: Fix incorrect task group ->load_avg
- update to 4.8.3

* Sat Jul 30 2016 Charles Barcza <info@blackpanther.hu> 4.7.0-1bP
- build for blackPanther OS v16.x
--------------------------------------------------------------

* Wed May 18 2016 Charles Barcza <info@blackpanther.hu> 4.6.0.0-1bP
- build for blackPanther OS v16.x
- stable 
------------------------------------------------------------------

* Mon May 16 2016 Charles Barcza <info@blackpanther.hu> 4.6.0.0-0.rc7.1bP
- build for blackPanther OS v16.x
------------------------------------------------------------------

* Fri Mar 11 2016 Charles Barcza <info@blackpanther.hu> 4.4.5-1bP
- new upstream
- build for blackPanther OS v16.x
--------------------------------------------------------------

* Mon Feb 22 2016 Charles Barcza <info@blackpanther.hu> 4.4.2-1bP
- build for blackPanther OS v14.x
- update to 4.4.2
  * drop merged patches
--------------------------------------------------------------

* Sun Jan 31 2016 Charles Barcza <info@blackpanther.hu> 4.4.1-1bP
- update to 4.4.1-rc1
- drm/radeon: Update radeon_get_vblank_counter_kms() (fdo#93879)
- KEYS: Fix keyring ref leak in join_session_keyring() (CVE-2016-0728)
- libata: disable forced PORTS_IMPL for >= AHCI 1.3

* Fri Aug  7 2015 Charles Barcza <info@blackpanther.hu> 4.1.4-1bP
- build for blackPanther OS v14.x
- new release 
--------------------------------------------------------------

* Thu Jul  9 2015 Charles Barcza <info@blackpanther.hu> 4.1.1-1bP
- build for blackPanther OS v14.x
- new release
--------------------------------------------------------------

* Mon Jun 29 2015 Charles Barcza <info@blackpanther.hu> 4.1.0-1bP
- build for blackPanther OS v14.x
- start new 4.x series
--------------------------------------------------------------
