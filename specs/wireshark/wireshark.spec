#define as arch specific (1)
%define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")

#define to 0 for final version
%define svn_version 0
%define with_adns 0
%define with_lua 0
%if 0%{?rhel} != 0
%define with_portaudio 0
%else
%define with_portaudio 1
%endif

Summary: 	Network traffic analyzer
Name: 		wireshark
Version:	1.8.10
%if %{svn_version}
Release: 	0.%{svn_version}%{?dist}
%else
Release: 	7.2%{?dist}
%endif
License: 	GPL+
Group: 		Applications/Internet
%if %{svn_version}
Source0:	http://www.wireshark.org/download/automated/src/wireshark-%{version}-SVN-%{svn_version}.tar.bz2
%else
Source0:	http://wireshark.org/download/src/%{name}-%{version}.tar.bz2
%endif
Source3:	wireshark.desktop
Source4:	wireshark-autoconf.m4
Source5:	wireshark-mime-package.xml
Source6:	wiresharkdoc-16x16.png
Source7:	wiresharkdoc-32x32.png
Source8:	wiresharkdoc-48x48.png
Source9:	wiresharkdoc-256x256.png
Source10:	config.h

Patch1:		wireshark-1.2.4-enable_lua.patch
Patch2:		wireshark-libtool-pie.patch
Patch3:		wireshark-1.6.1-group-msg.patch
Patch4:		wireshark-1.6.0-soname.patch
Patch5:		wireshark-1.8.2-python-symbols.patch
Patch6:		wireshark-1.8.x-dns-cleanup.patch
Patch7:		wireshark-1.8.x-capture-crash.patch
Patch8:		wireshark-1.8.x-dcom-string-overrun.patch
Patch9:		wireshark-1.8.x-sctp-bytes-graph-crash.patch
Patch10:		wireshark-1.8.x-airpcap-crash.patch
Patch11:		wireshark-1.8.8-CVE-2013-3557.patch
Patch12:		wireshark-1.8.8-tshark-L-D-output.patch
Patch13:		wireshark-1.8.x-dumpcap-path.patch
Patch14:		wireshark-1.8.x-disable-warning-dialog.patch
Patch15:		wireshark-1.8.10-reassembly-memleak.patch
Patch16:		wireshark-1.8.10-cve-2013-6336.patch
Patch17:		wireshark-1.8.10-cve-2013-6338.patch
Patch18:		wireshark-1.8.10-cve-2013-6339.patch
Patch19:		wireshark-1.8.10-cve-2013-6340.patch
Patch20:		wireshark-1.8.10-cve-2013-7112.patch
Patch21:		wireshark-1.8.10-cve-2013-7114.patch
Patch22:		wireshark-1.8.10-cve-2014-2281.patch
Patch23:		wireshark-1.8.10-cve-2014-2283.patch
Patch24:		wireshark-1.8.10-cve-2014-2299.patch
Patch25:		wireshark-1.8.10-cve-2013-6337.patch

Url: 		http://www.wireshark.org/
BuildRoot: 	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	libpcap-devel >= 0.9
BuildRequires: 	libsmi-devel
BuildRequires: 	zlib-devel, bzip2-devel
BuildRequires:  openssl-devel
BuildRequires:	glib2-devel, gtk2-devel
BuildRequires:  elfutils-devel, krb5-devel
BuildRequires:  python, pcre-devel, libselinux
BuildRequires:  gnutls-devel
BuildRequires:  desktop-file-utils, automake, libtool
BuildRequires:	xdg-utils
BuildRequires: 	flex, bison, python
BuildRequires: 	libgcrypt-devel
%if %{with_adns}
BuildRequires:	adns-devel
%endif
%if %{with_portaudio}
BuildRequires: portaudio-devel
%endif
%if %{with_lua}
BuildRequires:	lua-devel
%endif
Obsoletes:	ethereal
Provides:	ethereal


%package	gnome
Summary:	Gnome desktop integration for wireshark and wireshark-usermode
Group:		Applications/Internet
Requires: 	gtk2
Requires:	usermode >= 1.37
Requires:	wireshark = %{version}-%{release}
Requires:	libsmi
Requires:	xdg-utils, usermode-gtk
%if %{with_adns}
Requires:	adns
%endif
%if %{with_portaudio}
Requires:	portaudio
%endif
Obsoletes:	ethereal-gnome
Provides:	ethereal-gnome

