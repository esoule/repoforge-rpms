# $Id: perl-Device-SerialPorts.spec 125 2004-03-16 22:05:34Z dag $

# Authority: dag

%define rname Device-SerialPort

Summary: Device-SerialPort - Linux/POSIX emulation of Win32::SerialPort functions.
Name: perl-Device-SerialPort
Version: 1
Release: 1
License: GPL or Artistic
Group: Applications/CPAN
URL: http://search.cpan.org/dist/Device-SerialPorts/

Packager: Dag Wieers <dag@wieers.com>
Vendor: Dag Apt Repository, http://dag.wieers.com/apt/

Source: http://search.cpan.org/CPAN/authors/id/C/CO/COOK/Device-SerialPort-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root


Obsoletes: perl-Device-SerialPort
BuildRequires: perl >= 0:5.8.0
Requires: perl >= 0:5.8.0

%description
This module provides an object-based user interface essentially
identical to the one provided by the Win32::SerialPort module.

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
%doc Changes MANIFEST README TODO
### FIXME: Disabled examples
#%doc eg/
%doc %{_mandir}/man?/*
%{_bindir}/*
%{_libdir}/perl5/vendor_perl/*/*

%changelog
* Thu Mar 18 2004 Dag Wieers <dag@wieers.com> - 1-1
- Updated to release 1.

* Mon Jul 21 2003 Dag Wieers <dag@wieers.com> - 0.22-1
- Disabled examples.

* Sun Jul 20 2003 Dag Wieers <dag@wieers.com> - 0.22-0
- Initial package. (using DAR)
