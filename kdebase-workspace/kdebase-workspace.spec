%{!?python_sitearch:%global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

%define _unpackaged_files_terminate_build 0

Summary: KDE Workspace for Qubes Dom0
Name:    kdebase-workspace
Version: %{version}
Release: %{rel}.qubes
Epoch:   1000

License: GPLv2
Group:   User Interface/Desktops
URL:     http://www.kde.org/
Source0: kdebase-workspace-%{version}.tar.bz2
AutoReq: 0

# Some of the Fedora patches used for their kdebase-workspace package
###############################################################
# We're leaving them just in case ;)
#

# 434824: KDE4 System Settings - No Method To Enter Administrative Mode
Patch9: kdebase-workspace-4.3.75-rootprivs.patch

# We leave them just in case -- joanna
Patch11: kdebase-workspace-4.1.96-font.patch
Patch13: kdebase-workspace-4.2.0-pykde4.patch

Patch18: kdebase-workspace-4.4.2-kdm_plymouth.patch
Patch19: kdebase-workspace-4.4.2-kdm_plymouth081.patch

# We leave them just in case -- joanna
Patch20: kdebase-workspace-4.3.80-xsession_errors_O_APPEND.patch
# support the widgetStyle4 hack in the Qt KDE platform plugin
Patch21: kdebase-workspace-4.3.98-platformplugin-widgetstyle4.patch

###############################################################
# Qubes Patches:

Patch100: kdebase-workspace-4.4.5-qubes-cleanup.patch
Patch101: kdebase-workspace-4.4.3-plastik-for-qubes.patch

###############################################################
#BuildRequires: akonadi-devel
#BuildRequires: bluez-libs-devel
#BuildRequires: ConsoleKit-devel
BuildRequires: desktop-file-utils

BuildRequires: glib2-devel
BuildRequires: libutempter-devel
BuildRequires: libxklavier-devel
BuildRequires: libXau-devel
BuildRequires: libXdmcp-devel
BuildRequires: libXres-devel

BuildRequires: lm_sensors-devel

BuildRequires: NetworkManager-devel
BuildRequires: pam-devel
#BuildRequires: polkit-qt-devel
BuildRequires: qimageblitz-devel
BuildRequires: soprano-devel
BuildRequires: python-devel
BuildRequires: kdelibs4 >= %{version}
BuildRequires: kdelibs4-devel >= %{version}

Requires: kdebase-runtime >= %{version}

Requires: ksysguardd = %{version}-%{release}

Requires: libxklavier

# startkde references: dbus-launch df mkdir test xmessage xprop xrandr xrdb xset xsetroot
Requires: coreutils
Requires: dbus-x11
Requires: xorg-x11-apps
Requires: xorg-x11-utils
Requires: xorg-x11-server-utils


Provides: kdebase-workspace = %{version}-%{release}

%define default_face_icon default1.png

%description
The KDE Workspace for Qubes Dom0.

%package devel
Summary:  Development files for %{name}
Provides: solid-bluetooth-devel = %{version}-%{release} 
Requires: %{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
Requires: kdelibs4-devel
%description devel
%{summary}.

%package libs
Summary: Runtime libraries for %{name}
Provides: solid-bluetooth = %{version}-%{release} 
Requires: kdelibs4%{?_isa} >= %{version}
Requires: %{name} = %{version}-%{release}
%description libs
%{summary}.

%package wallpapers
Summary: KDE wallpapers
Requires: kde-filesystem
BuildArch: noarch
%description wallpapers
%{summary}.

%package -n kdm
Summary: The KDE login manager
Provides: kdebase-kdm = %{version}-%{release}
Provides: service(graphical-login) = kdm
Requires: kdelibs4%{?_isa} >= %{version}
Requires: kde-settings-kdm
%description -n kdm
KDM graphical login screen for Qubes.

%package -n ksysguardd
Summary: Performance monitor daemon
Group:   System Environment/Daemons
Provides: ksysguardd = %{version}-%{release}
%description -n ksysguardd
%{summary}.


%package -n oxygen-cursor-themes
Summary: Oxygen cursor themes
Group: User Interface/Desktops
BuildArch: noarch
%description -n oxygen-cursor-themes
%{summary}.

%prep

%setup -q -n kdebase-workspace-%{version}

%patch9 -p1 -b .rootprivs
%patch11 -p1 -b .font
#%patch13 -p1 -b .pykde4
%patch18 -p1 -b .kdm_plymouth
#%patch19 -p1 -b .kdm_plymouth
%patch20 -p1 -b .xsession_errors_O_APPEND
%patch21 -p1 -b .platformplugin-widgetstyle4

%patch100 -p1 -b .qubes-cleanup


rm -fr %_sourcedir/kdebase-workspace-%{version}/kwin/clients/plastik
ln -sf %_sourcedir/../plastik-for-qubes %_sourcedir/kdebase-workspace-%{version}/kwin/clients/plastik


%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} \
  -DKDE4_KDM_PAM_SERVICE=kdm \
  -DKDE4_KCHECKPASS_PAM_SERVICE=kcheckpass \
  -DKDE4_KSCREENSAVER_PAM_SERVICE=kscreensaver \
  ..
popd

# FIXME: not smp-safe?
#make -C %{_target_platform}
make %{?_smp_mflags} -C %{_target_platform}

%install
rm -rf $RPM_BUILD_ROOT

make install/fast DESTDIR=$RPM_BUILD_ROOT -C %{_target_platform}

# xsession support
mkdir -p $RPM_BUILD_ROOT%{_datadir}/xsessions/
mv $RPM_BUILD_ROOT%{_kde4_appsdir}/kdm/sessions/kde.desktop \
   $RPM_BUILD_ROOT%{_kde4_appsdir}/kdm/sessions/kde-safe.desktop \
   $RPM_BUILD_ROOT%{_datadir}/xsessions/

# nuke, use external kde-settings-kdm
rm -rf  $RPM_BUILD_ROOT%{_kde4_configdir}/kdm

## unpackaged files
rm -fv $RPM_BUILD_ROOT%{_kde4_libdir}/libpolkitkdeprivate*.so

%check
for f in $RPM_BUILD_ROOT%{_kde4_datadir}/applications/kde4/*.desktop ; do
  desktop-file-validate $f
done


%clean
rm -rf $RPM_BUILD_ROOT

%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :
touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null || :

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &> /dev/null || :
update-desktop-database -q &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :
touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &> /dev/null || :
update-desktop-database -q &> /dev/null || :
fi

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README
%{_kde4_bindir}/kaccess                           
%{_kde4_bindir}/kapplymousetheme                  
%{_kde4_bindir}/kblankscrn.kss                    
%{_kde4_bindir}/kcheckrunning                     
%{_kde4_bindir}/kcminit                           
%{_kde4_bindir}/kcminit_startup                   
%{_kde4_bindir}/kdostartupconfig4                 
#%{_kde4_bindir}/klipper
%{_kde4_bindir}/kmenuedit
%{_kde4_bindir}/krandom.kss
%{_kde4_bindir}/krandrtray
%{_kde4_bindir}/krdb
%{_kde4_bindir}/krunner
%{_kde4_bindir}/ksmserver
%{_kde4_bindir}/ksplashsimple
%{_kde4_bindir}/ksplashx
%{_kde4_bindir}/ksplashx_scale
%{_kde4_bindir}/kstartupconfig4
%{_kde4_bindir}/ksysguard
%{_kde4_bindir}/ksystraycmd
%{_kde4_bindir}/kwin*
%{_kde4_bindir}/kxkb
%{_kde4_bindir}/plasma-desktop
#%{_kde4_bindir}/plasma-netbook
%{_kde4_bindir}/plasma-overlay
%{_kde4_bindir}/plasmaengineexplorer
%{_kde4_bindir}/plasmoidviewer
%{_kde4_bindir}/plasmawallpaperviewer
%{_kde4_bindir}/safestartkde
%{_kde4_bindir}/solid-action-desktop-gen
%{_kde4_bindir}/solid-bluetooth
%{_kde4_bindir}/solid-network
%{_kde4_bindir}/solid-powermanagement
%{_kde4_bindir}/startkde
%{_kde4_bindir}/systemsettings

%{_kde4_appsdir}/color-schemes/
%{_kde4_appsdir}/desktoptheme/
%{_kde4_appsdir}/kaccess/
%{_kde4_appsdir}/katepart/syntax/plasma-desktop-js.xml
%{_kde4_appsdir}/kcminput/
%{_kde4_appsdir}/kcmkeys/
%{_kde4_appsdir}/kcmsolidactions/
%{_kde4_appsdir}/kconf_update/
%{_kde4_appsdir}/kcontrol/
%{_kde4_appsdir}/kdisplay/
%{_kde4_appsdir}/khotkeys/
%{_kde4_appsdir}/kmenuedit/
%{_kde4_appsdir}/kscreenlocker/
%{_kde4_appsdir}/ksplash/
%{_kde4_appsdir}/ksysguard/
%{_kde4_appsdir}/kthememanager/
%{_kde4_appsdir}/kwin/
%{_kde4_appsdir}/kwrited/
%{_kde4_appsdir}/plasma/
%{_kde4_appsdir}/plasma-desktop/
#%{_kde4_appsdir}/plasma-netbook/
%{_kde4_appsdir}/plasma_scriptengine_ruby/
%{_kde4_appsdir}/powerdevil/
%{_kde4_appsdir}/solid/
%{_kde4_appsdir}/solidfakenetbackend/
%{_kde4_appsdir}/systemsettings/

#%{_kde4_configdir}/aurorae.knsrc
%{_kde4_configdir}/background.knsrc
%{_kde4_configdir}/colorschemes.knsrc
%{_kde4_configdir}/ksplash.knsrc
%{_kde4_configdir}/ksysguard.knsrc
%{_kde4_configdir}/plasma-overlayrc
%{_kde4_configdir}/plasma-themes.knsrc
%{_kde4_configdir}/wallpaper.knsrc

%{_kde4_datadir}/kde4/services/*
%exclude %{_kde4_datadir}/kde4/services/kdm.desktop
%{_kde4_datadir}/kde4/servicetypes/*
%{_kde4_datadir}/sounds/pop.wav
#%{_kde4_datadir}/autostart/klipper.desktop
%{_kde4_datadir}/autostart/krunner.desktop
%{_kde4_datadir}/autostart/plasma.desktop
%{_kde4_datadir}/autostart/plasma-desktop.desktop
%{_kde4_datadir}/applications/kde4/*
%{_sysconfdir}/dbus-1/system.d/*.conf
%{_datadir}/dbus-1/interfaces/*.xml
%{_datadir}/dbus-1/services/*.service
%{_datadir}/dbus-1/system-services/*.service
%{_kde4_datadir}/config.kcfg/*
%{_datadir}/xsessions/*.desktop
%{_kde4_docdir}/HTML/en/kcontrol/
#%{_kde4_docdir}/HTML/en/klipper/
%{_kde4_docdir}/HTML/en/kmenuedit/
%{_kde4_docdir}/HTML/en/ksysguard/
%{_kde4_docdir}/HTML/en/kxkb/
%{_kde4_docdir}/HTML/en/plasma-desktop/
%{_kde4_docdir}/HTML/en/systemsettings/
%{_kde4_iconsdir}/hicolor/*/*/*
%{_kde4_iconsdir}/oxygen/*/*/*
%{_kde4_libdir}/kde4/classic_mode.so
%{_kde4_libdir}/kde4/icon_mode.so
#%{_kde4_libdir}/kde4/ion_*.so
%{_kde4_libdir}/kde4/kcm_*.so
%exclude %{_kde4_libdir}/kde4/kcm_kdm.so
%{_kde4_libdir}/kde4/kded_*.so
%{_kde4_libdir}/kde4/krunner_*.so
%{_kde4_libdir}/kde4/kstyle_keramik_config.so
%{_kde4_libdir}/kde4/kwin*_*.so
%{_kde4_libdir}/kde4/plasma_animator_default.so
%{_kde4_libdir}/kde4/plasma_applet_*.so
%{_kde4_libdir}/kde4/plasma_containmentactions_*.so

%{_kde4_libdir}/kde4/plasma_appletscriptengine_dashboard.so
%{_kde4_libdir}/kde4/plasma_appletscriptengine_webapplet.so
%{_kde4_libdir}/kde4/plasma_containment_*.so
%{_kde4_libdir}/kde4/plasma_engine_*.so
#%{_kde4_libdir}/kde4/plasma-geolocation-ip.so
%{_kde4_libdir}/kde4/plasma_package*_*.so
%{_kde4_libdir}/kde4/plasma_wallpaper_*.so
%{_kde4_libdir}/kde4/solid_*.so
%{_kde4_libexecdir}/kcheckpass
%{_kde4_libexecdir}/kcmdatetimehelper
%{_kde4_libexecdir}/krootimage
%{_kde4_libexecdir}/kscreenlocker
%{_kde4_libexecdir}/ksysguardprocesslist_helper
%{_kde4_libexecdir}/test_kcm_xinerama
%{_kde4_libdir}/libkdeinit*.so
%{_kde4_libdir}/libkickoff.so
%{_kde4_libdir}/libsystemsettingsview.so
%{_kde4_libdir}/kconf_update_bin/*
%{_mandir}/man1/plasmaengineexplorer.1*

# googlegadgets
#%exclude %{_kde4_libdir}/kde4/plasma_package_ggl.so
#%exclude %{_kde4_libdir}/kde4/plasma_scriptengine_ggl.so
#%exclude %{_kde4_datadir}/kde4/services/*googlegadgets.desktop
# python widget
%exclude %{_kde4_datadir}/kde4/services/plasma-scriptengine*python.desktop
# akonadi
#%exclude %{_kde4_libdir}/kde4/plasma_engine_akonadi.so
#%exclude %{_kde4_datadir}/kde4/services/plasma-engine-akonadi.desktop
%{_kde4_bindir}/kfontinst
%{_kde4_bindir}/kfontview
%{_kde4_libdir}/kde4/fontthumbnail.so
%{_kde4_libdir}/kde4/kfontviewpart.so
%{_kde4_libdir}/kde4/kio_fonts.so
%{_kde4_libdir}/strigi/strigita_font.so
%{_kde4_libexecdir}/fontinst
%{_kde4_libexecdir}/fontinst_helper
%{_kde4_libexecdir}/fontinst_x11
%{_kde4_libexecdir}/kfontprint
%{_polkit_qt_policydir}/org.kde.fontinst.policy
%{_polkit_qt_policydir}/org.kde.kcontrol.kcmclock.policy
%{_polkit_qt_policydir}/org.kde.ksysguard.processlisthelper.policy
%{_kde4_appsdir}/kfontinst/
%{_kde4_appsdir}/kfontview/
%{_kde4_appsdir}/konqsidebartng/virtual_folders/services/fonts.desktop

# PolicyKit-kde
#%exclude %{_kde4_sharedir}/kde4/services/kcm_pkk_authorization.desktop
#%exclude %{_kde4_datadir}/dbus-1/services/org.kde.PolicyKit.service
#%exclude %{_kde4_datadir}/dbus-1/services/kde-org.freedesktop.PolicyKit.AuthenticationAgent.service
#%exclude %{_kde4_libdir}/kde4/kcm_pkk_authorization.so

%files libs
%defattr(-,root,root,-)
%{_kde4_libdir}/lib*.so.*
#%exclude %{_kde4_libdir}/libpolkitkdeprivate.so.4*
%{_kde4_libdir}/libplasma_applet-system-monitor.so
%{_kde4_libdir}/kde4/plugins/designer/ksignalplotterwidgets.so
%{_kde4_libdir}/kde4/plugins/designer/ksysguardwidgets.so
%{_kde4_libdir}/kde4/plugins/designer/ksysguardlsofwidgets.so
%{_kde4_libdir}/kde4/plugins/gui_platform/libkde.so

%files devel
%defattr(-,root,root,-)
%{_kde4_includedir}/*
%{_kde4_libdir}/lib*.so
%{_kde4_appsdir}/cmake/modules/*.cmake
%{_kde4_libdir}/cmake/KDE4Workspace-%{version}/
%exclude %{_kde4_libdir}/libkdeinit*.so
%exclude %{_kde4_libdir}/libkickoff.so
%exclude %{_kde4_libdir}/libplasma_applet-system-monitor.so
%exclude %{_kde4_libdir}/libsystemsettingsview.so

%files wallpapers
%defattr(-,root,root,-)
%{_kde4_datadir}/wallpapers/*

%files -n kdm
%defattr(-,root,root,-)
%{_kde4_bindir}/genkdmconf
%{_kde4_bindir}/kdm
%{_kde4_bindir}/kdmctl
%{_kde4_libdir}/kde4/kcm_kdm.so
%{_kde4_libexecdir}/kdm_config
%{_kde4_libexecdir}/kdm_greet
%{_kde4_libdir}/kde4/kgreet_*.so
%{_kde4_configdir}/kdm.knsrc
%{_kde4_docdir}/HTML/en/kdm/
%dir %{_kde4_appsdir}/doc
%{_kde4_appsdir}/doc/kdm/
%{_kde4_appsdir}/kdm/
%{_kde4_datadir}/kde4/services/kdm.desktop

%files -n ksysguardd
%defattr(-,root,root,-)
%config(noreplace) %{_kde4_sysconfdir}/ksysguarddrc
%{_kde4_bindir}/ksysguardd

%files -n oxygen-cursor-themes
%defattr(-,root,root,-)
%{_kde4_iconsdir}/Oxygen_Black/
%{_kde4_iconsdir}/Oxygen_Black_Big/
%{_kde4_iconsdir}/Oxygen_Blue/
%{_kde4_iconsdir}/Oxygen_Blue_Big/
%{_kde4_iconsdir}/Oxygen_White/
%{_kde4_iconsdir}/Oxygen_White_Big/
%{_kde4_iconsdir}/Oxygen_Yellow/
%{_kde4_iconsdir}/Oxygen_Yellow_Big/
%{_kde4_iconsdir}/Oxygen_Zion/
%{_kde4_iconsdir}/Oxygen_Zion_Big/

%changelog

* Mon May 24 2010 Joanna Rutkowska <joanna@invisiblethingslab.com>
- spec file adapted to Qubes OS (based on Fedora spec)
- based on the original spec from Fedora 12:


