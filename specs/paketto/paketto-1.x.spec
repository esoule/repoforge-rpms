# $Id$

# Authority: dag

Summary: Unusual TCP/IP testing tools.
Name: paketto
Version: 1.10
Release: 0
License: GPL
Group: Applications/Network
URL: http://www.doxpara.com/

Packager: Dag Wieers <dag@wieers.com>
Vendor: Dag Apt Repository, http://dag.wieers.com/apt/

Source: http://www.doxpara.com/paketto-%{version}.tar.gz
Patch0: paketto-1.10-gcc33.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root


BuildRequires: libpcap, bison, flex

%description
The Paketto Keiretsu is a collection of tools that use new and unusual
strategies for manipulating TCP/IP networks.

This package includes:

	scanrand (very fast port, host, and network trace scanner),
	minewt (user space NAT/MAT gateway)
	linkcat(lc) (provides direct access to the network level 2)
	paratrace (traceroute-like tool using existing TCP connections)
and	phentropy (plots a large data source onto a 3D matrix)

%prep
%setup
%configure
%patch0

%build
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%makeinstall

### Clean up docs
%{__rm} -rf docs/CVS/

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING INSTALL NEWS README TODO docs/
%doc %{_mandir}/man?/*
%{_bindir}/*
%{_sbindir}/*
%{_includedir}/*.h

%changelog
* Wed Feb 18 2004 Dag Wieers <dag@wieers.com> - 1.10-0
- Initial package. (using DAR)
