# $Id$

# Authority: dag

# Upstream: Olivier Sessink <olivier@bluefish.openoffice.nl>

%define dfi %(which desktop-file-install &>/dev/null; echo $?)

Summary: A personal password manager for GNOME
Name: gpasman
Version: 1.2.0
Release: 0
License: GPL
Group: Applications/Productivity
URL: http://gpasman.sf.net/

Packager: Dag Wieers <dag@wieers.com>
Vendor: Dag Apt Repository, http://dag.wieers.com/apt/

Source: http://gpasman.sf.net/files/gpasman-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root


%description
Gpasman is a password manager. People working with the internet have to
remember lots of passwords. Saving them in a textfile is not a secure
idea. Gpasman is a GTK solution to this problem since it saves the
password information encrypted, so now you have to remember only one
password instead of ten (or more).

%prep
%setup

%build
%configure
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__install} -d -m0755 %{buildroot}%{_bindir}
%makeinstall

cat <<EOF >gnome-%{name}.desktop
[Desktop Entry]
Name=Password manager
Comment=%{summary}
Icon=keyring.png
Exec=gpasman
Terminal=false
Type=Application
EOF

%if %{dfi}
	%{__install} -d -m0755 %{buildroot}%{_datadir}/gnome/apps/Utilities
	%{__install} -m0644 gnome-%{name}.desktop %{buildroot}%{_datadir}/gnome/apps/Utilities/
%else
	%{__install} -d -m0755 %{buildroot}%{_datadir}/applications
	desktop-file-install --vendor gnome                \
		--add-category X-Red-Hat-Base              \
		--add-category Application                 \
		--add-category Utility                     \
		--dir %{buildroot}%{_datadir}/applications \
		gnome-%{name}.desktop
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc AUTHORS BUGS ChangeLog COPYING NEWS README
%{_bindir}/*
%if %{dfi}
        %{_datadir}/gnome/apps/Utilities/*.desktop
%else
        %{_datadir}/applications/*.desktop
%endif

%changelog
* Sun Mar 23 2003 Dag Wieers <dag@wieers.com> - 1.2.0-0
- Initial package. (using DAR)
