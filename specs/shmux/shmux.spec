# $Id$

# Authority: dag

# Upstream: Christophe Kalt <shmux@taranis.org>

%define rversion 0.11a

Summary: Program for executing the same command on many hosts in parallel.
Name: shmux
Version: 0.11
Release: 0.a
License: Proprietary License with Source
Group: System Environment/Shells
URL: http://web.taranis.org/shmux/

Packager: Dag Wieers <dag@wieers.com>
Vendor: Dag Apt Repository, http://dag.wieers.com/apt/

Source: http://web.taranis.org/shmux/dist/%{name}-%{rversion}.tgz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root


Requires: fping

%description
shmux is program for executing the same command on many hosts in parallel.
For each target, a child process is spawned by shmux, and a shell on the
target obtained one of the supported methods: rsh, ssh, or sh. The output
produced by the children is received by shmux and either output in turn to
the user, or written to files for later processing.

%prep
%setup -n %{name}-%{rversion}

%build
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%makeinstall \
	sharedir="%{buildroot}%{_datadir}/shmux"

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc CHANGES INSTALL LICENSE mcmd.sh
%doc %{_mandir}/man?/*
%{_bindir}/*
%{_datadir}/shmux/

%changelog
* Mon Dec 31 2003 Dag Wieers <dag@wieers.com> - 0.11-0.a
- Updated to release 0.11a.

* Mon Jun 23 2003 Dag Wieers <dag@wieers.com> - 0.10-0.a
- Updated to release 0.10a.

* Mon May 05 2003 Dag Wieers <dag@wieers.com> - 0.9-0.a
- Updated to release 0.9a.

* Fri May 02 2003 Dag Wieers <dag@wieers.com> - 0.8-0
- Updated to release 0.8a.

* Tue Apr 29 2003 Dag Wieers <dag@wieers.com> - 0.7-0
- Updated to release 0.7a. (using DAR)

* Wed Aug 14 2002 Dag Wieers <dag@wieers.com> - 0.3-0
- Initial package.