%package devel
Summary:        Development headers and libraries for wireshark
Group:		Development/Libraries
Requires:       %{name} = %{version}-%{release} glibc-devel glib2-devel


%description
Wireshark is a network traffic analyzer for Unix-ish operating systems.

This package lays base for libpcap, a packet capture and filtering
library, contains command-line utilities, contains plugins and
documentation for wireshark. A graphical user interface is packaged
separately to GTK+ package.

%description gnome
Contains wireshark for Gnome 2 and desktop integration file

%description devel
The wireshark-devel package contains the header files, developer
documentation, and libraries required for development of wireshark scripts
and plugins.


%prep
%if %{svn_version}
%setup -q -n %{name}-%{version}-SVN-%{svn_version}
%else
%setup -q -n %{name}-%{version}
%endif

%if %{with_lua}
%patch1 -p1 -b .enable_lua
%endif
%patch2 -p1 -b .v4cleanup
%patch3 -p1 -b .group-msg
%patch4 -p1 -b .soname
%patch5 -p1 -b .python-symbols
%patch6 -p1 -b .dns-cleanup
%patch7 -p1 -b .capture-crash
%patch8 -p1 -b .dcom-str-overrun
%patch9 -p1 -b .sctp-bytes-graph-crash
%patch10 -p1 -b .airpcap-crash
%patch11 -p1 -b .cve-2013-3557
%patch12 -p1 -b .tshark-L-D-output
%patch13 -p1 -b .dumpcap-path
%patch14 -p1 -b .disable-warning-dialog
%patch15 -p1 -b .reassembly-memleak
%patch16 -p1 -b .cve-2013-6336
%patch17 -p1 -b .cve-2013-6338
%patch18 -p1 -b .cve-2013-6339
%patch19 -p1 -b .cve-2013-6340
%patch20 -p1 -b .cve-2013-7112
%patch21 -p1 -b .cve-2013-7114
%patch22 -p1 -b .cve-2014-2281
%patch23 -p1 -b .cve-2014-2283
%patch24 -p1 -b .cve-2014-2299
%patch25 -p1 -b .cve-2013-6337

