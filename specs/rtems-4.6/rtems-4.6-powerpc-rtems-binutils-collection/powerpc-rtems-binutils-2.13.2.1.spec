#
# spec file for binutils package targetting powerpc-rtems
# 
# Copyright  (c)  1999,2000,2002 OARCorp, Huntsville, AL
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

Vendor: 	OARCorp
Distribution: 	Linux

BuildRoot:	%{_defaultbuildroot}

%define binutils_version     2.13.2.1
%define binutils_target      powerpc-rtems

Name:         %{rpmprefix}%{binutils_target}-binutils-collection
Summary:      binutils for target %{binutils_target}
Group:        %{rpmgroup}
Release:      2.0.4%{?dist}
License:      GPL/LGPL

Autoreqprov:  	on
Packager:     	corsepiu@faw.uni-ulm.de and joel@OARcorp.com
Prefix:		%{_prefix}
BuildRequires:	/sbin/install-info
BuildRequires:	texinfo >= 4.2

Version:      	%{binutils_version}
Source0:	ftp://ftp.gnu.org/pub/gnu/binutils/binutils-%{binutils_version}.tar.bz2


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
%if 0%{?nosrcrpm} != 0
NoSource:      0
%endif

#
# binutils builds on x86_64, but powerpc-rtems-ld fails to
# link some of the RTEMS tests, and also prints 64-bit pointer
# addresses in disassembly. Use i686 packages on x86_64 architecture
#
ExcludeArch: x86_64

## Do not generate debuginfo packages
%define debug_package %{nil}
## Do not strip any binaries
%define __strip /bin/true

%description

RTEMS is an open source operating system for embedded systems.

This is binutils sources with patches for RTEMS.

%prep
%setup -c -n %{name}-%{version}

  test -d build || mkdir build

%build
  cd build
  ../binutils-%{binutils_version}/configure \
    --build=%_build --host=%_host \
    --target=%{binutils_target} \
    --verbose --prefix=%{_prefix} --disable-nls

  make all
  make info


%install
  cd build
  make prefix=$RPM_BUILD_ROOT%{_prefix} install
  make prefix=$RPM_BUILD_ROOT%{_prefix} install-info
# A bug in binutils: binutils does not install share/locale
# however it uses it
  ../binutils-%{binutils_version}/mkinstalldirs \
    $RPM_BUILD_ROOT%{_prefix}/share/locale

