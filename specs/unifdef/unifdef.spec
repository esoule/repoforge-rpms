Summary: Tool for removing ifdef'd lines
Name: unifdef
Version: 2.10
Release: 1%{?dist}
License: BSD
Group: Development/Languages
URL: http://dotat.at/prog/unifdef/
Source0: http://dotat.at/prog/unifdef/unifdef-%{version}.tar.xz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires: pkgconfig

%description
Unifdef is useful for removing ifdefed lines from a file while otherwise
leaving the file alone. Unifdef acts on #ifdef, #ifndef, #else, and #endif
lines, and it knows only enough about C and C++ to know when one of these
is inactive because it is inside a comment, or a single or double quote.

%prep
%setup -q

%build
make CFLAGS="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT
install -d -m0755 $RPM_BUILD_ROOT%{_bindir}
install -p -m0755 unifdef $RPM_BUILD_ROOT%{_bindir}/unifdef
install -p -m0755 unifdefall.sh $RPM_BUILD_ROOT%{_bindir}/unifdefall.sh

install -d -m0755 $RPM_BUILD_ROOT%{_mandir}/man1
install -p -m0644 unifdef.1 $RPM_BUILD_ROOT%{_mandir}/man1/unifdef.1

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_bindir}/unifdef
%{_bindir}/unifdefall.sh
%{_mandir}/man1/unifdef.1.gz


%changelog
* Wed Feb 26 2014 Eric Smith <spacewar@gmail.com> - 2.10-1
- Update to latest upstream.

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.9-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sun Jun 09 2013 Eric Smith <spacewar@gmail.com> - 2.9-1
- Update to latest upstream.

* Fri Feb 15 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Sun Jul 22 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Apr 30 2011 Eric Smith <eric@brouhaha.com> 2.6-1
- Update to latest upstream
- Upstream now includes their own strlcmp, so we no longer need to use
  libbsd

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.334-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Feb 11 2010 Eric Smith <eric@brouhaha.com> 1.334-1
- Remove package name from summary
- Change URL from FreeBSD CVS to project home page
- Update source to upstream 1.334
- No longer need getline() patch
- Use strlcpy from libbsd

* Fri Jan 15 2010 Kyle McMartin <kyle@redhat.com> 1.171-10
- fix unifdef ftbfs

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.171-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.171-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 18 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 1.171-7
- Autorebuild for GCC 4.3

* Wed Aug 22 2007 David Woodhouse <dwmw2@infradead.org> - 1.171-6
- Rebuild

* Sat Jul 15 2006 David Woodhouse <dwmw2@infradead.org> - 1.171-5
- Don't redefine %%dist

* Fri Jul 14 2006 Jesse Keating <jkeating@redhat.com> - 1.171-4
- Minor specfile cleanups from review

* Tue May  2 2006 David Woodhouse <dwmw2@infradead.org> - 1.171-3
- Minor specfile cleanups from review

* Wed Apr 26 2006 David Woodhouse <dwmw2@infradead.org> - 1.171-2
- Change BuildRoot

* Tue Apr 25 2006 David Woodhouse <dwmw2@infradead.org> - 1.171-1
- Initial import from FreeBSD CVS

