Name:           infocenter
Version:        2.3.0
Release:        0
Summary:        Information Center
License:        GPL-2.0
URL:            https://github.com/grouplinuxclient/infocenter/
Source0:        %{name}-%{version}.tar.xz
BuildRequires:  meson
BuildRequires:  python-rpm-macros
BuildRequires:  python3-devel >= 3.6
BuildRequires:  python3-distro
BuildRequires:  python3-pydbus
BuildRequires:  blueprint-compiler
BuildRequires:  gtk-update-icon-cache
BuildRequires:  desktop-file-utils
BuildRequires:  gtk4
BuildRequires:  libadwaita-devel
Requires:       python3 >= 3.6
Requires:       python3-pydbus
Recommends:     python3-distro
Recommends:     python3-dnspython
Recommends:     python3-netifaces
Recommends:     python3-pycryptodomex
BuildArch:      noarch

%description
Information Center utility offers basic information about the current system which is valuable in support cases.
Furthermore it includes basic disclaimer text for using the client in a corporate environment.

%prep
%setup -q

%build
%meson
%meson_build

%install
%meson_install

%check
%meson_test

%files
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{python3_sitelib}/*
%{_datadir}/applications/de.volkswagen.infocenter.desktop
%{_datadir}/glib-2.0/schemas/de.volkswagen.infocenter.gschema.xml
%{_datadir}/icons/hicolor/scalable/apps/de.volkswagen.infocenter.svg
%{_datadir}/icons/hicolor/scalable/apps/test-symbolic.svg
%{_datadir}/icons/hicolor/symbolic/apps/de.volkswagen.infocenter-symbolic.svg
%{_datadir}/infocenter/infocenter.gresource
%{_datadir}/locale/de/LC_MESSAGES/de.volkswagen.infocenter.mo
%{_datadir}/metainfo/de.volkswagen.infocenter.metainfo.xml

%changelog
* Tue Aug 5 2025 Jan-Michael Brummer <jan-michael.brummer1@volkswagen.de> 2.3.0-0
- Update to 2.3.0