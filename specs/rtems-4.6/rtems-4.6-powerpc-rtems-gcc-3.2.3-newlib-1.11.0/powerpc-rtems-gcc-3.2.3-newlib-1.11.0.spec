#
# spec file for building gcc for rtems
# 
# Copyright  (c) 1999,2000,2001,2002,2003 OARCorp, Huntsville, AL
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

Vendor: 	www.rtems.com
Distribution: 	Linux

BuildRoot:	%{_defaultbuildroot}

%define gcc_version	3.2.3
%define newlib_version	1.11.0

%define gcc_target	powerpc-rtems

Name:         %{rpmprefix}%{gcc_target}-gcc-newlib
Summary:      gcc and newlib C Library for %{gcc_target}.
Group: %{rpmgroup}
Release:      4.0.6%{?dist}
License:      gcc is GPL/LGPL ; newlib no has restrictions on run-time usage

AutoReqProv:  	on
Packager:     	corsepiu@faw.uni-ulm.de and joel@OARcorp.com

Version:      	gcc%{gcc_version}newlib%{newlib_version}
%if "%{gcc_version}" >= "3.2.2"
Source0: ftp://ftp.gnu.org/pub/gnu/gcc/gcc-%{gcc_version}/gcc-%{gcc_version}.tar.bz2
%else
%if "%{gcc_version}" >= "3.0"
Source0: ftp://ftp.gnu.org/pub/gnu/gcc/gcc-%{gcc_version}/gcc-%{gcc_version}.tar.gz
%else
Source0: ftp://ftp.gnu.org/pub/gnu/gcc/gcc-%{gcc_version}/gcc-%{gcc_version}-everything.tar.gz
%endif
%endif
Source1:	ftp://sources.redhat.com/pub/newlib/newlib-%{newlib_version}.tar.gz
Patch0: gcc-3.2.3-rtems-20040420.diff
Patch1: newlib-1.11.0-rtems-20030605.diff
Patch2: gcc-3.2.3-obstack-1grow-fast-lvalue.patch
Patch3: gcc-3.2.3-current_binding_level.patch
Patch4: gcc-3.2.3-flag_jni-non-static.patch

BuildRequires:	texinfo >= 4.2
BuildRequires:	%{rpmprefix}%{gcc_target}-binutils
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
NoSource:	0
NoSource:	1
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

# Use rpm -ba --define 'gnat [0|1]' xxx.spec to override building gnat for 
# those targets wanting to support ada.

%if "%{gcc_version}" >= "3.2"
# default to building gnat
%define _gnat	%{?gnat:%gnat}%{!?gnat:1}
%else
# default to not building gnat
%define _gnat	%{?gnat:%gnat}%{!?gnat:0}
%endif

# Use rpm -ba --define 'gcj [0|1]' xxx.spec to override building gcj for 
# those targets wanting to support gcj.

%if "%{gcc_version}" >= "3.2"
# default to building gcj
%define _gcj	%{?gcj:%gcj}%{!?gcj:1}
%else
# default to not building gcj
%define _gcj	%{?gcj:%gcj}%{!?gcj:0}
%endif


%define build_cxx 	1
%define build_g77 	0
%define build_objc	0
%define build_gcj	0
%define build_gnat	0

%if "%{gcc_target}" == "arm-rtems"
%define build_gcj	%_gcj
%endif

%if "%{gcc_target}" == "c4x-rtems"
%define build_cxx	0
%endif

%if "%{gcc_target}" == "i386-rtems"
%define build_gnat      %_gnat
%define build_gcj	%_gcj
%endif

%if "%{gcc_target}" == "i960-rtems"
%define build_cxx	0
%endif

%if "%{gcc_target}" == "m68k-rtems"
%define build_gcj	%_gcj
%endif

%if "%{gcc_target}" == "mips-rtems"
%define build_gnat      %_gnat
%define build_gcj	%_gcj
%endif

%if "%{gcc_target}" == "powerpc-rtems"
# disable Ada support on powerpc-rtems, it does not build with gcc 4.4.7 on EL6
%define build_gnat      0
%define build_gcj	%_gcj
%endif