%build
%ifarch s390 s390x sparcv9 sparc64
export PIECFLAGS="-fPIE"
%else
export PIECFLAGS="-fpie"
%endif
# FC5+ automatic -fstack-protector-all switch
export RPM_OPT_FLAGS=${RPM_OPT_FLAGS//-fstack-protector/-fstack-protector-all}
export CFLAGS="$RPM_OPT_FLAGS $CPPFLAGS $PIECFLAGS -D_LARGEFILE64_SOURCE"
export CXXFLAGS="$RPM_OPT_FLAGS $CPPFLAGS $PIECFLAGS -D_LARGEFILE64_SOURCE"
export LDFLAGS="$LDFLAGS -lm -lcrypto -pie"
%if %{svn_version}
./autogen.sh
%endif

%configure \
   --bindir=%{_sbindir} \
   --with-zlib \
   --enable-ipv6 \
   --with-libsmi \
   --with-gnu-ld \
   --with-gtk3=no \
   --with-pic \
%if %{with_adns}
   --with-adns \
%else
   --with-adns=no \
%endif
%if %{with_lua}
   --with-lua \
%else
   --with-lua=no \
%endif
%if %{with_portaudio}
   --with-portaudio \
%else
   --with-portaudio=no \
%endif
   --with-ssl \
   --disable-warnings-as-errors \
   --with-plugins=%{_libdir}/%{name}/plugins/%{version} \
   --with-dumpcap-group="wireshark" \
   --enable-setcap-install \
   --enable-airpcap

# Remove rpath
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

# The evil plugins hack
perl -pi -e 's|-L../../epan|-L../../epan/.libs|' plugins/*/*.la

make DESTDIR=$RPM_BUILD_ROOT install

# Symlink tshark to tethereal
ln -s tshark $RPM_BUILD_ROOT%{_sbindir}/tethereal

# Install python stuff.
mkdir -p $RPM_BUILD_ROOT%{python_sitelib}
install -m 644 tools/wireshark_be.py tools/wireshark_gen.py  $RPM_BUILD_ROOT%{python_sitelib}

desktop-file-install                                            \
        --dir ${RPM_BUILD_ROOT}%{_datadir}/applications         \
        --add-category X-Fedora                                 \
        %{SOURCE3}

# Install desktop icons
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/{16x16,32x32,48x48,64x64,256x256}/apps
install -m 644 image/wsicon16.png $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/16x16/apps/wireshark.png
install -m 644 image/wsicon32.png $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/32x32/apps/wireshark.png
install -m 644 image/wsicon48.png $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/48x48/apps/wireshark.png
install -m 644 image/wsicon64.png $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/64x64/apps/wireshark.png
install -m 644 image/wsicon256.png $RPM_BUILD_ROOT/%{_datadir}/icons/hicolor/256x256/apps/wireshark.png

mkdir -p $RPM_BUILD_ROOT/%{_datadir}/{icons/gnome/{16x16,32x32,48x48,256x256}/mimetypes,mime/packages}
install -m 644 -T %{SOURCE5} $RPM_BUILD_ROOT/%{_datadir}/mime/packages/wireshark.xml
install -m 644 -T %{SOURCE6} $RPM_BUILD_ROOT/%{_datadir}/icons/gnome/16x16/mimetypes/application-x-pcap.png
install -m 644 -T %{SOURCE7} $RPM_BUILD_ROOT/%{_datadir}/icons/gnome/32x32/mimetypes/application-x-pcap.png
install -m 644 -T %{SOURCE8} $RPM_BUILD_ROOT/%{_datadir}/icons/gnome/48x48/mimetypes/application-x-pcap.png
install -m 644 -T %{SOURCE9} $RPM_BUILD_ROOT/%{_datadir}/icons/gnome/256x256/mimetypes/application-x-pcap.png

# Install devel files
install -d -m 0755  $RPM_BUILD_ROOT/%{_includedir}/wireshark
IDIR="${RPM_BUILD_ROOT}%{_includedir}/wireshark"
mkdir -p "${IDIR}/epan"
mkdir -p "${IDIR}/epan/crypt"
mkdir -p "${IDIR}/epan/ftypes"
mkdir -p "${IDIR}/epan/dfilter"
mkdir -p "${IDIR}/epan/dissectors"
mkdir -p "${IDIR}/wiretap"
mkdir -p "${IDIR}/wsutil"
install -m 644 color.h register.h		"${IDIR}/"
install -m 644 cfile.h file.h			"${IDIR}/"
install -m 644 packet-range.h print.h   	"${IDIR}/"
install -m 644 epan/*.h				"${IDIR}/epan/"
install -m 644 epan/crypt/*.h			"${IDIR}/epan/crypt"
install -m 644 epan/ftypes/*.h			"${IDIR}/epan/ftypes"
install -m 644 epan/dfilter/*.h			"${IDIR}/epan/dfilter"
install -m 644 epan/dissectors/*.h		"${IDIR}/epan/dissectors"
install -m 644 wiretap/*.h			"${IDIR}/wiretap"
install -m 644 wsutil/*.h			"${IDIR}/wsutil"
%ifarch %{ix86} s390 ppc
install -m 644 config.h				"${IDIR}/config-32.h"
%else
install -m 644 config.h				"${IDIR}/config-64.h"
%endif
install -m 644 -T %{SOURCE10}			"${IDIR}/config.h"

# Create pkg-config control file.
mkdir -p "${RPM_BUILD_ROOT}%{_libdir}/pkgconfig"
cat > "${RPM_BUILD_ROOT}%{_libdir}/pkgconfig/wireshark.pc" <<- "EOF"
	prefix=%{_prefix}
	exec_prefix=%{_prefix}
	libdir=%{_libdir}
	includedir=%{_includedir}

	Name:		%{name}
	Description:	Network Traffic Analyzer
	Version:	%{version}
	Requires:	glib-2.0 gmodule-2.0
	Libs:		-L${libdir} -lwireshark -lwiretap
	Cflags:		-DWS_VAR_IMPORT=extern -DHAVE_STDARG_H -DWS_MSVC_NORETURN= -I${includedir}/wireshark -I${includedir}/wireshark/epan
EOF

# Install the autoconf macro.
mkdir -p "${RPM_BUILD_ROOT}%{_datadir}/aclocal"
cp "%{SOURCE4}" "${RPM_BUILD_ROOT}%{_datadir}/aclocal/wireshark.m4"

# Remove .la files
rm -f $RPM_BUILD_ROOT/%{_libdir}/%{name}/plugins/%{version}/*.la

# Remove .la files in libdir
rm -f $RPM_BUILD_ROOT/%{_libdir}/*.la

# Add wspy_dissectors directory for plugins
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/%{name}/python/%{version}/wspy_dissectors

%clean
rm -rf $RPM_BUILD_ROOT

%pre
getent group wireshark >/dev/null || groupadd -r wireshark

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%post gnome
update-desktop-database &> /dev/null ||:
update-mime-database %{_datadir}/mime &> /dev/null || :
touch --no-create %{_datadir}/icons/gnome &>/dev/null || :
touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun gnome
update-desktop-database &> /dev/null ||:
update-mime-database %{_datadir}/mime &> /dev/null || :
if [ $1 -eq 0 ] ; then
	touch --no-create %{_datadir}/icons/gnome &>/dev/null
	gtk-update-icon-cache %{_datadir}/icons/gnome &>/dev/null || :

	touch --no-create %{_datadir}/icons/hicolor &>/dev/null
	gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/gnome &>/dev/null || :
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog INSTALL NEWS README*
%{_sbindir}/editcap
%{_sbindir}/tshark
%{_sbindir}/mergecap
%{_sbindir}/text2pcap
%{_sbindir}/dftest
%{_sbindir}/capinfos
%{_sbindir}/randpkt
%attr(0750, root, wireshark) %caps(cap_net_raw,cap_net_admin=eip) %{_sbindir}/dumpcap
%{_sbindir}/tethereal
%{_sbindir}/rawshark
%{python_sitelib}/*
%{_libdir}/lib*.so.*
%{_libdir}/wireshark/plugins
%{_mandir}/man1/editcap.*
%{_mandir}/man1/tshark.*
%{_mandir}/man1/mergecap.*
%{_mandir}/man1/text2pcap.*
%{_mandir}/man1/capinfos.*
%{_mandir}/man1/dumpcap.*
%{_mandir}/man4/wireshark-filter.*
%{_mandir}/man1/rawshark.*
%{_mandir}/man1/dftest.*
%{_mandir}/man1/randpkt.*
%{_datadir}/wireshark
%if %{with_lua}
%exclude %{_datadir}/wireshark/init.lua
%endif

%files gnome
%defattr(-,root,root)
%{_datadir}/applications/wireshark.desktop
%{_datadir}/icons/hicolor/16x16/apps/wireshark.png
%{_datadir}/icons/hicolor/32x32/apps/wireshark.png
%{_datadir}/icons/hicolor/48x48/apps/wireshark.png
%{_datadir}/icons/hicolor/64x64/apps/wireshark.png
%{_datadir}/icons/hicolor/256x256/apps/wireshark.png
%{_datadir}/icons/gnome/16x16/mimetypes/application-x-pcap.png
%{_datadir}/icons/gnome/32x32/mimetypes/application-x-pcap.png
%{_datadir}/icons/gnome/48x48/mimetypes/application-x-pcap.png
%{_datadir}/icons/gnome/256x256/mimetypes/application-x-pcap.png
%{_datadir}/mime/packages/wireshark.xml
%{_sbindir}/wireshark
%{_mandir}/man1/wireshark.*

%files devel
%defattr(-,root,root)
%doc doc/README.*
%if %{with_lua}
%config(noreplace) %{_datadir}/wireshark/init.lua
%endif
%{_includedir}/wireshark
%{_libdir}/lib*.so
%{_libdir}/pkgconfig/*
%{_datadir}/aclocal/*

%changelog
* Sun Jun 15 2014 Evgueni Souleimanov <esoule@100500.ca> 1.8.10-7.2
- run Wireshark GUI as user, not root (remove pam configs)
- allow packet capture to users who are members of group
  wireshark (using setcap)
- replace unrecognized configure options with equivalent
  ones that are recognized:
    --with-zlib
    --with-gtk3=no
    --with-plugins
    --enable-airpcap

* Wed Mar 26 2014 Peter Hatina <phatina@redhat.com> 1.8.10-7
- security patches
- Resolves: CVE-2013-6337

* Tue Mar 25 2014 Peter Hatina <phatina@redhat.com> 1.8.10-6
- security patches
- Resolves: CVE-2014-2281
            CVE-2014-2283
            CVE-2014-2299

* Tue Mar 11 2014 Peter Hatina <phatina@redhat.com> 1.8.10-5
- security patches
- Resolves: CVE-2013-6336
            CVE-2013-6338
            CVE-2013-6339
            CVE-2013-6340
            CVE-2013-7112
            CVE-2013-7114

* Tue Sep 24 2013 Peter Hatina <phatina@redhat.com> 1.8.10-4
- fix memory leak when reassemblying a packet
- Related: #711024

* Tue Sep 17 2013 Peter Hatina <phatina@redhat.com> 1.8.10-3
- fix config.h conflict
- Related: #711024

* Fri Sep 13 2013 Peter Hatina <phatina@redhat.com> 1.8.10-2
- do not configure with setcap-install
- Related: #711024

* Thu Sep 12 2013 Peter Hatina <phatina@redhat.com> 1.8.10-1
- upgrade to 1.8.10
- see http://www.wireshark.org/docs/relnotes/wireshark-1.8.10.html
- Related: #711024

* Wed Sep 11 2013 Peter Hatina <phatina@redhat.com> 1.8.8-10
- fix consolehelper path for dumpcap
- Related: #711024

* Wed Sep 11 2013 Peter Hatina <phatina@redhat.com> 1.8.8-9
- fix dumpcap group
- Related: #711024

* Wed Sep 11 2013 Peter Hatina <phatina@redhat.com> 1.8.8-8
- fix tshark output streams and formatting for -L, -D
- Resolves: #1004636

* Fri Sep  6 2013 Peter Hatina <phatina@redhat.com> 1.8.8-7
- fix double free in wiretap/netmon.c
- Related: #711024

* Fri Sep  6 2013 Peter Hatina <phatina@redhat.com> 1.8.8-6
- security patches
- Resolves: CVE-2013-4927
            CVE-2013-4931
            CVE-2013-4932
            CVE-2013-4933
            CVE-2013-4934
            CVE-2013-4935
            CVE-2013-3557

* Wed Jul  3 2013 Peter Hatina <phatina@redhat.com> 1.8.8-5
- fix desktop file
- Related: #711024

* Wed Jul  3 2013 Peter Hatina <phatina@redhat.com> 1.8.8-4
- fix tap-iostat buffer overflow
- fix dcom string overrun
- fix sctp bytes graph crash
- fix airpcap dialog crash
- Related: #711024

* Mon Jul  1 2013 Peter Hatina <phatina@redhat.com> 1.8.8-3
- fix dumpcap privileges to 755
- Related: #711024

* Mon Jul  1 2013 Peter Hatina <phtaina@redhat.com> 1.8.8-2
- new sources
- Related: #711024

* Tue Jun 11 2013 Peter Hatina <phatina@redhat.com> 1.8.8-1
- upgrade to 1.8.8
- see http://www.wireshark.org/docs/relnotes/wireshark-1.8.8.html
- Resolves: #711024
- Resolves: #858976
- Resolves: #699636
- Resolves: #750712
- Resolves: #832021
- Resolves: #889346
- Resolves: #659661
- Resolves: #715560

* Tue Apr 03 2012 Jan Synáček <jsynacek@redhat.com> 1.2.15-3
- security patches
- Resolves: CVE-2011-1143
            CVE-2011-1590
            CVE-2011-1957
            CVE-2011-1959
            CVE-2011-2174
            CVE-2011-2175 CVE-2011-1958
            CVE-2011-2597 CVE-2011-2698
            CVE-2011-4102
            CVE-2012-0041 CVE-2012-0066 CVE-2012-0067
            CVE-2012-0042
            CVE-2012-1595

* Fri Oct 21 2011 Jan Safranek <jsafrane@redhat.com> 1.2.15-2
- enhance NFS v4.1 traffic dissector (#746839)

* Tue Mar  8 2011 Jan Safranek <jsafrane@redhat.com> 1.2.15-1
- upgrade to 1.2.15
- see http://www.wireshark.org/docs/relnotes/wireshark-1.2.14.html
- see http://www.wireshark.org/docs/relnotes/wireshark-1.2.15.html
- Resolves: CVE-2011-0444 CVE-2011-0538 CVE-2011-0713 CVE-2011-1139
  CVE-2011-1140 CVE-2011-1141 CVE-2011-1143

* Wed Jan  5 2011 Jan Safranek <jsafrane@redhat.com>
- fix buffer overflow in ENTTEC dissector
- Resolves: #667338

* Fri Nov 26 2010 Jan Safranek <jsafrane@redhat.com> 1.2.13-1
- upgrade to 1.2.13
- see http://www.wireshark.org/docs/relnotes/wireshark-1.2.11.html
- see http://www.wireshark.org/docs/relnotes/wireshark-1.2.12.html
- see http://www.wireshark.org/docs/relnotes/wireshark-1.2.13.html
- Resolves: #657535 (CVE-2010-4300 CVE-2010-3445)

* Mon Aug 16 2010 Jan Safranek <jsafrane@redhat.com> 1.2.10-2
- fix crash when processing SCTP packets (#624032)

* Tue Aug 10 2010 Jan Safranek <jsafrane@redhat.com> 1.2.10-1
- upgrade to 1.2.10
- see http://www.wireshark.org/docs/relnotes/wireshark-1.2.10.html
- Resolves: #604312 (proper fix for CVE-2010-2284)

* Mon Jun 28 2010 Petr Lautrbach <plautrba@redhat.com> 1.2.9-2
- save and check child exit status
- Resolves: #579990

* Wed Jun 16 2010 Radek Vokal <rvokal@redhat.com> - 1.2.9-1
- upgrade to 1.2.9
- see http://www.wireshark.org/docs/relnotes/wireshark-1.2.9.html
- Resolves: #604312

* Mon May 10 2010 Radek Vokal <rvokal@redhat.com> - 1.2.8-1
- upgrade to 1.2.8
- see http://www.wireshark.org/docs/relnotes/wireshark-1.2.8.html
- use sitearch instead of sitelib to avoid pyo and pyc conflicts 
- bring back -pie
- add patch to allow decode of NFSv4.0 callback channel
- add patch to allow decode of more SMB FIND_FILE infolevels

* Thu Feb 25 2010 Radek Vokal <rvokal@redhat.com> - 1.2.6-2
- remove `time' from spec file

* Mon Feb 22 2010 Radek Vokal <rvokal@redhat.com> - 1.2.6-1
- upgrade to 1.2.6
- see http://www.wireshark.org/docs/relnotes/wireshark-1.2.6.html 
- minor spec file tweaks for better svn checkout support (#553500)
- init.lua is present always and not only when lua support is enabled
- fix file list, init.lua is only in -devel subpackage (#552406)
- Autoconf macro for plugin development.

* Fri Dec 18 2009 Radek Vokal <rvokal@redhat.com> - 1.2.5-1
- upgrade to 1.2.5
- fixes security vulnaribilities, see http://www.wireshark.org/security/wnpa-sec-2009-09.html 

* Thu Dec 17 2009 Radek Vokal <rvokal@redhat.com> - 1.2.4-3
- split -devel package (#547899, #203642, #218451)
- removing root warning dialog (#543709)

* Mon Dec 14 2009 Radek Vokal <rvokal@redhat.com> - 1.2.4-2
- enable lua support - http://wiki.wireshark.org/Lua
- attempt to fix filter crash on 64bits

* Wed Nov 18 2009 Radek Vokal <rvokal@redhat.com> - 1.2.4-1
- upgrade to 1.2.4
- http://www.wireshark.org/docs/relnotes/wireshark-1.2.4.html

* Fri Oct 30 2009 Radek Vokal <rvokal@redhat.com> - 1.2.3-1
- upgrade to 1.2.3
- http://www.wireshark.org/docs/relnotes/wireshark-1.2.3.html

* Mon Sep 21 2009 Radek Vokal <rvokal@redhat.com> - 1.2.2-1
- upgrade to 1.2.2
- http://www.wireshark.org/docs/relnotes/wireshark-1.2.2.html

* Mon Sep 14 2009 Bill Nottingham <notting@redhat.com> - 1.2.1-5
- do not use portaudio in RHEL

* Fri Aug 28 2009 Radek Vokal <rvokal@redhat.com> - 1.2.1-4
- yet anohter rebuilt

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 1.2.1-3
- rebuilt with new openssl

* Mon Jul 27 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 22 2009 Radek Vokal <rvokal@redhat.com> - 1.2.1
- upgrade to 1.2.1
- http://www.wireshark.org/docs/relnotes/wireshark-1.2.1.html

* Tue Jun 16 2009 Radek Vokal <rvokal@redhat.com> - 1.2.0
- upgrade to 1.2.0
- http://www.wireshark.org/docs/relnotes/wireshark-1.2.0.html

* Fri May 22 2009 Radek Vokal <rvokal@redhat.com> - 1.1.4-0.pre1
- update to latest development build

* Thu Mar 26 2009 Radek Vokal <rvokal@redhat.com> - 1.1.3-1
- upgrade to 1.1.3

* Thu Mar 26 2009 Radek Vokal <rvokal@redhat.com> - 1.1.2-4.pre1
- fix libsmi support

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.2-3.pre1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Radek Vokal <rvokal@redhat.com> - 1.1.2-2.pre1
- add netdump support

* Sun Feb 15 2009 Steve Dickson <steved@redhat.com> - 1.1.2-1.pre1
- NFSv4.1: Add support for backchannel decoding

* Mon Jan 19 2009 Radek Vokal <rvokal@redhat.com> - 1.1.2-0.pre1
- upgrade to latest development release
- added support for portaudio (#480195)

* Sun Jan 18 2009 Tomas Mraz <tmraz@redhat.com> - 1.1.1-0.pre1.2
- rebuild with new openssl

* Sat Nov 29 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 1.1.1-0.pre1.1
- Rebuild for Python 2.6

* Thu Nov 13 2008 Radek Vokál <rvokal@redhat.com> 1.1.1-0.pre1
- upgrade to 1.1.1 development branch

* Wed Sep 10 2008 Radek Vokál <rvokal@redhat.com> 1.0.3-1
- upgrade to 1.0.3
- Security-related bugs in the NCP dissector, zlib compression code, and Tektronix .rf5 file parser have been fixed. 
- WPA group key decryption is now supported. 
- A bug that could cause packets to be wrongly dissected as "Redback Lawful Intercept" has been fixed. 

* Mon Aug 25 2008 Radek Vokál <rvokal@redhat.com> 1.0.2-3
- fix requires for wireshark-gnome

* Thu Jul 17 2008 Steve Dickson <steved@redhat.com> 1.0.2-2
- Added patches to support NFSv4.1

* Fri Jul 11 2008 Radek Vokál <rvokal@redhat.com> 1.0.2-1
- upgrade to 1.0.2

* Tue Jul  8 2008 Radek Vokál <rvokal@redhat.com> 1.0.1-1
- upgrade to 1.0.1

* Sun Jun 29 2008 Dennis Gilmore <dennis@ausil.us> 1.0.0-3
- add sparc arches to -fPIE 
- rebuild for new gnutls

* Tue Apr  1 2008 Radek Vokál <rvokal@redhat.com> 1.0.0-2
- fix BuildRequires - python, yacc, bison

* Tue Apr  1 2008 Radek Vokál <rvokal@redhat.com> 1.0.0-1
- April Fools' day upgrade to 1.0.0

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.99.7-3
- Autorebuild for GCC 4.3

* Wed Dec 19 2007 Radek Vokál <rvokal@redhat.com> 0.99.7-2
- fix crash in unprivileged mode (#317681)

* Tue Dec 18 2007 Radek Vokál <rvokal@redhat.com> 0.99.7-1
- upgrade to 0.99.7

* Fri Dec  7 2007 Radek Vokál <rvokal@redhat.com> 0.99.7-0.pre2.1
- rebuilt for openssl

* Mon Nov 26 2007 Radek Vokal <rvokal@redhat.com> 0.99.7-0.pre2
- switch to libsmi from net-snmp
- disable ADNS due to its lack of Ipv6 support
- 0.99.7 prerelease 2

* Tue Nov 20 2007 Radek Vokal <rvokal@redhat.com> 0.99.7-0.pre1
- upgrade to 0.99.7 pre-release

* Wed Sep 19 2007 Radek Vokál <rvokal@redhat.com> 0.99.6-3
- fixed URL

* Thu Aug 23 2007 Radek Vokál <rvokal@redhat.com> 0.99.6-2
- rebuilt

* Mon Jul  9 2007 Radek Vokal <rvokal@redhat.com> 0.99.6-1
- upgrade to 0.99.6 final

* Fri Jun 15 2007 Radek Vokál <rvokal@redhat.com> 0.99.6-0.pre2
- another pre-release
- turn on ADNS support

* Wed May 23 2007 Radek Vokál <rvokal@redhat.com> 0.99.6-0.pre1
- update to pre1 of 0.99.6 release

* Mon Feb  5 2007 Radek Vokál <rvokal@redhat.com> 0.99.5-1
- multiple security issues fixed (#227140)
- CVE-2007-0459 - The TCP dissector could hang or crash while reassembling HTTP packets
- CVE-2007-0459 - The HTTP dissector could crash.
- CVE-2007-0457 - On some systems, the IEEE 802.11 dissector could crash.
- CVE-2007-0456 - On some systems, the LLT dissector could crash.

* Mon Jan 15 2007 Radek Vokal <rvokal@redhat.com> 0.99.5-0.pre2
- another 0.99.5 prerelease, fix build bug and pie flags

* Tue Dec 12 2006 Radek Vokal <rvokal@redhat.com> 0.99.5-0.pre1
- update to 0.99.5 prerelease

* Thu Dec  7 2006 Jeremy Katz <katzj@redhat.com> - 0.99.4-5
- rebuild for python 2.5 

* Tue Nov 28 2006 Radek Vokal <rvokal@redhat.com> 0.99.4-4
- rebuilt for new libpcap and net-snmp

* Thu Nov 23 2006 Radek Vokal <rvokal@redhat.com> 0.99.4-3
- add htmlview to Buildrequires to be picked up by configure scripts (#216918)

* Tue Nov  7 2006 Radek Vokal <rvokal@redhat.com> 0.99.4-2.fc7
- Requires: net-snmp for the list of MIB modules 

* Wed Nov  1 2006 Radek Vokál <rvokal@redhat.com> 0.99.4-1
- upgrade to 0.99.4 final

* Tue Oct 31 2006 Radek Vokál <rvokal@redhat.com> 0.99.4-0.pre2
- upgrade to 0.99.4pre2

* Tue Oct 10 2006 Radek Vokal <rvokal@redhat.com> 0.99.4-0.pre1
- upgrade to 0.99.4-0.pre1

* Fri Aug 25 2006 Radek Vokál <rvokal@redhat.com> 0.99.3-1
- upgrade to 0.99.3
- Wireshark 0.99.3 fixes the following vulnerabilities:
- the SCSI dissector could crash. Versions affected: CVE-2006-4330
- the IPsec ESP preference parser was susceptible to off-by-one errors. CVE-2006-4331
- a malformed packet could make the Q.2931 dissector use up available memory. CVE-2006-4333 

* Tue Jul 18 2006 Radek Vokál <rvokal@redhat.com> 0.99.2-1
- upgrade to 0.99.2

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.99.2-0.pre1.1
- rebuild

* Tue Jul 11 2006 Radek Vokál <rvokal@redhat.com> 0.99.2-0.pre1
- upgrade to 0.99.2pre1, fixes (#198242)

* Tue Jun 13 2006 Radek Vokal <rvokal@redhat.com> 0.99.1-0.pre1
- spec file changes

* Fri Jun  9 2006 Radek Vokal <rvokal@redhat.com> 0.99.1pre1-1
- initial build for Fedora Core
