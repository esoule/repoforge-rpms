#
# Please send bugfixes or comments to
# 	http://www.rtems.org/bugzilla
#

%define _prefix                 /opt/rtems-4.6ng
%define _exec_prefix            %{_prefix}
%define _bindir                 %{_exec_prefix}/bin
%define _sbindir                %{_exec_prefix}/sbin
%define _libexecdir             %{_exec_prefix}/libexec
%define _datarootdir            %{_prefix}/share
%define _datadir                %{_datarootdir}
%define _sysconfdir             %{_prefix}/etc
%define _sharedstatedir         %{_prefix}/com
%define _localstatedir          %{_prefix}/var
%define _includedir             %{_prefix}/include
%define _libdir                 %{_exec_prefix}/%{_lib}
%define _mandir                 %{_prefix}/man
%define _infodir                %{_prefix}/info
%define _localedir              %{_datarootdir}/locale

%ifos cygwin cygwin32 mingw mingw32
%define _exeext .exe
%define debug_package           %{nil}
%define _libdir                 %{_exec_prefix}/lib
%else
%define _exeext %{nil}
%endif

%ifos cygwin cygwin32
%define optflags -O3 -pipe -march=i486 -funroll-loops
%endif

%ifos mingw mingw32
%if %{defined _mingw32_cflags}
%define optflags %{_mingw32_cflags}
%else
%define optflags -O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions --param=ssp-buffer-size=4 -mms-bitfields
%endif
%endif

%if "%{_build}" != "%{_host}"
%define _host_rpmprefix %{_host}-
%else
%define _host_rpmprefix %{nil}
%endif

%define srcvers	2.59
%define rpmvers %{expand:%(echo "2.59" | tr - _ )}

%define name			rtems-4.6ng-autoconf

# --with alltests	enable all tests (default: off)
%bcond_with		alltests

# --with check          enable checks (default: off)
%bcond_with             check

Name:		%{name}
License:	GPL
URL:		http://www.gnu.org/software/autoconf
Group:		Development/Tools
Version:	%{rpmvers}
Release:	4.0.1%{?dist}
Summary:	Tool for automatically generating GNU style Makefile.in's

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch
BuildRequires: 	perl m4 gawk emacs
BuildRequires:  /bin/hostname
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Text::ParseWords)
BuildRequires:  m4 >= 1.4.5
Requires:     	m4 gawk
Requires(post):		/sbin/install-info
Requires(preun):	/sbin/install-info

Source0: ftp://ftp.gnu.org/gnu/autoconf/autoconf-%{srcvers}.tar.bz2


# rpm-4.9 filter
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Autom4te::
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(Autom4te::

# rpm-4.8 filter
%{?filter_setup:
%filter_from_provides /^perl(Autom4te::/d
%filter_from_requires /^perl(Autom4te::/d
%filter_setup
}

%description
GNU's Autoconf is a tool for configuring source code and Makefiles.
Using Autoconf, programmers can create portable and configurable
packages, since the person building the package is allowed to
specify various configuration options.
You should install Autoconf if you are developing software and you'd
like to use it to create shell scripts which will configure your
source code packages.
Note that the Autoconf package is not required for the end user who
may be configuring software with an Autoconf-generated script;
Autoconf is only required for the generation of the scripts, not
their use.

%prep
%setup -q -n autoconf-%{srcvers}
%{?PATCH0:%patch0 -p1}

%if 0%{?el5}
# Work around rpm inserting bogus perl-module deps
cat << \EOF > %{name}-prov
#!/bin/sh
%{__perl_provides} $* |\
    sed -e '/^perl(Autom4te/d'
EOF
%define __perl_provides %{_builddir}/autoconf-%{srcvers}/%{name}-prov
chmod +x %{__perl_provides}

cat << \EOF > %{name}-requ
#!/bin/sh
%{__perl_requires} $* |\
    sed -e '/^perl(Autom4te/d'
EOF
%define __perl_requires %{_builddir}/autoconf-%{srcvers}/%{name}-requ
chmod +x %{__perl_requires}
%endif

%build
./configure --prefix=%{_prefix} --infodir=%{_infodir} --mandir=%{_mandir} \
  --bindir=%{_bindir} --datadir=%{_datadir} --disable-silent-rules
make

%check
%if "%{_build}" == "%{_host}"
%if "%{srcvers}" == "2.68"
# test 199 fails sporadically
# test 205 fails deterministically
TESTSUITEFLAGS='-198 200-204 206-'
%endif
%if "%{srcvers}" == "2.69"
# test 209 fails sporadically
TESTSUITEFLAGS='-208 210-'
%endif

%if %{with check}
make check %{!?with_alltests:TESTSUITEFLAGS="${TESTSUITEFLAGS}"}
%endif
%endif

%install
rm -rf "${RPM_BUILD_ROOT}"
make DESTDIR=${RPM_BUILD_ROOT} install

# Create this directory to prevent the corresponding line
# in %%files below to fail
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/emacs/site-lisp

# RTEMS's standards.info comes from binutils
rm -f $RPM_BUILD_ROOT%{_infodir}/standards.info*

rm -f $RPM_BUILD_ROOT%{_infodir}/dir
touch $RPM_BUILD_ROOT%{_infodir}/dir

# Extract %%__os_install_post into os_install_post~
cat << \EOF > os_install_post~
%__os_install_post
EOF

# Generate customized brp-*scripts
cat os_install_post~ | while read a x y; do
case $a in
# Prevent brp-strip* from trying to handle foreign binaries
*/brp-strip*)
  b=$(basename $a)
  sed -e 's,find $RPM_BUILD_ROOT,find $RPM_BUILD_ROOT%_bindir $RPM_BUILD_ROOT%_libexecdir,' $a > $b
  chmod a+x $b
  ;;
# Fix up brp-compress to handle %%_prefix != /usr
*/brp-compress*)
  b=$(basename $a)
  sed -e 's,\./usr/,.%{_prefix}/,g' < $a > $b
  chmod a+x $b
  ;;
esac
done

sed -e 's,^\s*/usr/lib/rpm.*/brp-strip,./brp-strip,' \
  -e 's,^\s*/usr/lib/rpm.*/brp-compress,./brp-compress,' \
< os_install_post~ > os_install_post 
%define __os_install_post . ./os_install_post

%clean
  rm -rf $RPM_BUILD_ROOT

%post
/sbin/install-info  --info-dir=%{_infodir} %{_infodir}/autoconf.info.gz ||:

%preun
if [ $1 -eq 0 ]; then
  /sbin/install-info --delete --info-dir=%{_infodir} %{_infodir}/autoconf.info.gz ||:
fi   

%files
%defattr(-,root,root)
# %doc AUTHORS COPYING ChangeLog NEWS README THANKS
%dir %{_bindir}
%{_bindir}/*
%dir %{_infodir}
%ghost %{_infodir}/dir

%{_infodir}/autoconf.info*
%dir %{_mandir}
%dir %{_mandir}/man1
%{_mandir}/man1/*
%dir %{_datadir}
%{_datadir}/autoconf
%exclude %{_datadir}/emacs/site-lisp

%changelog
* Sat Jul 12 2014 Evgueni Souleimanov <esoule@100500.ca> - 2.59-4.0.1
- Build autoconf 2.59 for developing with rtems-4.6 (rtems-4.6ng)
- place manpages to /opt/rtems-4.6ng/man
- place info pages to /opt/rtems-4.6ng/info

* Tue Mar 19 2013 RTEMS Project - 2.68-4
- Original Package, as provided by RTEMS Project for RTEMS 4.10
