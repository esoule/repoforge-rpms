#
# spec file for building gdb for rtems
# 
# Copyright  (c)  1999  OARCorp, Huntsville, AL
#
# Please send bugfixes or comments to
# 	http://www.rtems.com/cgi-bin/gnatweb.pl
# or	mailto:rtems-bugs@rtems.com
#

%define	_prefix			/opt/rtems-4.6
%if "%{_prefix}" != "/usr"
%define _infodir		%{_prefix}/info
%define _mandir			%{_prefix}/man
%endif

%define rpmprefix		rtems-4.6-
%define rpmgroup		RTEMS/4.6

%define _defaultbuildroot 	%{_tmppath}/%{name}-%{version}-root
%ifos cygwin cygwin32
%define _exeext .exe
%else
%define _exeext %{nil}
%endif

# Work around to a bug in rpm-4.2
%define __os_install_post	%{nil}

Vendor: 	OARCorp
Distribution: 	Linux

BuildRoot:	%{_defaultbuildroot}

%define gdb_version	5.2
%define gdb_target	powerpc-rtems

Name:         %{rpmprefix}%{gdb_target}-gdb-collection
Release:      1
License:      GPL/LGPL
Group:        %{rpmgroup}

Autoreqprov:  on
Packager:     corsepiu@faw.uni-ulm.de and joel@OARcorp.com

Version:      %{gdb_version}
Summary:      gdb for target %{gdb_version}
Source0:      ftp://ftp.gnu.org/pub/gnu/gdb-%{gdb_version}.tar.gz
Patch0:	      gdb-%{gdb_version}-rtems-base-20030211.diff
Patch1:	      gdb-%{gdb_version}-rtems-cg-20030211.diff
Patch2:	      gdb-%{gdb_version}-rtems-rdbg-20030211.diff

%if "%{_vendor}" == "redhat"
BuildPreReq:	ncurses-devel
%endif

#
# The original sources are not included in the source RPM.
# If we included them, then the source RPMs for each target
# would duplicate MBs of source unnecessarily.  This is 
# a duplication of over 30 MBs of source for each of
# the more than 10 targets it is possible to build.
#
# You can get them yourself from the Internet and copy them to
# your /usr/src/redhat/SOURCES directory ($RPM_SOURCE_DIR).
# Or you can try the ftp options of rpm :-)
#
NoSource:      0

#  Account as best possible for targets without simulators
#  and targets which require extra arguments.
%define _sim	1

%if "%{gdb_target}" == "m68k-rtems"
%define _sim	0
%endif
%if "%{gdb_target}" == "i386-rtems"
%define _sim	0
%endif


%description
RTEMS is an open source operating system for embedded systems.

This is the GNU gdb for RTEMS targetting %{gdb_version}.

%prep
%setup -c -n %{name}-%{version} -a 0

cd gdb-%{gdb_version}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%if "%_sim" == "1"
 simargs="--enable-sim"
%endif

%if "%{gdb_target}" == "powerpc-rtems"
 simargs="$simargs --enable-sim-timebase --enable-sim-hardware"
 #  Enabling this causes the program image to be huge and causes
 #  some gcc/hosts combinations to run out of memory.
 # simargs="$simargs --enable-sim-inline"
%endif

test -d build || mkdir build
  cd build
  export PATH="%{_bindir}:${PATH}"
  ../gdb-%{gdb_version}/configure \
    --build=%_build --host=%_host \
    --target=%{gdb_target} \
    --verbose --prefix=%{_prefix} $simargs \
    --disable-nls

  make all
  make info

