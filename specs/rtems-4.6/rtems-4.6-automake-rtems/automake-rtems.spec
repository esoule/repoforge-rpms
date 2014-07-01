#
# spec file for automake 
#

%define rpmvers 1.7.2
%define srcvers	1.7.2
%define amvers  1.7

%define _defaultbuildroot	%{_tmppath}/%{name}-%{srcvers}-root
%define _prefix			/opt/rtems-4.6
%define _name			automake

%if "%{_prefix}" != "/usr"
%define name			rtems-4.6-%{_name}-rtems
%define requirements		rtems-4.6-autoconf-rtems >= 2.54
%define _infodir		%{_prefix}/info
%define _mandir			%{_prefix}/man
%else
%define name			%{_name}
%define requirements		autoconf >= 2.54
%endif

Vendor:       http://www.rtems.com
Name:         %{name}
Packager:     Ralf Corsepius <corsepiu@faw.uni-ulm.de>
URL:          http://sources.redhat.com/automake

License:      GPL
Group:        RTEMS/4.6
Autoreqprov:  on
Version:      %{rpmvers}
Release:      2.0.3%{?dist}
Summary:      Tool for automatically generating GNU style Makefile.in's
BuildArch:    noarch
BuildRoot:    %{_defaultbuildroot}
BuildRequires: %{requirements} perl help2man
Requires:     %{requirements}
Requires(post,preun): /sbin/install-info

Source: ftp://ftp.gnu.org/gnu/automake/automake-%{srcvers}.tar.bz2

%description
Automake is a tool for automatically generating "Makefile.in"s from
files called "Makefile.am". "Makefile.am" is basically a series of
"make" macro definitions (with rules being thrown in occasionally).
The generated "Makefile.in"s are compatible to the GNU Makefile
standards.

%prep
%setup -q -n %{_name}-%{srcvers}

%build
PATH=%{_prefix}/bin:$PATH
./configure --prefix=%{_prefix} --infodir=%{_infodir} --mandir=%{_mandir}
make

%install
%makeinstall

install -m 755 -d $RPM_BUILD_ROOT/%{_mandir}/man1
for i in $RPM_BUILD_ROOT%{_bindir}/aclocal \
  $RPM_BUILD_ROOT%{_bindir}/automake ; 
do
  perllibdir=$RPM_BUILD_ROOT/%{_datadir}/automake-%{amvers} \
  help2man $i > `basename $i`.1
  install -m 644 `basename $i`.1 $RPM_BUILD_ROOT/%{_mandir}/man1
done

# info/dir file is not packaged
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

gzip -9qf $RPM_BUILD_ROOT%{_infodir}/*.info* 2>/dev/null
gzip -9qf $RPM_BUILD_ROOT%{_mandir}/man?/* 2>/dev/null

%post 
install-info  --info-dir=%{_infodir} %{_infodir}/automake.info.gz

%preun
if [ $1 = 0 ]; then
  install-info --delete --info-dir=%{_infodir} %{_infodir}/automake.info.gz
fi

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README THANKS
%{_bindir}/aclocal*
%{_bindir}/automake*
%doc %{_infodir}/automake.info*.gz
%doc %{_mandir}/man?/*
%{_datadir}/aclocal-%{amvers}
%{_datadir}/automake-%{amvers}

%changelog
* Tue Jul 1 2014 Evgueni Souleimanov <esoule@100500.ca> - 1.7.2-2.0.3
- Update rpm tags to match rpm 4.8.0
- gzip all man pages and info pages

* Wed Jan 21 2004 RTEMS Project - 1.7.2-2
- Original Package, as provided by RTEMS