%if "%{gcc_target}" == "sparc-rtems"
%define build_gnat      %_gnat
%define build_gcj	%_gcj
%endif

%if %build_gcj
# Building gcj requires bison and zlib
BuildRequires:	bison
BuildRequires:	zlib-devel
%endif

%if %build_gnat
# Building gnat requires gnat
BuildRequires:	gcc-gnat
%endif

%description
RTEMS is an open source operating system for embedded systems.

This is gcc's and newlib C Library's sources with patches for RTEMS.

 The original sources are not included in the source RPM.
 If we included them, then the source RPMs for each target
 would duplicate MBs of source unnecessarily.  This is 
 a duplication of over 30 MBs of source for each of
 the more than 10 targets it is possible to build.

 You can get them yourself from the Internet and copy them to
 your /usr/src/[redhat|packages]/SOURCES directory ($RPM_SOURCE_DIR).
 Or you can try the ftp options of rpm :-)

%prep
# untar the sources inside %{gcc_target}-gcc-newlib
%setup -c -T -n %{name}-%{version} -a0 -a1

%patch0 -p0
%patch1 -p0
%patch2 -p1
%patch3 -p1
%patch4 -p1

  cd gcc-%{gcc_version}
    sed -e 's/\(version_string = \"[^\"]*\)/\1 (OAR Corporation gcc-%{gcc_version}-20040420\/newlib-%{newlib_version}-20030605-4)/' \
    gcc/version.c > gcc/version.c~
    mv gcc/version.c~  gcc/version.c 

  # Fix timestamps
    contrib/gcc_update --touch
  cd ..

  # Copy the C library into gcc's source tree
  ln -s ../newlib-%{newlib_version}/newlib gcc-%{gcc_version}
  test -d build || mkdir build

%build
  cd build

#  ALERT: GCJ would be better if we could add this flag and build
#  it's libraries but this code isn't ready to be embedded.
#  libgcj_flag="--enable-libgcj"

  languages="c"
%if %build_cxx
  languages="$languages,c++"
%endif
%if %build_g77
  languages="$languages,g77"
%endif
%if %build_gcj
  languages="$languages,java"
%endif
%if %build_objc
  languages="$languages,objc"
%endif
%if %build_gnat
  languages="$languages,ada"
%endif

  export PATH="%{_bindir}:${PATH}"
  ../gcc-%{gcc_version}/configure \
    --build=%_build --host=%_host \
    --target=%{gcc_target} \
    --with-gnu-as --with-gnu-ld --with-newlib --verbose \
    --with-system-zlib --disable-nls \
    --enable-version-specific-runtime-libs \
    --enable-threads=rtems --prefix=%{_prefix} \
    --enable-languages=$languages ${libgcj_flag}

%if "%_host" != "%_build"
  # Bug in gcc-3.2.1:
  # Somehow, gcc doesn't get syslimits.h right for Cdn-Xs
  test -d gcc/include || mkdir -p gcc/include
  cp ../gcc-%{gcc_version}/gcc/gsyslimits.h gcc/include/syslimits.h
%endif

  rm -f $RPM_BUILD_ROOT%{_prefix}/bin/%{gcc_target}-c++filt%{_exeext}

%if %build_gnat
  cd ../gcc-%{gcc_version}/gcc/ada
  touch treeprs.ads [es]info.h nmake.ad[bs]
  cd ../../../build
%endif
  make all
%if %build_gnat
# This gnat configuration is crap :(

# This is what is documented, but it doesn't work for me (RC)
#  make gnatlib_and_tools
  make -C gcc cross-gnattools
  make -C gcc ada.all.cross

# This should work, but doesn't.
#  make -C gcc gnatlib 

# This is what gcc/ada/Makefile.in contains by default, 
# but what we override below
  GNATLIBCFLAGS="-g -O2"
