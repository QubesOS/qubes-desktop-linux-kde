%if 0%{?qubes_builder}
%define _sourcedir %(pwd)/plasma-breeze-qubes
%define _builddir  %(pwd)/plasma-breeze-qubes
%endif

%global         base_name   breeze
%global         build_kde4  1

Name:    plasma-breeze-qubes
Version: 5.5.4
Release: 1%{?dist}
Summary: Artwork, styles and assets for the Breeze visual style for the Plasma Desktop on Qubes OS

License: GPLv2+
URL:     https://qubes-os.org

%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/plasma/%{version}/%{base_name}-%{version}.tar.xz
Patch0:  0001-Initial-work-on-QubesOS-support.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  kf5-rpm-macros
BuildRequires:  extra-cmake-modules
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel

BuildRequires:  kf5-kservice-devel
BuildRequires:  kf5-kcmutils-devel
BuildRequires:  kf5-plasma-devel

# kde4breeze
BuildRequires:  kf5-kcoreaddons-devel
BuildRequires:  kf5-kconfig-devel
BuildRequires:  kf5-kguiaddons-devel

# kstyle
BuildRequires:  kf5-ki18n-devel
BuildRequires:  kf5-kcompletion-devel
BuildRequires:  kf5-frameworkintegration-devel
BuildRequires:  kf5-kwindowsystem-devel
BuildRequires:  kdecoration-devel

BuildRequires:  libxcb-devel

BuildRequires:  gettext

# icon optimizations
BuildRequires:  hardlink
# for optimizegraphics
BuildRequires:  kde-dev-scripts
BuildRequires:  time

Requires:       kf5-filesystem

Requires:       %{name}-common = %{version}-%{release}

Conflicts:      plasma-breeze
Provides:       plasma-breeze

%description
%{summary}.

%package        common
Summary:        Common files shared between KDE 4 and Plasma 5 versions of the Breeze style
BuildArch:      noarch

Conflicts:      plasma-breeze-common
Provides:       plasma-breeze-common
%description    common
%{summary}.

%if 0%{?build_kde4:1}
%package -n     kde-style-breeze-qubes
Summary:        KDE 4 version of Plasma 5 artwork, style and assets for Qubes OS
BuildRequires:  kdelibs4-devel
BuildRequires:  libxcb-devel
Requires:       %{name}-common = %{version}-%{release}
Obsoletes:      plasma-breeze-kde4 < 5.1.95
Provides:       plasma-breeze-kde4%{?_isa} = %{version}-%{release}

Conflicts:      kde-style-breeze
Provides:       kde-style-breeze

%description -n kde-style-breeze-qubes
%{summary}.
%endif

%prep
%setup -q -n %{base_name}-%{version}
%patch0 -p1

%build
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake_kf5} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%if 0%{?build_kde4:1}
mkdir %{_target_platform}_kde4
pushd %{_target_platform}_kde4
%{cmake_kde4} -DUSE_KDE4=TRUE ..
popd

make %{?_smp_mflags} -C %{_target_platform}_kde4
%endif


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}
%find_lang breeze --with-qt --all-name

%if 0%{?build_kde4:1}
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}_kde4
%endif

# omit/rename kde4breeze.upd, seems to be causing problems for
# (at least) new users, lame workaround for
# http://bugzilla.redhat.com/1283348
mv %{buildroot}%{_kf5_datadir}/kconf_update/kde4breeze.upd \
   %{buildroot}%{_kf5_datadir}/kconf_update/kde4breeze.upd.BAK

# plasma-breeze-qubes does not provide a cursor sub-package.
rm -rf %{buildroot}%{_kf5_datadir}/icons/breeze_cursors/
rm -rf %{buildroot}%{_kf5_datadir}/icons/Breeze_Snow/

%post
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_datadir}/icons/hicolor &> /dev/null || :
gtk-update-icon-cache %{_datadir}/icons/hicolor &> /dev/null || :
fi

