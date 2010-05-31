%define rel 1

%define _unpackaged_files_terminate_build 0

Name:       kdebase-runtime
Summary:    KDE Runtime
Version:    %{version}
Release:    %{rel}.qubes
Epoch:      1000

# http://techbase.kde.org/Policies/Licensing_Policy
License:    LGPLv2+
URL:        http://www.kde.org/

Source0:    kdebase-runtime-%{version}.tar.bz2

###############################################################
# Qubes Patches:

Patch100: kdebase-runtime-4.4.3-qubes-cleanup.patch

###############################################################

Provides:   kdebase4-runtime = %{version}-%{release}

# knotify4 provides dbus service org.freedesktop.Notifications too 
Provides:   desktop-notification-daemon

# ensure default/fallback icon theme present
# beware of bootstrapping, there be dragons
Requires:   oxygen-icon-theme >= %{version}

BuildRequires: kde-filesystem
BuildRequires: alsa-lib-devel
BuildRequires: attica-devel
BuildRequires: bzip2-devel
#BuildRequires: clucene-core-devel
BuildRequires: exiv2-devel
BuildRequires: hal-devel
BuildRequires: kdelibs4-devel >= %{version}
#BuildRequires: libsmbclient-devel
#BuildRequires: libssh-devel >= 0.4.2
BuildRequires: libXScrnSaver-devel
BuildRequires: OpenEXR-devel
BuildRequires: openssl-devel
BuildRequires: pkgconfig
BuildRequires: pulseaudio-libs-devel
BuildRequires: qimageblitz-devel
BuildRequires: shared-desktop-ontologies-devel
BuildRequires: soprano-devel >= 2.3.0
BuildRequires: xorg-x11-font-utils
BuildRequires: xorg-x11-proto-devel
BuildRequires: xz-devel
BuildRequires: zlib-devel

%description
Core runtime for KDE 4.

%package libs
Summary: Runtime libraries for %{name}
Group:   System Environment/Libraries
Requires: kdelibs4%{?_isa} >= %{version}
Requires: %{name} = %{version}-%{release}
%description libs
%{summary}.


%package flags
Summary: Geopolitical flags
Group: User Interface/Desktops
Requires: %{name} = %{version}-%{release}
BuildArch: noarch
%description flags
%{summary}.


%prep
%setup -q -n kdebase-runtime-%{version}%{?alphatag}

%patch100 -p1 -b .qubes-cleanup
%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf $RPM_BUILD_ROOT

make install/fast DESTDIR=$RPM_BUILD_ROOT -C %{_target_platform}

# kdesu symlink
ln -s %{_kde4_libexecdir}/kdesu $RPM_BUILD_ROOT%{_kde4_bindir}/kdesu

# omit hicolor index.theme, use one from hicolor-icon-theme
#rm -f $RPM_BUILD_ROOT%{_kde4_iconsdir}/hicolor/index.theme

%clean
rm -rf $RPM_BUILD_ROOT

%post
touch --no-create %{_kde4_iconsdir}/crystalsvg &> /dev/null || :
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/crystalsvg &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
update-desktop-database -q &> /dev/null ||:
update-mime-database %{_kde4_datadir}/mime &> /dev/null

%postun
if [ $1 -eq 0 ] ; then
    touch --no-create %{_kde4_iconsdir}/crystalsvg &> /dev/null || :
    touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :
    gtk-update-icon-cache %{_kde4_iconsdir}/crystalsvg &> /dev/null || :
    gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
    update-desktop-database -q &> /dev/null ||:
    update-mime-database %{_kde4_datadir}/mime &> /dev/null
fi

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%{_kde4_bindir}/*
# FIXME(?), currently contains cmake/modules -- Rex
%{_kde4_appsdir}/*
%{_kde4_configdir}/*.knsrc
%{_kde4_datadir}/config.kcfg/
%{_datadir}/dbus-1/interfaces/*
%{_datadir}/dbus-1/services/*
%{_kde4_datadir}/kde4/services/*
%{_kde4_datadir}/kde4/servicetypes/*
%{_kde4_datadir}/sounds/*
%{_kde4_libdir}/kconf_update_bin/*
%{_kde4_libdir}/libkdeinit4_*.so
%{_kde4_libdir}/kde4/kcm_*.so
%{_kde4_libdir}/kde4/kded_*.so
%{_kde4_libexecdir}/*
%{_mandir}/man1/*
%{_mandir}/man8/*
%{_kde4_docdir}/HTML/en/*
%{_kde4_sysconfdir}/xdg/menus/kde-information.menu
%{_kde4_datadir}/desktop-directories/*.directory
%{_kde4_datadir}/emoticons/kde4/
%{_kde4_datadir}/locale/en_US/entry.desktop
%{_kde4_datadir}/locale/l10n/
%{_kde4_datadir}/locale/currency/
%{?flags:%exclude %{_kde4_datadir}/locale/l10n/*/flag.png}

%files libs
%defattr(-,root,root,-)
%{_kde4_libdir}/kde4/*.so
%exclude %{_kde4_libdir}/kde4/kcm_*.so
%exclude %{_kde4_libdir}/kde4/kded_*.so
%{_kde4_libdir}/kde4/plugins/phonon_platform/
%{_kde4_libdir}/kde4/plugins/styles/

%files flags
%defattr(-,root,root,-)
%{_kde4_datadir}/locale/l10n/*/flag.png


%changelog
* Mon May 24 2010 Joanna Rutkowska <joanna@invisiblethingslab.com>
- spec file adapted to Qubes OS (based on Fedora spec)
- based on the original spec from Fedora 12:


