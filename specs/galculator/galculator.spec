# $Id$

# Authority: dag
# Upstream: Simon Floery <simon.floery@gmx.at>

Summary: Graphical scientific calculator.
Name: galculator
Version: 1.2.1
Release: 1
License: GPL
Group: Applications/Engineering
URL: http://galculator.sf.net/

Packager: Dag Wieers <dag@wieers.com>
Vendor: Dag Apt Repository, http://dag.wieers.com/apt/

Source: http://dl.sf.net/galculator/galculator-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root


BuildRequires: gettext, gtk2-devel >= 2.0, libglade2-devel >= 2.0

%description
galculator is a scientific calculator. It supports different number
bases (DEC/HEX/OCT/BIN) and angle units (DEG/RAD/GRAD) and features
a wide range of mathematical (basic arithmetic operations,
trigonometric functions, etc) and other useful functions (memory, etc)
at the moment. galculator can be used in algebraic mode as well as in
Reverse Polish Notation.

%prep
%setup

%build
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%makeinstall
%find_lang %{name}

%clean
%{__rm} -rf %{buildroot}

%files -f %{name}.lang
%defattr(-, root, root, 0755)
%doc AUTHORS ChangeLog COPYING NEWS README THANKS TODO doc/shortcuts
%doc %{_mandir}/man?/*
%{_bindir}/*
%{_datadir}/applications/*.desktop
%{_datadir}/galculator/

%changelog
* Sun Mar 21 2004 Dag Wieers <dag@wieers.com> - 1.2.1-1
- Updated to release 1.2.1.

* Thu Mar 11 2004 Dag Wieers <dag@wieers.com> - 1.2.0-1
- Updated to release 1.2.0.

* Mon Nov 17 2003 Dag Wieers <dag@wieers.com> - 1.1.4-0
- Updated to release 1.1.4.

* Sun Aug 31 2003 Dag Wieers <dag@wieers.com> - 1.1.3-0
- Updated to release 1.1.3.

* Mon Jul 07 2003 Dag Wieers <dag@wieers.com> - 1.1.2-0
- Updated to release 1.1.2.

* Tue Jun 24 2003 Dag Wieers <dag@wieers.com> - 1.1.1-0
- Updated to release 1.1.1.

* Sun Jun 22 2003 Dag Wieers <dag@wieers.com> - 1.1.0-0
- Updated to release 1.1.0.

* Tue Apr 24 2003 Dag Wieers <dag@wieers.com> - 1.0-0
- Updated to release 1.0.

* Sat Mar 29 2003 Dag Wieers <dag@wieers.com> - 0.9.91-0
- Initial package. (using DAR)