%files
%license COPYING COPYING-ICONS
%{_kf5_qtplugindir}/org.kde.kdecoration2/breezedecoration.so
%{_kf5_qtplugindir}/styles/breeze.so
%{_kf5_datadir}/kstyle/themes/breeze.themerc
%{_kf5_qtplugindir}/kstyle_breeze_config.so
%{_kf5_datadir}/kconf_update/kde4breeze.upd*
%{_kf5_libdir}/kconf_update_bin/kde4breeze
%{_kf5_qmldir}/QtQuick/Controls/Styles/Breeze
%{_bindir}/breeze-settings5
%{_datadir}/icons/hicolor/*/apps/breeze-settings.*
%{_kf5_datadir}/kservices5/breezedecorationconfig.desktop
%{_kf5_datadir}/kservices5/breezestyleconfig.desktop
%{_kf5_datadir}/kservices5/plasma-lookandfeel-org.kde.breezedark.desktop.desktop
%{_kf5_datadir}/plasma/look-and-feel/org.kde.breezedark.desktop/

%files common -f breeze.lang
%{_datadir}/color-schemes/*.colors
%{_datadir}/QtCurve/Breeze.qtcurve
%{_datadir}/wallpapers/Next/

%if 0%{?build_kde4:1}
%files -n kde-style-breeze-qubes
%{_kde4_libdir}/kde4/plugins/styles/breeze.so
%{_kde4_libdir}/kde4/kstyle_breeze_config.so
%{_kde4_appsdir}/kstyle/themes/breeze.themerc
%endif

%changelog
* Wed Jan 27 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.4-1
- Plasma 5.5.4

* Fri Jan 08 2016 Rex Dieter <rdieter@fedoraproject.org> - 5.5.3-2
- .spec cosmetics
- drop icon-related deps
- breeze-cursor-theme: tighten %%files, don't use %%ghost, drop scriptlets
- avoid kde4breeze.upd, causes problems for new users (#1283348)

* Thu Jan 07 2016 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.3-1
- Plasma 5.5.3

* Thu Dec 31 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.5.2-1
- 5.5.2

* Fri Dec 18 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.1-1
- Plasma 5.5.1

* Thu Dec 03 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.5.0-1
- Plasma 5.5.0

* Wed Nov 25 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.95-2
- Plasma 5.4.95

* Sun Nov 15 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.3-5
- icon-theme/cursor theme: drop Requires: -common, add versioned Conflicts instead

* Sun Nov 15 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.3-4
- breeze-cursor-theme pkg (#1282203)

* Fri Nov 06 2015 Daniel Vrátil <dvraitl@fedoraproject.org> - 5.4.3-2
- tarball respin

* Thu Nov 05 2015 Daniel Vrátil <dvratil@fedoraproject.org> - 5.4.3-1
- Plasma 5.4.3

* Tue Oct 13 2015 Jan Grulich <jgrulich@redhat.com> - 5.4.2-2
- Fix breeze-dark icons inheritance

* Thu Oct 01 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.2-1
- 5.4.2

* Wed Sep 16 2015 Rex Dieter <rdieter@fedoraproject.org> 5.4.1-2
- breeze-icon-theme: optimizegraphics,hardlink optimizations

* Wed Sep 09 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.4.1-1
- 5.4.1

* Fri Aug 21 2015 Daniel Vrátil <dvratil@redhat.com> - 5.4.0-1
- Plasma 5.4.0

* Thu Aug 13 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.95-1
- Plasma 5.3.95

* Thu Jun 25 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.2-1
- Plasma 5.3.2

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 5.3.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.1-1
- Plasma 5.3.1

* Mon Apr 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.3.0-1
- Plasma 5.3.0

* Wed Apr 22 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.95-1
- Plasma 5.2.95

* Fri Mar 20 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.2-1
- Plasma 5.2.2

* Tue Mar 10 2015 Rex Dieter <rdieter@fedoraproject.org> - 5.2.1-3
- backport upstream fixes (mostly crashers)
- .spec cosmetics

* Fri Feb 27 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-2
- Rebuild (GCC 5)

* Tue Feb 24 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.1-1
- Plasma 5.2.1

* Mon Jan 26 2015 Daniel Vrátil <dvratil@redhat.com> - 5.2.0-1
- Plasma 5.2.0

* Mon Jan 12 2015 Daniel Vrátil <dvratil@redhat.com> - 5.1.95-1.beta
- Plasma 5.1.95 Beta

* Mon Jan 05 2015 Jan Grulich <jgrulich@redhat.com> - 5.1.1-2
- better URL
  breeze-kde4 renamed to kde-style-breeze
  created breeze-icon-theme subpackage
  used make install instead of make_install macro

* Wed Dec 17 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.2-2
- Plasma 5.1.2

* Fri Nov 07 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.1-1
- Plasma 5.1.1

* Tue Oct 14 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0.1-1
- Plasma 5.1.0.1

* Thu Oct 09 2014 Daniel Vrátil <dvratil@redhat.com> - 5.1.0-1
- Plasma 5.1.0

* Tue Sep 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.2-1
- Plasma 5.0.2

* Sun Aug 10 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.1-1
- Plasma 5.0.1

* Wed Jul 16 2014 Daniel Vrátil <dvratil@redhat.com> - 5.0.0-1
- Plasma 5.0.0

* Wed May 14 2014 Daniel Vrátil <dvratil@redhat.com> - 4.90.1-1.20140514git73a19ea
- Update to latest upstream

* Fri May 02 2014 Jan Grulich <jgrulich@redhat.com> 4.90.1-0.1.20140502git
- Initial version
