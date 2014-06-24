Name:		coan
Version:	5.2
Release:	2.1%{?dist}
Summary:	A command line tool for simplifying the pre-processor conditionals in source code
Group:		Development/Languages
License:	BSD
URL:		http://coan2.sourceforge.net/
Source0:	http://downloads.sourceforge.net/coan2/%{name}-%{version}.tar.gz

# Avoid install of coan.1.gz as coan.1.1 - bug in Makefile
Patch1:         coan-man-double-gzip.patch

# Note: coan was formerly called sunifdef i.e sunifdef was renamed to coan
# with the 4.0 release. This Provides can be removed in F-16.
Provides:	sunifdef = %{version}-%{release}
Obsoletes:	sunifdef < 4.0

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  findutils

%description
%{name} (formerly sunifdef) is a software engineering tool for analyzing
pre-processor-based configurations of C or C++ source code. Its principal use
is to simplify a body of source code by eliminating any parts that are
redundant with respect to a specified configuration.

%{name} is most useful to developers of constantly evolving products
with large code bases, where pre-processor conditionals are used to
configure the feature sets, APIs or implementations of different
releases. In these environments the code base steadily
accumulates #ifdef-pollution as transient configuration options become
obsolete. %{name} can largely automate the recurrent task of purging
redundant #if-logic from the code.

%prep
%setup -q

for i in AUTHORS LICENSE.BSD README ChangeLog ; do
    sed -i -e 's/\r$//' $i
done

for i in ./Makefile.am ./man/Makefile.am ./test_coan/README ; do
    sed -i -e 's/\r$//' $i
done

find ./test_coan/test_cases \( -name '*.c' -o -name '*.c.expect' \) | xargs -n 1 sed -i -e 's/\r$//'

%patch1 -p1

%build
autoreconf -f
%configure
make %{?_smp_mflags}

%check
make check

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"

%files
%doc AUTHORS LICENSE.BSD README ChangeLog
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1.*

%changelog
* Mon Jun 23 2014 Evgueni Souleimanov <esoule@100500.ca> - 5.2-2.1
- fix double gzip of manpage coan.1.1
- convert CRLF line terminators to LF in tests, makefiles

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 24 2014 Filipe Rosset <rosset.filipe@gmail.com> - 5.2-1
- Rebuilt for new upstream version, fixes rhbz #925162, #992071 and #902927

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jan 25 2013 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 5.1.2-1
- Update to version 5.1.2

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.1-2
- Rebuilt for c++ ABI breakage

* Wed Feb  8 2012 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 5.1-1
- Update to version 5.1

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jun 12 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.1-2
- Use wild card for manpage extension to allow future compression changes
- Replace occurences of Sunifdef in package description with %%{name}
- Use INSTALL="install -p" to preserve file time stamps
- Beautify top of spec file
- No longer need to remove executable bit on source files
- Fix up spelling mistakes

* Sat Jun 12 2010 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 4.1-1
- Rename package to coan (from sunifdef)

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Mar  9 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 3.1.3-2
- Fix Source0 URL

* Wed Feb  6 2008 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 3.1.3-1
- Update to version 3.1.3

* Sun Nov 25 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 3.1.2-1
- Update to version 3.1.2
- Fix typo in changelog
- Fix line endings in AUTHORS LICENSE.BSD README ChangeLog

* Fri Aug 31 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 3.1-4
- Fix source URL
- Fix email addresses in changelog entries

* Tue Aug 28 2007 Stepan Kasal <skasal@redhat.com> - 3.1-3
- Fix typos, do not try to use '\#' to avoid interpretation of #
  as a comment; it seems the only way is to take care that it does
  not appear at the beginning of a line.

* Tue Aug 21 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 3.1-2
- Bump release and rebuild

* Mon May 21 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 3.1-1
- Update to version 3.1 (bug fix release)

* Wed Jan 24 2007 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 3.0-1
- Update to version 3.0

* Tue Jul 25 2006 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 2.1.2-1
- Update to version 2.1.2

* Tue Jul 11 2006 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 2.1.1-1
- Update to version 2.1.1

* Mon Jun  5 2006 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0.1-4
- Update to version 1.0.1
- No need to remove build-bin and autom4te.cache with this release

* Sat Jun  3 2006 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0-3
- Move make check to a check section

* Fri Jun  2 2006 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0-2
- Clean up permissions on source files
- Remove prebuilt binary directory and automa4te.cache that are included in
  tarball 
- Add make check to build
- Wrap description at 70 columns rather than 80

* Mon May 29 2006 Jonathan G. Underwood <jonathan.underwood@gmail.com> - 1.0-1
- Initial package

