%define _unpackaged_files_terminate_build 0

Name:    kdebase
Summary: KDE Core Files
Version: %{version}
Release: %{rel}%{dist}
Epoch:   %{epoch}



License: GPLv2
URL: http://www.kde.org/
Source0: kdebase-%{version}.tar.bz2

###############################################################
# Qubes Patches:

Patch100: kdebase-4.4.3-qubes-cleanup.patch

###############################################################

Provides:  kdebase4 = %{version}-%{release}

# FIXME: remove BRs which are only needed for stuff now in -runtime
BuildRequires: alsa-lib-devel
BuildRequires: bzip2-devel
BuildRequires: cmake >= 2.6.2
BuildRequires: cyrus-sasl-devel
BuildRequires: doxygen
BuildRequires: fontconfig-devel
BuildRequires: gettext
BuildRequires: giflib-devel
BuildRequires: hal-devel
BuildRequires: pcre-devel
#BuildRequires: kdebase-workspace-devel
BuildRequires: kdelibs4-devel >= %{version}
BuildRequires: plasma-devel >= %{version}
BuildRequires: OpenEXR-devel
BuildRequires: openssl-devel
BuildRequires: pciutils-devel
BuildRequires: pcre-devel
BuildRequires: pkgconfig
BuildRequires: qimageblitz-devel
#BuildRequires: soprano-devel 
#BuildRequires: strigi-devel 
# needed?
BuildRequires: xorg-x11-font-utils
BuildRequires: xorg-x11-proto-devel
BuildRequires: glib2-devel

# Dolphin needs the ioslaves from kdebase-runtime (#438632)
Requires: kdebase-runtime

%description
Core runtime requirements and applications for KDE 4.

%prep
%setup -q -n kdebase-%{version}

%patch100 -p1 -b .qubes-cleanup
%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

%clean
rm -rf %{buildroot}


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
%{_kde4_bindir}/kdialog
%{_kde4_bindir}/konsole
%{_kde4_bindir}/konsoleprofile
%{_kde4_bindir}/kdepasswd
%{_kde4_appsdir}/kbookmark/
%{_kde4_appsdir}/kconf_update/*
%{_kde4_appsdir}/konsole/
%{_kde4_datadir}/config.kcfg/*
%{_datadir}/dbus-1/interfaces/*
%{_kde4_datadir}/kde4/services/*.desktop
%{_kde4_datadir}/kde4/services/ServiceMenus/
%{_kde4_datadir}/kde4/services/kded/*.desktop
%{_kde4_datadir}/kde4/servicetypes/*.desktop
%{_kde4_datadir}/applications/kde4/konsole.desktop
%{_kde4_datadir}/applications/kde4/kdepasswd.desktop
%{_kde4_libdir}/kde4/*.so
%{_kde4_datadir}/templates/*.desktop
%{_kde4_datadir}/templates/.source/*
%{_kde4_libdir}/libkdeinit4_*.so
%{_kde4_libdir}/libkonsoleprivate.so
%{_kde4_libdir}/libkonq.so*



%changelog
* Mon May 24 2010 Joanna Rutkowska <joanna@invisiblethingslab.com>
- spec file adapted to Qubes OS (based on Fedora spec)
- based on the original spec from Fedora 12:

