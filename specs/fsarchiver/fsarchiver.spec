
%{?el5:%define _without_lzo 1}
%{?_without_lzo:%define _disable_lzo_flag --disable-lzo}

Name:		fsarchiver
Version:	0.6.17
Release:	2%{?dist}
Summary:	Safe and flexible file-system backup/deployment tool

Group:		Applications/Archiving
License:	GPLv2
URL:		http://www.fsarchiver.org
Source0:  	http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.gz      
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if 0%{?el6}
BuildRequires:	e2fsprogs-devel => 1.41.4
BuildRequires:	libuuid-devel
BuildRequires:	libblkid-devel
%endif
%if 0%{?el5}
BuildRequires:	e2fsprogs-devel
%endif
BuildRequires:	e2fsprogs
BuildRequires:	libattr-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	zlib-devel
BuildRequires:	bzip2-devel
%{!?_without_lzo:BuildRequires: lzo-devel}
BuildRequires:	xz-devel

%description
FSArchiver is a system tool that allows you to save the contents of a 
file-system to a compressed archive file. The file-system can be restored 
on a partition which has a different size and it can be restored on a 
different file-system. Unlike tar/dar, FSArchiver also creates the 
file-system when it extracts the data to partitions. Everything is 
checksummed in the archive in order to protect the data. If the archive 
is corrupt, you just lose the current file, not the whole archive.

%prep
%setup -q

%build
%configure %{?_disable_lzo_flag}
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_sbindir}/%{name}
%{_mandir}/man8/%{name}*
%doc COPYING README THANKS NEWS

%changelog
* Wed May 8 2013 Evgueni Souleimanov <esoule@100500.ca> - 0.6.17-2
- build on el5 without lzo
- libuuid and libblkid are part of e2fsprogs on el5

* Wed May 8 2013 Evgueni Souleimanov <esoule@100500.ca> - 0.6.17-1
- import initial release from upstream

