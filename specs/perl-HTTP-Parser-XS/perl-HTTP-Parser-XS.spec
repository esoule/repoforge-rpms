# $Id$
# Authority: shuff
# Upstream: Kazuho Oku <kozuhooku$gmail,com>

%define perl_vendorlib %(eval "`perl -V:installvendorlib`"; echo $installvendorlib)
%define perl_vendorarch %(eval "`perl -V:installvendorarch`"; echo $installvendorarch)

%define real_name HTTP-Parser-XS

Summary: A fast, primitive HTTP request parser
Name: perl-HTTP-Parser-XS
Version: 0.14
Release: 1%{?dist}
License: Artistic/GPL
Group: Applications/CPAN
URL: http://search.cpan.org/dist/HTTP-Parser-XS/

Source: http://search.cpan.org/CPAN/authors/id/K/KA/KAZUHO/HTTP-Parser-XS-%{version}.tar.gz
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: perl
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(Test::More)
BuildRequires: rpm-macros-rpmforge
Requires: perl

### remove autoreq Perl dependencies
%filter_from_requires /^perl.*/d
%filter_setup

%description
HTTP::Parser::XS is a fast, primitive HTTP request/response parser.

The request parser can be used either for writing a synchronous HTTP server or
a event-driven server.

The response parser can be used for writing HTTP clients.

%prep
%setup -n %{real_name}-%{version}

# fix problem with modules generated by older versions of Dist::Zilla
#%{?el5:%{__perl} -pi -e '/.*ExtUtils::MakeMaker.*6\.31.*/ && s/6\.3\d/6.30/' Makefile.PL}

%build
%{__perl} Makefile.PL INSTALLDIRS="vendor" PREFIX="%{buildroot}%{_prefix}"
%{__make} %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
%{__make} pure_install
#%{__rm} -rf %{buildroot}%{perl_archlib} %{buildroot}%{perl_vendorarch}

# fix for stupid strip issue
#%{__chmod} -R u+w %{buildroot}/*

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-, root, root, 0755)
%doc Changes META.yml README benchmark/
%doc %{_mandir}/man?/*
%{perl_vendorarch}/HTTP/Parser/XS.pm
%{perl_vendorarch}/HTTP/Parser/XS/*
#%exclude %{perl_archlib}/perllocal.pod
%{perl_vendorarch}/auto/*/*/*/*
%exclude %{perl_vendorarch}/auto/*/*/*/.packlist

%changelog
* Tue Jul 19 2011 Steve Huff <shuff@vecna.org> - 0.14-1
- Initial package.