#  rm -f $RPM_BUILD_ROOT%{_prefix}/bin/%{binutils_target}-c++filt%{_exeext}
# gzip info files
  gzip -9qf $RPM_BUILD_ROOT%{_prefix}/info/*.info 2>/dev/null
  gzip -9qf $RPM_BUILD_ROOT%{_prefix}/info/*.info-* 2>/dev/null

# gzip man files
  gzip -9qf $RPM_BUILD_ROOT%{_mandir}/man?/* 2>/dev/null

  if test -f $RPM_BUILD_ROOT%{_prefix}/info/configure.info.gz;
  then
# These are only present in binutils >= 2.9.5
    find $RPM_BUILD_ROOT%{_prefix}/info -name 'configure.*' | \
      sed -e "s,^$RPM_BUILD_ROOT,,g" > ../files
  else
    touch ../files
  fi

# We assume that info/dir exists when building the RPMs
  rm -f $RPM_BUILD_ROOT%{_prefix}/info/dir
  f=`find $RPM_BUILD_ROOT%{_prefix}/info -name '*.info.gz'`
  test x"$f" != x"" && for i in $f; do
    /sbin/install-info $i $RPM_BUILD_ROOT%{_prefix}/info/dir
  done

# ==============================================================
# rtems-base-binutils
# ==============================================================
%package -n %{rpmprefix}rtems-base-binutils
Summary:      base package for rtems binutils
Group: %{rpmgroup}
Requires(post,postun): /sbin/install-info

%description -n %{rpmprefix}rtems-base-binutils

RTEMS is an open source operating system for embedded systems.

This is the base for binutils regardless of target CPU.

%post -n %{rpmprefix}rtems-base-binutils
  if test -d $RPM_INSTALL_PREFIX%{_prefix}/info; 
  then
    rm -f $RPM_INSTALL_PREFIX%{_prefix}/info/dir
    f=`find $RPM_INSTALL_PREFIX%{_prefix}/info -name '*.info.gz'`
    test x"$f" != x"" && for i in $f; do
      /sbin/install-info $i $RPM_INSTALL_PREFIX%{_prefix}/info/dir
    done
  fi

%postun -n %{rpmprefix}rtems-base-binutils
  if test -d $RPM_INSTALL_PREFIX%{_prefix}/info; 
  then
    rm -f $RPM_INSTALL_PREFIX%{_prefix}/info/dir
    f=`find $RPM_INSTALL_PREFIX%{_prefix}/info -name '*.info.gz'`
    test x"$f" != x"" && for i in $f; do
      /sbin/install-info $i $RPM_INSTALL_PREFIX%{_prefix}/info/dir
    done
  fi

%files -n %{rpmprefix}rtems-base-binutils -f files
%defattr(-,root,root)
%dir %{_prefix}/info
%doc %{_prefix}/info/dir
%doc %{_prefix}/info/as.info.gz
%doc %{_prefix}/info/bfd.info.gz
%doc %{_prefix}/info/binutils.info.gz
%doc %{_prefix}/info/ld.info.gz
#### %if "%{binutils_version}" < "2.14"
%doc %{_prefix}/info/as.info-*.gz
%doc %{_prefix}/info/bfd.info-*.gz
#### %endif
# deleted as of 2.13
# %doc %{_prefix}/info/gasp.info.gz
%doc %{_prefix}/info/standards.info.gz

%dir %{_prefix}/man
%dir %{_prefix}/man/man1

# deleted as of 2.13
# %dir %{_prefix}/include
# %{_prefix}/include/bfd.h
# %{_prefix}/include/ansidecl.h
# %{_prefix}/include/bfdlink.h

%dir %{_prefix}/lib
# deleted as of 2.13
%{_prefix}/lib/libiberty*
# deleted as of 2.13
# %{_prefix}/lib/libbfd*
# %{_prefix}/lib/libopcodes*

%dir %{_prefix}/share
%dir %{_prefix}/share/locale

# ==============================================================
# %{binutils_target}-binutils
# ==============================================================
%package -n %{rpmprefix}%{binutils_target}-binutils
Summary:      rtems binutils for %{binutils_target}
Group: %{rpmgroup}
Requires: %{rpmprefix}rtems-base-binutils
Autoreqprov:  	off

%description -n %{rpmprefix}%{binutils_target}-binutils

RTEMS is an open source operating system for embedded systems.

This is the GNU binutils for RTEMS targetting %{binutils_target}.

%files -n %{rpmprefix}%{binutils_target}-binutils
%defattr(-,root,root)
%doc %{_prefix}/man/man1/%{binutils_target}-*.1*

%dir %{_prefix}/bin
%{_prefix}/bin/%{binutils_target}-addr2line%{_exeext}
%{_prefix}/bin/%{binutils_target}-ar%{_exeext}
%{_prefix}/bin/%{binutils_target}-as%{_exeext}
%{_prefix}/bin/%{binutils_target}-c++filt%{_exeext}
%if "%{binutils_version}" < "2.13"
# deleted as of 2.13
%{_prefix}/bin/%{binutils_target}-gasp%{_exeext}
%endif
%{_prefix}/bin/%{binutils_target}-ld%{_exeext}
%{_prefix}/bin/%{binutils_target}-nm%{_exeext}
%{_prefix}/bin/%{binutils_target}-objcopy%{_exeext}
%{_prefix}/bin/%{binutils_target}-objdump%{_exeext}
%{_prefix}/bin/%{binutils_target}-ranlib%{_exeext}
%{_prefix}/bin/%{binutils_target}-readelf%{_exeext}
%{_prefix}/bin/%{binutils_target}-size%{_exeext}
%{_prefix}/bin/%{binutils_target}-strings%{_exeext}
%{_prefix}/bin/%{binutils_target}-strip%{_exeext}

%dir %{_prefix}/%{binutils_target}
%dir %{_prefix}/%{binutils_target}/bin
%{_prefix}/%{binutils_target}/bin/ar%{_exeext}
%{_prefix}/%{binutils_target}/bin/as%{_exeext}
%{_prefix}/%{binutils_target}/bin/ld%{_exeext}
%{_prefix}/%{binutils_target}/bin/nm%{_exeext}
%{_prefix}/%{binutils_target}/bin/ranlib%{_exeext}
%{_prefix}/%{binutils_target}/bin/strip%{_exeext}

%dir %{_prefix}/%{binutils_target}/lib
%{_prefix}/%{binutils_target}/lib/ldscripts

%changelog
* Tue Jul 1 2014 Evgueni Souleimanov <esoule@100500.ca> - 2.13.2.1-2.0.4
- Update rpm tags to match rpm 4.8.0
- gzip all man pages and info pages
- fix packaging of info files
- disallow build on x86_64, powerpc-rtems-ld fails to link some RTEMS tests

* Wed Jan 21 2004 RTEMS Project - 2.13.2.1-2
- Original Package, as provided by RTEMS
