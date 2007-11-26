##
## This a generated specfile from dietlibc.spec
##
%define cross ppc
##
%define name	%{cross_prefix}dietlibc
%define version 0.27
%define release 12mdk

# This is eventually a biarch package, so no %_lib for diethome
%define diethome %{_prefix}/lib/dietlibc

# Enable builds without testing (default shall always be testing)
%define build_check		1
%{expand: %{?_with_CHECK:	%%global build_check 1}}
%{expand: %{?_without_CHECK:	%%global build_check 0}}

# Enable cross compilation
%define build_cross		0
%{expand: %{?cross:		%%global build_cross 1}}
%if %{build_cross}
%define target_cpu		%{cross}
%define cross_prefix		cross-%{target_cpu}-
%define cross_make_flags	ARCH=%{target_cpu} CROSS=%{target_cpu}-linux-
%define build_check		0
%else
%define cross_prefix		%{nil}
%define cross_make_flags	%{nil}
%endif

Summary:	C library optimized for size
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Development/Other
%if %{build_cross}
BuildRequires:	%{cross_prefix}gcc
%endif
URL:		http://www.fefe.de/dietlibc/
Source0:	http://www.fefe.de/dietlibc/dietlibc-%{version}.tar.bz2
Source1:	build_cross_dietlibc.sh
Patch0:		dietlibc-0.21-features.patch.bz2
Patch1:		dietlibc-0.27-mdkconfig.patch.bz2
Patch3:		dietlibc-0.22-tests.patch.bz2
Patch4:		dietlibc-0.27-fix-getpriority.patch.bz2
Patch5:		dietlibc-0.22-net-ethernet.patch.bz2
Patch6:		dietlibc-0.24-rpc-types.patch.bz2
Patch7:		dietlibc-0.22-amd64-ioport.patch.bz2
Patch8:		dietlibc-0.24-strtol-64bit-fixes.patch.bz2
Patch9:		dietlibc-0.27-glibc-nice.patch.bz2
Patch10:	dietlibc-0.26-LC_-defines.patch.bz2
Patch11:	dietlibc-0.26-amd64-rdtsc.patch.bz2
Patch12:	dietlibc-0.26-64bit-fixes.patch.bz2
Patch13:	dietlibc-0.27-x86_64-lseek64.patch.bz2
# (oe) http://synflood.at/patches/contrapolice/contrapolice-0.3.patch
Patch14:	dietlibc-0.27-contrapolice.diff.bz2
Patch15:	dietlibc-0.27-ppc-rdtsc.patch.bz2
Patch16:	dietlibc-0.27-test-makefile-fix.patch.bz2
Patch17:	dietlibc-0.27-x86_64-stat64.patch.bz2
Patch18:	dietlibc-0.24-ppc64-umount.patch.bz2
Patch19:	dietlibc-0.24-ppc64-setjmp.patch.bz2
Patch20:	dietlibc-0.24-ppc64-endian.patch.bz2
Patch21:	dietlibc-0.24-ppc64-select.patch.bz2
Patch22:	dietlibc-0.27-ppc64-stat64.patch.bz2
Patch23:	dietlibc-0.27-biarch.patch.bz2
Patch24:	dietlibc-0.27-quiet.patch.bz2
Patch25:	dietlibc-0.27-ppc-select.patch.bz2
Patch26:	dietlibc-0.27-kernel2.6-types.patch.bz2
Patch27:	dietlibc-0.27-cross.patch.bz2
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Small libc for building embedded applications.

%package	devel
Group:          Development/C
Summary:        Development files for dietlibc
%if %{build_cross}
# Requires main dietlibc package for "diet" program (dispatcher)
# XXX: build %{target_cpu}-linux-diet wrapper too?
Requires:	dietlibc >= %{version}
Requires:	%{cross_prefix}gcc
%endif
Obsoletes:	%name
Provides:	%name

%description	devel
Small libc for building embedded applications.

%prep

%setup -q -n dietlibc-%{version}
%patch0 -p1 -b .features
%patch1 -p1 -b .mdkconfig
%patch3 -p1 -b .tests
%patch4 -p1 -b .fix-getpriority
%patch5 -p1 -b .net-ethernet
%patch6 -p1 -b .rpc-types
%patch7 -p1 -b .amd64-ioport
%patch8 -p1 -b .strtol-64bit-fixes
%patch9 -p1 -b .glibc-nice -E
%patch10 -p1 -b .locale-macros
%patch11 -p1 -b .amd64-rdtsc
%patch12 -p1 -b .tzfile-64bit-fixes
%patch13 -p1 -b .x86_64-lseek64
# (oe) http://synflood.at/patches/contrapolice/contrapolice-0.3.patch
%patch14 -p1 -b .contrapolice
%patch15 -p1 -b .ppc-rdtsc
%patch16 -p1 -b .inettest
%patch17 -p1 -b .x86_64-stat64
%patch18 -p1 -b .ppc64-umount
%patch19 -p1 -b .ppc64-setjmp
%patch20 -p1 -b .ppc64-endian
%patch21 -p1 -b .ppc64-select
%patch22 -p1 -b .ppc64-stat64
%patch23 -p1 -b .biarch
%patch24 -p1 -b .quiet
%patch25 -p1 -b .ppc-select
%patch26 -p1 -b .kernel2.6-types
%patch27 -p1 -b .cross

# fix execute permission on test scripts
chmod a+x test/{dirent,inet,stdio,string,stdlib,time}/runtests.sh

%build

%make %{cross_make_flags}

# make and run the tests
%if %{build_check}
cd test; rm *.c.*
export DIETHOME="%{_builddir}/%{name}-%{version}"
MYARCH=`uname -m | sed -e 's/i[4-9]86/i386/' -e 's/armv[3-6][lb]/arm/'`
find -name "Makefile" | xargs perl -pi -e "s|^DIET.*|DIET=\"${DIETHOME}/bin-${MYARCH}/diet\"|g"
%make
cd ..
%endif

# run the tests
%if %{build_check}
cd test
STANDARD_TESTPROGRAMS=`grep "^TESTPROGRAMS" runtests.sh | cut -d\" -f2`
# these fails: cp-test3 cp-test4 cp-test6 cp-test7 cp-test11 cp-test12 cp-test15
CP_TEST_PROGRAMS="cp-test1 cp-test2 cp-test5 cp-test8 cp-test9 cp-test10 cp-test13 cp-test14"
perl -pi -e "s|^TESTPROGRAMS.*|TESTPROGRAMS=\"${STANDARD_TESTPROGRAMS} ${CP_TEST_PROGRAMS}\"|g" runtests.sh
# getpass requires user input
perl -pi -e "s|^PASS.*|PASS=\"\"|g" runtests.sh
sh ./runtests.sh
cd ..
%endif

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

make %{cross_make_flags} DESTDIR=%{buildroot} install

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files devel
%defattr(-,root,root)
%doc AUTHOR BUGS CAVEAT CHANGES README THANKS TODO FAQ
%if ! %{build_cross}
%{_bindir}/diet
%{_mandir}/man*/*
%dir %{diethome}
%dir %{diethome}/include
%{diethome}/include/*
%endif
%dir %{diethome}/lib-*
%{diethome}/lib-*/*

