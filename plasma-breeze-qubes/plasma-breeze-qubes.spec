%if 0%{?qubes_builder}
%define _sourcedir %(pwd)/plasma-breeze-qubes
%define _builddir  %(pwd)/plasma-breeze-qubes
%endif

Name:    plasma-breeze-qubes
Version: 5.5.6
Release: 1%{?dist}
Summary: Qubes colorful frames for Breeze plasma theme

License: GPLv2+
URL:     https://qubes-os.org

Source0: qubes-generate-color-palette
Source1: qubes-generate-color-palette.desktop
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires:       plasma-breeze
Requires:       pyxdg

Obsoletes: kde-style-plastik-for-qubes

%description
%{summary}.

%prep
# nothing to do

%build
# nothing to do

%install
mkdir -p %{buildroot}/usr/bin
install -m 0755 %{SOURCE0} %{buildroot}/usr/bin/
mkdir -p %{buildroot}/etc/xdg/autostart
install -m 0644 %{SOURCE1} %{buildroot}/etc/xdg/autostart/

%files
/usr/bin/qubes-generate-color-palette
%config(noreplace) /etc/xdg/autostart/qubes-generate-color-palette.desktop

%changelog
