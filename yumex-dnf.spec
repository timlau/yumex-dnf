%global appname yumex

Name:     %{appname}-dnf
Version:  3.99.1
Release:  1%{?dist}
Summary:  Yum Extender graphical package management tool

Group:    Applications/System
License:  GPLv2+
URL:      http://yumex.dk
Source0:  https://fedorahosted.org/releases/y/u/yumex/%{name}-%{version}.tar.gz

BuildArch: noarch
BuildRequires: desktop-file-utils
BuildRequires: gettext
BuildRequires: intltool
BuildRequires: python3-devel

Requires: python3-dnfdaemon >= 0.1.1
Requires: python3-gobject >= 3.10
Requires: python3-pyxdg
Requires: python3-dbus
Requires: python3-cairo

%description
Graphical package tool for maintain packages on the system


%prep
%setup -q 


%build
make


%install
make install PYTHON=%{__python3} DESTDIR=$RPM_BUILD_ROOT DATADIR=%{_datadir}
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}.desktop    
desktop-file-validate %{buildroot}/%{_datadir}/applications/%{name}-local.desktop

%find_lang %name

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database %{_datadir}/applications &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :
fi
update-desktop-database %{_datadir}/applications &> /dev/null || :

%posttrans
/usr/bin/gtk-update-icon-cache -f %{_datadir}/icons/hicolor &>/dev/null || :

%files -f  %{name}.lang
%doc README.md COPYING
%{_datadir}/%{name}
%{_bindir}/%{name}
%{python3_sitelib}/*
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/
%{_datadir}/dbus-1/services/*

%changelog
* Sun Sep 15 2013 Tim Lauridsen <timlau@fedoraproject.org> 3.99.1-1
- Initial rpm build
