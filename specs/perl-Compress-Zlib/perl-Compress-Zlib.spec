# $Id$

# Authority: dag

%define rname Compress-Zlib

Summary: Compress-Zlib module for perl 
Name: perl-Compress-Zlib
Version: 1.33
Release: 0
License: distributable
Group: Applications/CPAN
URL: http://search.cpan.org/dist/Compress-Zlib/

Packager: Dag Wieers <dag@wieers.com>
Vendor: Dag Apt Repository, http://dag.wieers.com/apt/

Source: http://www.cpan.org/authors/id/P/PM/PMQS/Compress-Zlib-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root


BuildRequires: perl >= 0:5.004, zlib-devel >= 1.0.2
Requires: perl >= 0:5.004, zlib >= 1.0.2

%description
Compress-Zlib module for perl

%prep
%setup -n %{rname}-%{version} 

%build
CFLAGS="%{optflags}" %{__perl} Makefile.PL \
	PREFIX="%{buildroot}%{_prefix}" \
	INSTALLDIRS="vendor"
%{__make} %{?_smp_mflags} \
	OPTIMIZE="%{optflags}"

%install
%{__rm} -rf %{buildroot}
%makeinstall

### Clean up buildroot
%{__rm} -rf %{buildroot}%{_libdir}/perl5/*/*-linux-thread-multi/
%{__rm} -f %{buildroot}%{_libdir}/perl5/vendor_perl/*/*-linux-thread-multi/auto/*{,/*}/.packlist

%clean 
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc ANNOUNCE README
%doc %{_mandir}/man?/*
%{_libdir}/perl5/vendor_perl/*/*/*

%changelog
* Thu Mar 18 2004 Dag Wieers <dag@wieers.com> - 1.33-0
- Updated to release 1.33.

* Mon Jul 14 2003 Dag Wieers <dag@wieers.com> - 1.22-0
- Updated to release 1.22.

* Sun Jan 26 2003 Dag Wieers <dag@wieers.com>
- Initial package. (using DAR)
