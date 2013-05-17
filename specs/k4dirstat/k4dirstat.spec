%define preversion 20130311git33ed79e

Name:           k4dirstat
Version:        2.7.4
Release:        0.12.%{preversion}%{?dist}
Summary:        Graphical Directory Statistics for Used Disk Space

Group:          Applications/System
License:        GPLv2 and LGPLv2
URL:            http://bitbucket.org/jeromerobert/k4dirstat

Source0:        %{name}-%{version}.tar.bz2
#script to get snapshot of k4dirstat
Source1:        k4dirstat-snapshot.sh

Patch100:       k4dirstat-2.7.4-desktop.patch

BuildRequires:  kdebase4-devel

Obsoletes: kdirstat < %{version}-%{release}
Provides: kdirstat = %{version}-%{release}

%{?_kde4_macros_api:Requires: kde4-macros(api) = %{_kde4_macros_api} }

%description
KDirStat (KDE Directory Statistics) is a utility program that sums up
disk usage for directory trees - very much like the Unix 'du' command.
It can also help you clean up used space.

K4DirStat is the port to KDE4.

This is Jerome Robert's fork of Joshua Hodosh kdirstat KDE4 port
(http://grumpypenguin.org).

%prep
%setup -q
%patch100 -p1 -b .desktop-file

%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

cd %{buildroot}%{_kde4_bindir}
ln -s k4dirstat kdirstat

%check
desktop-file-validate \
  %{buildroot}/%{_datadir}/applications/kde4/k4dirstat.desktop

%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:


%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
update-desktop-database -q &> /dev/null ||:


%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:
  gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
  update-desktop-database -q &> /dev/null ||:
fi

%files
%defattr(-,root,root,-)
%doc AUTHORS  COPYING  COPYING.LIB  CREDITS  TODO
%{_kde4_bindir}/k4dirstat
%{_kde4_bindir}/kdirstat
%{_kde4_datadir}/applications/kde4/k4dirstat.desktop
%{_kde4_datadir}/config.kcfg/k4dirstat.kcfg
%{_kde4_docdir}/HTML/en/k4dirstat/
%{_kde4_iconsdir}/hicolor/*/apps/k4dirstat.png
%{_kde4_iconsdir}/hicolor/*/apps/k4dirstat.svgz
%{_kde4_appsdir}/k4dirstat


%changelog
* Thu May 16 2013 Evgueni Souleimanov <esoule@100500.ca> - 2.7.4-0.12.20130311git33ed79e
- Update to version 2.7.4 git 33ed79e from Jerome Robert's fork
  at http://bitbucket.org/jeromerobert/k4dirstat
- Fix desktop file, so that it passes desktop-file-validate

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.0-0.9.20101010git6c0a9e6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.0-0.8.20101010git6c0a9e6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.0-0.7.20101010git6c0a9e6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.7.0-0.6.20101010git6c0a9e6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Tue Dec 16 2010 Dmitrij S. Kryzhevich <krege@land.ru> - 2.7.0-0.5.20101010git6c0a9e6
- Add symlink kdirstat -> k4dirstat.

* Sat Dec 04 2010 Dmitrij S. Kryzhevich <krege@land.ru> - 2.7.0-0.4.20101010git6c0a9e6
- Cleanup spec.

* Mon Oct 11 2010 Dmitrij S. Kryzhevich <krege@land.ru> - 2.7.0-0.3.20101010git6c0a9e6
- Sources update to git 6c0a9e6.
- Zlib patch dropped.
- Add obsoletes for kdirstat.

* Sun Oct 10 2010 Dmitrij S. Kryzhevich <krege@land.ru> - 2.7.0-0.2.20101010gitdd2de8e
- Change kdebase-devel to kdebase4-devel for sure.

* Sun Oct 10 2010 Dmitrij S. Kryzhevich <krege@land.ru> - 2.7.0-0.1.20101010gitdd2de8e
- Sources update.
- %%fles clean up.
- Add script for getting sources.
- Add LGPLv2 to License.
- Add kdebase-devel to BR.
- Move desktop-file-validate to %%check.
- Update zlib patch.

* Tue Jun  8 2010  <Laurent.Rineau__fedora@normalesup.org> - 0-0.6.20100304gitec01dd42
- %%{_kde4_docdir}/HTML/en/k4dirstat/ must be owned.

* Tue Jun  8 2010  <Laurent.Rineau__fedora@normalesup.org> - 0-0.5.20100304gitec01dd42
- Fix the changelog (bad email and bad use of %%{?dist}).

* Tue Jun  8 2010  <Laurent.Rineau__fedora@normalesup.org> - 0-0.4.20100304gitec01dd42
- Patch0 for F-13: link explicitly with zlib.
- Add a comment on Source0.

* Sat Mar  6 2010  <Laurent.Rineau__fedora@normalesup.org> - 0-0.3.20100304gitec01dd42
- New upstream version.
- New doc files (added upstream). Among them: COPYING, README, AUTHORS.
- Patch0 is merged upstream.

* Tue Mar  2 2010  <Laurent.Rineau__fedora@normalesup.org> - 0-0.2.20100223gitd3b530af3
- Use kde4 rpm macros.

* Tue Mar  2 2010  <Laurent.Rineau__fedora@normalesup.org> - 0-0.1.20100223gitd3b530af3
- Initial build.
