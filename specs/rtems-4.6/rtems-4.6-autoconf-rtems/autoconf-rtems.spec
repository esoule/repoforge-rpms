#
# spec file for autoconf 
#

%define rpmvers 2.59
%define srcvers	2.59

%define _defaultbuildroot	%{_tmppath}/%{name}-%{srcvers}-root
%define _prefix			/opt/rtems-4.6
%define _name			autoconf

%if "%{_prefix}" != "/usr"
%define name			rtems-4.6-%{_name}-rtems
%define _infodir		%{_prefix}/info
%define _mandir			%{_prefix}/man
%else
%define name			%{_name}
%endif


Vendor:       http://www.rtems.com
Name:         %{name}
Packager:     Ralf Corsepius <ralf_corsepius@rtems.org>

License:      GPL
URL:          http://www.gnu.org/software/autoconf
Group:        RTEMS/4.6
Version:      %{rpmvers}
Release:      1.0.4%{?dist}
Summary:      Tool for automatically generating GNU style Makefile.in's
BuildArch:    noarch
BuildRoot:    %{_defaultbuildroot}
BuildRequires: perl m4 gawk emacs
Requires:     m4 gawk
Requires(post,preun):  /sbin/install-info

Source: autoconf-%{srcvers}.tar.bz2
# Patch0: autoconf-2.59-quoting-20040817-1.diff

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
%setup -q -n %{_name}-%{srcvers}
# %patch -p0 -P 0

%build
./configure --prefix=%{_prefix} --infodir=%{_infodir} --mandir=%{_mandir} \
  --bindir=%{_bindir} --datadir=%{_datadir}
make

%install
rm -rf "${RPM_BUILD_ROOT}"
make DESTDIR=${RPM_BUILD_ROOT} install

# Create this directory to prevent the corresponding line
# in %%files below to fail
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/emacs/site-lisp

# RTEMS's standards.info comes from binutils
rm -f $RPM_BUILD_ROOT%{_infodir}/standards.info*
# info/dir file is not packaged
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

gzip -9qf $RPM_BUILD_ROOT%{_infodir}/*.info* 2>/dev/null
gzip -9qf $RPM_BUILD_ROOT%{_mandir}/man?/* 2>/dev/null

%post
install-info  --info-dir=%{_infodir} %{_infodir}/autoconf.info.gz
#install-info  --info-dir=%{_infodir} %{_infodir}/standards.info.gz

%preun
if [ $1 = 0 ]; then
  install-info --delete --info-dir=%{_infodir} %{_infodir}/autoconf.info.gz
#  install-info --delete --info-dir=%{_infodir} %{_infodir}/standards.info.gz
fi   

%files
%defattr(-,root,root)
# %doc AUTHORS COPYING ChangeLog NEWS README THANKS
%{_bindir}/*
%doc %{_infodir}/autoconf.info*
#%doc %{_infodir}/standards.info*
%doc %{_mandir}/man?/*
%{_datadir}/autoconf
%exclude %{_datadir}/emacs/site-lisp

%changelog
* Tue Jul 1 2014 Evgueni Souleimanov <esoule@100500.ca> - 2.59-1.0.4
- Update rpm tags to match rpm 4.8.0
- gzip all man pages and info pages

* Wed Oct 13 2004 RTEMS Project - 2.59-0
- Original Package, as provided by RTEMS
