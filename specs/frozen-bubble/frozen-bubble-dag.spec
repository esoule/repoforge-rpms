# Authority: freshrpms
# Upstream: <contact@frozen-bubble.org>

%define dfi %(which desktop-file-install &>/dev/null; echo $?)

Summary: Frozen Bubble arcade game.
Name: frozen-bubble
Version: 1.0.0
Release: 0
License: GPL
Group: Amusements/Games
URL: http://www.frozen-bubble.org/

Packager: Dag Wieers <dag@wieers.com>
Vendor: Dag Apt Repository, http://dag.wieers.com/apt/

Source: http://frozenbubble.free.fr/fb/%{name}-%{version}.tar.bz2
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root


BuildRequires: perl-SDL, SDL-devel, SDL_mixer-devel >= 1.2.2
Requires: perl(SDL), SDL >= 1.2, SDL_mixer >= 1.2.2
AutoReq: no

%description
Full-featured, colorful animated penguin eyecandy, 50 levels of 1p game,
hours and hours of 2p game, 3 professional quality 20-channels musics, 15
stereo sound effects, 7 unique graphical transition effects.

%prep
%setup

%build
%{__make} %{?_smp_mflags} \
	PREFIX="%{_prefix}" \
	OPTIMIZE="%{optflags}"

%install
%{__rm} -rf %{buildroot}
%makeinstall \
	PREFIX="%{buildroot}%{_prefix}" \
	INSTALLARCHLIB="%{buildroot}%{perl_sitearch}" \
	INSTALLSITEARCH="%{buildroot}%{perl_sitearch}" \
	INSTALLVENDORARCH="%{buildroot}%{perl_sitearch}"
%{__rm} -f %{buildroot}%{perl_sitearch}/{build_fbsyms,perllocal.pod}
%{__install} -d -m0755 %{buildroot}%{_datadir}/pixmaps
%{__install} -m0644 icons/frozen-bubble-icon-48x48.png %{buildroot}%{_datadir}/pixmaps/frozen-bubble.png

cat <<EOF >gnome-%{name}.desktop
[Desktop Entry]
Name=Frozen Bubble
Comment=%{summary}
Icon=frozen-bubble.png
Exec=%{_bindir}/%{name}
Terminal=false
Type=Application
EOF

%if %{dfi}
	%{__install} -d -m0755 %{buildroot}%{_datadir}/gnome/apps/Games/
	%{__install} -m0644 gnome-%{name}.desktop %{buildroot}%{_datadir}/gnome/apps/Games/
%else
	%{__install} -d -m0755 %{buildroot}%{_datadir}/applications
	desktop-file-install --vendor gnome                \
		--add-category X-Red-Hat-Base              \
		--add-category Application                 \
		--add-category Game                        \
		--dir %{buildroot}%{_datadir}/applications \
		gnome-%{name}.desktop
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc AUTHORS CHANGES COPYING README
%doc %{_mandir}/man?/*
%{_bindir}/*
%{_datadir}/frozen-bubble/
%{_datadir}/pixmaps/*
%{perl_sitearch}/
%if %{dfi}
        %{_datadir}/gnome/apps/Games/*.desktop
%else
        %{_datadir}/applications/*.desktop
%endif

%changelog
* Tue Feb 18 2003 Dag Wieers <dag@wieers.com> - 1.0.0-0
- Updated to 1.0.0

* Sun Feb 16 2003 Dag Wieers <dag@wieers.com> - 0.9.3-0
- Initial package. (using DAR)
