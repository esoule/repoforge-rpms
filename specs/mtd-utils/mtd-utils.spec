Summary: Utilities for dealing with MTD (flash) devices
Name: mtd-utils
Version: 1.2.0
Release: 3%{?dist}
License: GPLv2+
Group: Applications/System
URL: http://www.linux-mtd.infradead.org/
Source0: ftp://ftp.infradead.org/pub/mtd-utils/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: zlib-devel libacl-devel lzo-devel

%description
The mtd-utils package contains utilities related to handling MTD devices,
and for dealing with FTL, NFTL JFFS2 etc.

%package ubi
Summary: Utilities for dealing with UBI
Group: Applications/System

%description ubi
The mtd-utils-ubi package contains utilities for manipulating UBI on 
MTD (flash) devices.

%prep
%setup -q

%build
CFLAGS="$RPM_OPT_FLAGS" make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT SBINDIR=%{_sbindir} MANDIR=%{_mandir} install
make DESTDIR=$RPM_BUILD_ROOT SBINDIR=%{_sbindir} MANDIR=%{_mandir} install -C ubi-utils

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_sbindir}/bin2nand
%{_sbindir}/doc*
%{_sbindir}/flash*
%{_sbindir}/ftl*
%{_sbindir}/jffs2dump
%{_sbindir}/mkbootenv
%{_sbindir}/mkfs.jffs2
%{_sbindir}/mtd_debug
%{_sbindir}/nand*
%{_sbindir}/nftl*
%{_sbindir}/recv_image
%{_sbindir}/rfd*
%{_sbindir}/serve_image
%{_sbindir}/sumtool
%{_mandir}/*/*
%doc COPYING device_table.txt


%files ubi
%{_sbindir}/mkpfi
%{_sbindir}/pddcustomize
%{_sbindir}/pfi*
%{_sbindir}/unubi
%{_sbindir}/ubi*

%changelog
* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Jul 02 2008 David Woodhouse <david.woodhouse@intel.com> - 1.2.0-1
- Update to 1.2.0

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.1.0-3
- Autorebuild for GCC 4.3

* Tue Aug 28 2007 David Woodhouse <dwmw2@infradead.org> - 1.1.0-2
- Build ubi-utils

* Wed Aug 22 2007 David Woodhouse <dwmw2@infradead.org> - 1.1.0-1
- Update to 1.1.0 + nandtest + multicast utils

* Thu Oct 05 2006 Christian Iseli <Christian.Iseli@licr.org> - 1.0.1-2
- rebuilt for unwind info generation, broken in gcc-4.1.1-21

* Mon Sep 18 2006 David Woodhouse <dwmw2@infradead.org> - 1.0.1-1
- Update to 1.0.1

* Tue May  2 2006 David Woodhouse <dwmw2@infradead.org> - 1.0.0-2
- Fixes from review (include COPYING), BR zlib-devel
- Include device_table.txt

* Sun Apr 30 2006 David Woodhouse <dwmw2@infradead.org> - 1.0.0-1
- Initial build.