# Let gnatlib building find newlib's headers
  GNATLIBCFLAGS="$GNATLIBCFLAGS -isystem `pwd`/%{gcc_target}/newlib/targ-include"
  GNATLIBCFLAGS="$GNATLIBCFLAGS -isystem `pwd`/../newlib-%{newlib_version}/newlib/libc/include"
# Without this xgcc doesn't find the target's binutils.
  GNATLIBCFLAGS="$GNATLIBCFLAGS -B%{_prefix}/%{gcc_target}/bin/"
%if "%{gcc_target}" == "mips-rtems"
  GNATLIBCFLAGS="$GNATLIBCFLAGS -G0"
%endif
  make -C gcc GNATLIBCFLAGS="${GNATLIBCFLAGS}" gnatlib
%endif

  make info

%install
  export PATH="%{_bindir}:${PATH}"
  cd build
# Bug in gcc-2.95.1: It doesn't build this installation directory
# If it doesn't find it, gcc doesn't install %{gcc_target}/bin/gcc
%if "%{gcc_version}" < "3.0"
  ../gcc-%{gcc_version}/mkinstalldirs \
    $RPM_BUILD_ROOT%{_prefix}/%{gcc_target}/bin
%endif

  make prefix=$RPM_BUILD_ROOT%{_prefix} \
    bindir=$RPM_BUILD_ROOT%{_bindir} install
  cd %{gcc_target}/newlib
  make prefix=$RPM_BUILD_ROOT%{_prefix} \
    bindir=$RPM_BUILD_ROOT%{_bindir} install-info
  # cd back to build/
  cd ../..

%if %build_gnat
# Install a copy of gcc as gnatgcc
# Enables us to mix different versions of gnat and gnatgcc
  rm -f $RPM_BUILD_ROOT%{_bindir}/%{gcc_target}-gnatgcc%{_exeext}
  ln $RPM_BUILD_ROOT%{_bindir}/%{gcc_target}-gcc%{_exeext} \
    $RPM_BUILD_ROOT%{_bindir}/%{gcc_target}-gnatgcc%{_exeext}
%endif

  # Bug in gcc-3.x: It puts the build dirs into *.la files

  # host library
  rm -f  ${RPM_BUILD_ROOT}%{_prefix}/lib/libiberty.a

%if "%{gcc_version}" < "3.3"
  # We use the version from binutils
  rm -f $RPM_BUILD_ROOT%{_prefix}/bin/%{gcc_target}-c++filt%{_exeext}
%endif

%if "%{gcc_version}" < "3.0"
  # Bug in gcc-2.95.x: It bogusly tries to share cpp for all targets.
  # Rename it to target_alias-cpp
  if test -f $RPM_BUILD_ROOT%{_prefix}/bin/cpp%{_exeext};
  then
    mv $RPM_BUILD_ROOT%{_prefix}/bin/cpp%{_exeext} \
      $RPM_BUILD_ROOT%{_prefix}/bin/%{gcc_target}-cpp%{_exeext}
  fi
