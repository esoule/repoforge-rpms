# $Id$

# Authority: dag

Summary: Command line NNTP file grabber.
Name: nget
Version: 0.26
Release: 0
License: GPL
Group: Applications/System
URL: http://nget.sf.net/

Packager: Dag Wieers <dag@wieers.com>
Vendor: Dag Apt Repository, http://dag.wieers.com/apt/

Source: http://dl.sf.net/nget/nget-%{version}+uulib.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root


BuildRequires: pcre-devel, popt, ncurses-devel, zlib-devel

%description
nget is a command line nntp file grabber. It automatically pieces together
multipart postings for easy retrieval, even substituting parts from multiple
servers. Handles disconnects gracefully, resuming after the last part
succesfully downloaded.

%prep
%setup

%build
%configure \
	--with-pcre \
	--with-popt
%{__make} %{?_smp_mflags}
	        
%install
%{__rm} -rf %{buildroot}
#%{__install} -d -m0755 %{buildroot}%{_bindir} \
#			%{buildroot}%{_mandir}
%makeinstall

%post
/sbin/ldconfig 2>/dev/null

%postun
/sbin/ldconfig 2>/dev/null

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc Changelog COPYING FAQ README TODO .ngetrc
%doc %{_mandir}/man?/*
%{_bindir}/*

%changelog
* Sat Mar 06 2004 Dag Wieers <dag@wieers.com> - 0.26-0
- Updated to release 0.26.

* Mon Oct 13 2003 Dag Wieers <dag@wieers.com> - 0.24.2-0
- Initial package. (using DAR)
