# $Id$

# Authority: dag

# Upstream: Christian Glodt <chris@mind.lu>
# Distcc: 0

Summary: Mozilla plugin for using bonobo components.
Name: mozilla-bonobo
Version: 0.4.0
Release: 0
License: GPL
Group: Applications/Internet
URL: http://www.nongnu.org/moz-bonobo/

Packager: Dag Wieers <dag@wieers.com>
Vendor: Dag Apt Repository, http://dag.wieers.com/apt/

Source: http://savannah.nongnu.org/download/moz-bonobo/%{name}-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root


BuildRequires: mozilla-devel >= 1.0, mozilla-nspr-devel >= 1.0
BuildRequires: gtk2-devel >= 2.0, glib2-devel >= 2.0, pango-devel >= 1.0.0
BuildRequires: atk-devel >= 1.0, freetype-devel >= 2.0
#BuildRequires: libbonoboui

%description
This package contains a plugin for the Mozilla browser that makes it
possible to use bonobo components.

%prep
%setup

%build
%configure \
	--with-plugin-install-dir="%{buildroot}%{_libdir}/mozilla/plugins" \
	--disable-schemas-install
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__install} -d -m0755 %{buildroot}%{_libdir}/mozilla/plugins/
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL="1"
%makeinstall

### Clean up buildroot
%{__rm} -rf %{buildroot}%{_prefix}/doc/

%post
export GCONF_CONFIG_SOURCE="$(gconftool-2 --get-default-source)"
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/%{name}.schemas &>/dev/null
scrollkeeper-update -q

%postun
scrollkeeper-update -q

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING README NEWS TODO
%config %{_sysconfdir}/gconf/schemas/*.schemas
%{_bindir}/*
%{_libdir}/mozilla/plugins/*.so

%changelog
* Fri Oct 03 2003 Dag Wieers <dag@wieers.com> - 0.4.0-0
- Updated to release 0.4.0.

* Wed Jul 23 2003 Dag Wieers <dag@wieers.com> - 0.3.0-1
- Build against mozilla release 1.4.

* Tue May 20 2003 Dag Wieers <dag@wieers.com> - 0.3.0-0
- Updated to release 0.3.0.

* Fri May 09 2003 Dag Wieers <dag@wieers.com> - 0.2.0-0
- Updated to release 0.2.0.

* Thu May 08 2003 Dag Wieers <dag@wieers.com> - 0.1.0-0
- Initial package. (using DAR)