%endif

  # gzip info files
  gzip -9qf $RPM_BUILD_ROOT%{_prefix}/info/*.info 2>/dev/null
%if "%{gcc_version}" < "3.3"
  # gcc-3.3 ships monolytic *.infos
  gzip -9qf $RPM_BUILD_ROOT%{_prefix}/info/*.info-? 2>/dev/null
  gzip -9qf $RPM_BUILD_ROOT%{_prefix}/info/*.info-?? 2>/dev/null
%endif

  # gzip man files
  gzip -9qf $RPM_BUILD_ROOT%{_mandir}/man?/* 2>/dev/null

  rm -f dirs ;
  echo "%defattr(-,root,root)" >> dirs
  echo "%dir %{_prefix}/lib" >> dirs ;
  echo "%dir %{_prefix}/lib/gcc-lib" >> dirs ;
  echo "%dir %{_prefix}/lib/gcc-lib/%{gcc_target}" >> dirs ;

  # Collect multilib subdirectories
  f=`gcc/xgcc -Bgcc/ --print-multi-lib | sed -e 's,;.*$,,'`

  TGTDIR="%{_prefix}/lib/gcc-lib/%{gcc_target}/%{gcc_version}"
  for i in $f; do
    case $i in
    \.) echo "%dir ${TGTDIR}" >> dirs
      ;;
    *)  echo "%dir ${TGTDIR}/$i" >> dirs
      ;;
    esac
  done

  TGTDIR="%{_prefix}/%{gcc_target}/lib"
  for i in $f; do
    case $i in
    \.) echo "%dir ${TGTDIR}" >> dirs
      ;;
    *)  echo "%dir ${TGTDIR}/$i" >> dirs
      ;;
    esac
  done

  # Collect files to go into different packages
  cp dirs files.gcc
  cp dirs files.g77
  cp dirs files.objc
  cp dirs files.gcj
  cp dirs files.g++

  TGTDIR="%{_prefix}/lib/gcc-lib/%{gcc_target}/%{gcc_version}"
  f=`find ${RPM_BUILD_ROOT}${TGTDIR} ! -type d -print | sed -e "s,^$RPM_BUILD_ROOT,,g"`;
  for i in $f; do
    case $i in
    *lib*.la) rm ${RPM_BUILD_ROOT}/$i ;; # ignore: gcc produces bogus libtool libs
    *f771) ;;
    *cc1obj) ;;
    *libobjc*) echo "$i" >> files.objc ;;
    *include/objc*) ;;
    *include/g++*);;
    *include/c++*);;
    *adainclude*);;
    *adalib*);;
    *gnat1);;
    *jc1) ;;
    *jvgenmain) ;;
    *cc1plus) ;; # ignore: explicitly put into rpm elsewhere
    *libstdc++.a) echo "$i" >> files.g++ ;;
    *libsupc++.a) echo "$i" >> files.g++ ;;
    *) echo "$i" >> files.gcc ;;
    esac
  done

  TGTDIR="%{_prefix}/%{gcc_target}/lib"
  f=`find ${RPM_BUILD_ROOT}${TGTDIR} ! -type d -print | sed -e "s,^$RPM_BUILD_ROOT,,g"`;
  for i in $f; do
    case $i in
    *lib*.la) rm ${RPM_BUILD_ROOT}/$i;; # ignore - gcc produces bogus libtool libs
    *libiberty.a) rm ${RPM_BUILD_ROOT}/$i ;; # ignore - GPL'ed
# all other files belong to gcc
    *) echo "$i" >> files.gcc ;; 
    esac
  done

# info/dir file is not packaged
  rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
# let rpm --clean remove BuildRoot iif using the default BuildRoot
  test $RPM_BUILD_ROOT = "%{_defaultbuildroot}" && \
    rm -rf $RPM_BUILD_ROOT

# ==============================================================
# %{rpmprefix}rtems-base-gcc
# ==============================================================
%package -n %{rpmprefix}rtems-base-gcc
Summary:      	base package for rtems gcc and newlib C Library 
Group: %{rpmgroup}
Requires(pre,postun): /sbin/install-info

%description -n %{rpmprefix}rtems-base-gcc

RTEMS is an open source operating system for embedded systems.

This is the files for gcc and newlib that are shared by all targets.

%files -n %{rpmprefix}rtems-base-gcc
%defattr(-,root,root)
%dir %{_prefix}/info
%doc %{_prefix}/info/cpp.info*.gz
%doc %{_prefix}/info/cppinternals.info*.gz
%doc %{_prefix}/info/gcc.info*.gz
%doc %{_prefix}/info/libc.info*.gz
%doc %{_prefix}/info/libm.info*.gz
%doc %{_prefix}/info/gccint.info*.gz

%dir %{_prefix}/man
%dir %{_prefix}/man/man1
%doc %{_prefix}/man/man1/cpp.1*
%doc %{_prefix}/man/man1/gcov.1*
%dir %{_prefix}/man/man7
%doc %{_prefix}/man/man7/fsf-funding.7*
%doc %{_prefix}/man/man7/gfdl.7*
%doc %{_prefix}/man/man7/gpl.7*

%dir %{_prefix}/include

%post -n %{rpmprefix}rtems-base-gcc
  if test -d $RPM_INSTALL_PREFIX%{_prefix}/info; 
  then
    rm -f $RPM_INSTALL_PREFIX%{_prefix}/info/dir
    f=`find $RPM_INSTALL_PREFIX%{_prefix}/info -name '*.info.gz'`
    test -n "$f" && for i in $f; do
      install-info $i $RPM_INSTALL_PREFIX%{_prefix}/info/dir
    done
  fi

%postun -n %{rpmprefix}rtems-base-gcc
  if test -d $RPM_INSTALL_PREFIX%{_prefix}/info; 
  then
    rm -f $RPM_INSTALL_PREFIX%{_prefix}/info/dir
    f=`find $RPM_INSTALL_PREFIX%{_prefix}/info -name '*.info.gz'`
    test -n "$f" && for i in $f; do
      install-info $i $RPM_INSTALL_PREFIX%{_prefix}/info/dir
    done
  fi

# ==============================================================
# %{gcc_target}-gcc
# ==============================================================
%package -n %{rpmprefix}%{gcc_target}-gcc
Summary:      	rtems gcc and newlib C Library for %{gcc_target}
Group: %{rpmgroup}
Requires: %{rpmprefix}%{gcc_target}-binutils %{rpmprefix}rtems-base-gcc

%description -n %{rpmprefix}%{gcc_target}-gcc
RTEMS is an open source operating system for embedded systems.

This is gcc and newlib C Library for %{gcc_target}.

%files -n %{rpmprefix}%{gcc_target}-gcc -f build/files.gcc
%defattr(-,root,root)
%doc %{_prefix}/man/man1/%{gcc_target}-gcc.1*

%{_prefix}/bin/%{gcc_target}-cpp%{_exeext}
%{_prefix}/bin/%{gcc_target}-gcc%{_exeext}
%if "%{gcc_version}" >= "3.3"
%{_prefix}/bin/%{gcc_target}-gcc-%{gcc_version}%{_exeext}
%endif
%{_prefix}/bin/%{gcc_target}-gcov%{_exeext}
%{_prefix}/bin/%{gcc_target}-gccbug
%{_prefix}/%{gcc_target}/include

%dir %{_prefix}/lib/gcc-lib/%{gcc_target}/%{gcc_version}/include
%if %build_g77
# ==============================================================
# rtems-base-g77
# ==============================================================
%package -n %{rpmprefix}rtems-base-g77
Summary:      rtems base package for gcc/g77 compiler
Group: %{rpmgroup}
Requires: rtems-base-gcc
Requires(pre,postun): /sbin/install-info

%description -n %{rpmprefix}rtems-base-g77
RTEMS is an open source operating system for embedded systems.

This is the files for gcc/g77 that are shared by all targets.

%files -n %{rpmprefix}rtems-base-g77
%defattr(-,root,root)
%dir %{_prefix}/info
%doc %{_prefix}/info/g77.info*.gz

%dir %{_prefix}/man
%dir %{_prefix}/man/man1
%doc %{_prefix}/man/man1/%{gcc_target}-g77.1*

%post -n %{rpmprefix}rtems-base-g77
  if test -d $RPM_INSTALL_PREFIX%{_prefix}/info; 
  then
    rm -f $RPM_INSTALL_PREFIX%{_prefix}/info/dir
    f=`find $RPM_INSTALL_PREFIX%{_prefix}/info -name '*.info.gz'`
    test -n "$f" && for i in $f; do
      install-info $i $RPM_INSTALL_PREFIX%{_prefix}/info/dir
    done
  fi

%postun -n %{rpmprefix}rtems-base-g77
  if test -d $RPM_INSTALL_PREFIX%{_prefix}/info; 
  then
    rm -f $RPM_INSTALL_PREFIX%{_prefix}/info/dir
    f=`find $RPM_INSTALL_PREFIX%{_prefix}/info -name '*.info.gz'`
    test -n "$f" && for i in $f; do
      install-info $i $RPM_INSTALL_PREFIX%{_prefix}/info/dir
    done
  fi

%endif
%if %build_g77
# ==============================================================
# %{gcc_target}-g77
# ==============================================================
%package -n %{rpmprefix}%{gcc_target}-g77
Summary:	gcc/g77 compiler for %{gcc_target}
Group: %{rpmgroup}
Requires: %{rpmprefix}rtems-base-g77 %{rpmprefix}%{gcc_target}-gcc

%description -n %{rpmprefix}%{gcc_target}-g77
RTEMS is an open source operating system for embedded systems.

This is the gcc/g77 compiler for %{gcc_target}

%files -n %{rpmprefix}%{gcc_target}-g77 -f build/files.g77
%defattr(-,root,root)
%dir %{_prefix}/bin
%{_prefix}/bin/%{gcc_target}-g77%{_exeext}

%{_prefix}/lib/gcc-lib/%{gcc_target}/%{gcc_version}/f771%{_exeext}
%endif
%if %build_gcj
# ==============================================================
# rtems-base-gcj
# ==============================================================
%package -n %{rpmprefix}rtems-base-gcj
Summary:      base package for rtems gcc/java compiler (gcj).
Group: %{rpmgroup}
Requires: %{rpmprefix}rtems-base-gcc

%description -n %{rpmprefix}rtems-base-gcj
RTEMS is an open source operating system for embedded systems.

This is the files for gcc/java (gcj) that are shared by all targets.

%files -n %{rpmprefix}rtems-base-gcj
%defattr(-,root,root)
%dir %{_prefix}/bin
%{_prefix}/bin/jar%{_exeext}
%{_prefix}/bin/grepjar%{_exeext}

%dir %{_prefix}/info
%doc %{_prefix}/info/gcj.info*.gz

%dir %{_prefix}/man/man1
%doc %{_prefix}/man/man1/gcjh.1*
%doc %{_prefix}/man/man1/jv-scan.1*
%doc %{_prefix}/man/man1/jcf-dump.1*
%doc %{_prefix}/man/man1/gij.1*
%doc %{_prefix}/man/man1/jv-convert.1*
%doc %{_prefix}/man/man1/rmic.1*
%doc %{_prefix}/man/man1/rmiregistry.1*

%endif
%if %build_gcj
# ==============================================================
# %{gcc_target}-gcj
# ==============================================================
%package -n %{rpmprefix}%{gcc_target}-gcj
Summary:      gcc/java compiler (gcj) for %{gcc_target}
Group: %{rpmgroup}
Requires: %{rpmprefix}rtems-base-gcj %{rpmprefix}%{gcc_target}-gcc

%description -n %{rpmprefix}%{gcc_target}-gcj
RTEMS is an open source operating system for embedded systems.

This is the gcc/java compiler for %{gcc_target}

%files -n %{rpmprefix}%{gcc_target}-gcj -f build/files.gcj
%defattr(-,root,root)
%dir %{_prefix}/bin
%{_prefix}/bin/%{gcc_target}-gcj%{_exeext}
%{_prefix}/bin/%{gcc_target}-jcf-dump%{_exeext}
%{_prefix}/bin/%{gcc_target}-jv-scan%{_exeext}
%{_prefix}/bin/%{gcc_target}-gcjh%{_exeext}
%{_prefix}/man/man1/%{gcc_target}-gcj.1*

%{_prefix}/lib/gcc-lib/%{gcc_target}/%{gcc_version}/jc1%{_exeext}
%{_prefix}/lib/gcc-lib/%{gcc_target}/%{gcc_version}/jvgenmain%{_exeext}

%endif
%if %build_objc
# ==============================================================
# %{gcc_target}-objc
# ==============================================================
%package -n %{rpmprefix}%{gcc_target}-objc
Summary:      gcc/objc compiler for %{gcc_target}
Group: %{rpmgroup}
Requires: %{rpmprefix}%{gcc_target}-gcc

%description -n %{rpmprefix}%{gcc_target}-objc
RTEMS is an open source operating system for embedded systems.

This is the gcc/objc compiler for %{gcc_target}

%files -n %{rpmprefix}%{gcc_target}-objc -f build/files.objc
%defattr(-,root,root)
%{_prefix}/lib/gcc-lib/%{gcc_target}/%{gcc_version}/cc1obj%{_exeext}
%{_prefix}/lib/gcc-lib/%{gcc_target}/%{gcc_version}/include/objc
%endif
%if %build_cxx
# ==============================================================
# %{gcc_target}-c++
# ==============================================================
%package -n %{rpmprefix}%{gcc_target}-c++
Summary:      gcc/g++ compiler (c++) for %{gcc_target}
Group: %{rpmgroup}
Requires: %{rpmprefix}rtems-base-gcc %{rpmprefix}%{gcc_target}-gcc

%description -n %{rpmprefix}%{gcc_target}-c++
RTEMS is an open source operating system for embedded systems.

This is the gcc/g++ compiler for %{gcc_target}

%files -n %{rpmprefix}%{gcc_target}-c++ -f build/files.g++
%defattr(-,root,root)
%doc %{_prefix}/man/man1/%{gcc_target}-g++.1*

%dir %{_prefix}/bin
%{_prefix}/bin/%{gcc_target}-c++%{_exeext}
%{_prefix}/bin/%{gcc_target}-g++%{_exeext}

%{_prefix}/lib/gcc-lib/%{gcc_target}/%{gcc_version}/cc1plus%{_exeext}
%dir %{_prefix}/lib/gcc-lib/%{gcc_target}/%{gcc_version}/include
%if "%{gcc_version}" >= "3.2"
%{_prefix}/lib/gcc-lib/%{gcc_target}/%{gcc_version}/include/c++
%else
%{_prefix}/lib/gcc-lib/%{gcc_target}/%{gcc_version}/include/g++
%endif
%endif
%if %build_gnat
# ==============================================================
# rtems-base-gnat
# ==============================================================
%package -n %{rpmprefix}rtems-base-gnat
Summary:	gcc/gnat tools
Group: %{rpmgroup}

%description -n %{rpmprefix}rtems-base-gnat
RTEMS is an open source operating system for embedded systems.

This is the gcc/gnat tools for the gcc/gnat compiler

%files -n %{rpmprefix}rtems-base-gnat
%defattr(-,root,root)
%dir %{_prefix}/bin
# %{_prefix}/bin/gnat*
%endif
%if %build_gnat
# ==============================================================
# %{gcc_target}-gnat
# ==============================================================
%package -n %{rpmprefix}%{gcc_target}-gnat
Summary:	gcc/gnat compiler for %{gcc_target}
Group: %{rpmgroup}
Requires: %{rpmprefix}rtems-base-gnat %{rpmprefix}%{gcc_target}-gcc

%description -n %{rpmprefix}%{gcc_target}-gnat
RTEMS is an open source operating system for embedded systems.

This is the gcc/gnat compiler for %{gcc_target}

%files -n %{rpmprefix}%{gcc_target}-gnat
%defattr(-,root,root)
%dir %{_prefix}/bin
%{_prefix}/bin/%{gcc_target}-gnat*

%{_prefix}/lib/gcc-lib/%{gcc_target}/%{gcc_version}/gnat1%{_exeext}
%{_prefix}/lib/gcc-lib/%{gcc_target}/%{gcc_version}/adalib
%{_prefix}/lib/gcc-lib/%{gcc_target}/%{gcc_version}/adainclude
%endif

%changelog
* Tue Jul 1 2014 Evgueni Souleimanov <esoule@100500.ca> - gcc3.2.3newlib1.11.0-4.0.6
- Update rpm tags to match rpm 4.8.0
- gzip all man pages and info pages
- fix packaging of info files
- add patches for building with gcc 4.4.7 on EL6
- disable Ada support, it does not build with gcc 4.4.7 on EL6
- disallow build on x86_64, powerpc-rtems-ld fails to link some RTEMS tests

* Tue Apr 20 2004 RTEMS Project - gcc3.2.3newlib1.11.0-4
- Original Package, as provided by RTEMS