%install
  cd build
  make prefix=$RPM_BUILD_ROOT%{_prefix} install
  make prefix=$RPM_BUILD_ROOT%{_prefix} install-info

  # host files
  rm -rf $RPM_BUILD_ROOT%{_prefix}/include/*.h
  rm -rf $RPM_BUILD_ROOT%{_prefix}/lib/lib*a

  # These come from other packages
  rm -rf $RPM_BUILD_ROOT%{_prefix}/info/bfd*
  rm -rf $RPM_BUILD_ROOT%{_prefix}/info/configure*
  rm -rf $RPM_BUILD_ROOT%{_prefix}/info/standards*
 
  # gzip info files
  gzip -f $RPM_BUILD_ROOT%{_prefix}/info/*.info 2>/dev/null
  gzip -f $RPM_BUILD_ROOT%{_prefix}/info/*.info-? 2>/dev/null
  gzip -f $RPM_BUILD_ROOT%{_prefix}/info/*.info-?? 2>/dev/null
%clean
# let rpm --clean remove BuildRoot iif using the default BuildRoot
  test $RPM_BUILD_ROOT = "%{_defaultbuildroot}" && \
    rm -rf $RPM_BUILD_ROOT

# =====================================================================
# rtems-base-gdb
# =====================================================================

%package -n %{rpmprefix}rtems-base-gdb
Summary:      base package for rtems gdb
Group: %{rpmgroup}

%description -n %{rpmprefix}rtems-base-gdb

RTEMS is an open source operating system for embedded systems.

This is the base for gdb regardless of target CPU.

%files -n %{rpmprefix}rtems-base-gdb
%defattr(-,root,root)

%dir %{_prefix}/info
%doc %{_prefix}/info/gdb.info*
%doc %{_prefix}/info/mmalloc.info*
# FIXME: When had gdbint and stabs been introduced?
%if "%{gdb_version}" >= "5.0"
%doc %{_prefix}/info/gdbint.info*
%doc %{_prefix}/info/stabs.info*
%endif
# gdb 4.18 installed this, gdb 5.0 does not
%if "%{gdb_version}" < "5.0"
%doc %{_prefix}/info/readline.info*
%endif

%dir %{_prefix}/man
%dir %{_prefix}/man/man1

%dir %{_prefix}/include
# We install libbfd from binutils
# %{_prefix}/include/bfd.h
# %{_prefix}/include/bfdlink.h

%dir %{_prefix}/lib
# We install libbfd from binutils
# %{_prefix}/lib/libbfd*
# We use libiberty from gcc
# %{_prefix}/lib/libiberty*

%post -n %{rpmprefix}rtems-base-gdb
  if test -d $RPM_INSTALL_PREFIX/rtems/info;
  then
    rm -f $RPM_INSTALL_PREFIX/rtems/info/dir
    f=`find $RPM_INSTALL_PREFIX/rtems/info -name '*.info.gz'`
    test -n "$f" && for i in $f; do
      install-info $i $RPM_INSTALL_PREFIX/rtems/info/dir
    done
  fi

%postun -n %{rpmprefix}rtems-base-gdb
  if test -d $RPM_INSTALL_PREFIX/rtems/info;
  then
    rm -f $RPM_INSTALL_PREFIX/rtems/info/dir
    f=`find $RPM_INSTALL_PREFIX/rtems/info -name '*.info.gz'`
    test -n "$f" && for i in $f; do
      install-info $i $RPM_INSTALL_PREFIX/rtems/info/dir
    done
  fi
# =====================================================================
# %{gdb_target}-gdb
# =====================================================================

%package -n %{rpmprefix}%{gdb_target}-gdb
Summary:      rtems gdb for %{gdb_target}
Group: %{rpmgroup}
Requires: %{rpmprefix}rtems-base-gdb

%description -n %{rpmprefix}%{gdb_target}-gdb

RTEMS is an open source operating system for embedded systems.

This is the GNU gdb for RTEMS targetting %{gdb_target}.

%files -n %{rpmprefix}%{gdb_target}-gdb
%defattr(-,root,root)
%doc %{_prefix}/man/man1/%{gdb_target}-gdb.1*
%if "%_sim" == "1"
%doc %{_prefix}/man/man1/%{gdb_target}-run.1*
%endif

%dir %{_prefix}/bin
%{_prefix}/bin/%{gdb_target}-gdb%{_exeext}
%if "%_sim" == "1"
%{_prefix}/bin/%{gdb_target}-run%{_exeext}
%endif
%if "%{gdb_target}" == "sparc-rtems"
%{_prefix}/bin/%{gdb_target}-sis%{_exeext}
%endif

%changelog
* Fri Sep 5 2003 RTEMS Project - 5.2-1
- Original Package, as provided by RTEMS
