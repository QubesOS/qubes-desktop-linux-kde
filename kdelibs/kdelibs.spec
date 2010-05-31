%define rel 1

Summary: KDE Libraries
Version: %{version}
Release: %{rel}.qubes

Name: kdelibs
Provides: kdelibs4 = %{version}-%{release}
%{?_isa:Provides: kdelibs4%{?_isa} = %{version}-%{release}}
Provides: kdelibs-dom0, kdelibs4-dom0

# http://techbase.kde.org/Policies/Licensing_Policy
License: LGPLv2+
URL:     http://www.kde.org/
Source0: kdelibs-%{version}.tar.bz2

BuildRequires: kde4-macros(api) >= 2
BuildRequires: kde-filesystem >= 4-23

Requires: hicolor-icon-theme
Requires: kde-filesystem >= 4-23
Requires: kde-settings

Requires: hal
Requires: phonon
Requires: shared-desktop-ontologies
Requires: shared-mime-info

Source1: kde4.sh
Source2: kde4.csh

# Some of the Fedora patches used for their kdelibs package
###############################################################
# We're leaving them just in case ;)
#
# don't cache kdeglobals paths because they change after profile directories
# are loaded from kde4rc
Patch10: kdelibs-4.1.72-no-cache-kdeglobals-paths.patch

# patch KStandardDirs to use %{_libexecdir}/kde4 instead of %{_libdir}/kde4/libexec
Patch14: kdelibs-4.2.85-libexecdir.patch

# kstandarddirs changes: search /etc/kde, find %{_kde4_libexecdir}
Patch18: kdelibs-4.1.72-kstandarddirs.patch

# COMMENT ME PLEASE
Patch20: kdelibs-4.1.70-cmake.patch

# disable drkonqi by default, RHEL prefers/wants abrt
Patch24: kdelibs-4.3.1-drkonq.patch

# die rpath die, since we're using standard paths, we can avoid
# this extra hassle (even though cmake is *supposed* to not add standard
# paths (like /usr/lib64) already! With this, we can drop
# -DCMAKE_SKIP_RPATH:BOOL=ON (finally)
Patch27: kdelibs-4.3.98-no_rpath.patch

###############################################################
# Qubes Patches:

#Patch100: kdelibs-4.4.3-qubes-cleanup.patch

#
# END of Patches
###############################################################

BuildRequires: qt4-devel >= 4.6.0
Requires: qt4 >= 4.6.0
Requires: xdg-utils
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

BuildRequires: alsa-lib-devel
#BuildRequires: attica-devel >= %{attica_ver} 
BuildRequires: automoc4 >= 0.9.88
BuildRequires: avahi-devel
BuildRequires: bison flex
BuildRequires: bzip2-devel
BuildRequires: cmake >= 2.6.4
BuildRequires: cups-devel cups
BuildRequires: enchant-devel
BuildRequires: gamin-devel
BuildRequires: gettext-devel
BuildRequires: giflib-devel
BuildRequires: jasper-devel
BuildRequires: krb5-devel
BuildRequires: libacl-devel libattr-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: libtiff-devel
BuildRequires: libxslt-devel libxml2-devel
BuildRequires: libutempter-devel
BuildRequires: OpenEXR-devel
BuildRequires: openssl-devel
BuildRequires: pcre-devel
BuildRequires: phonon-devel >= %{phonon_ver} 
BuildRequires: polkit-qt-devel
BuildRequires: qca2-devel
#BuildRequires: shared-desktop-ontologies-devel
#BuildRequires: shared-mime-info
#BuildRequires: soprano-devel >= %{soprano_ver} 
#BuildRequires: strigi-devel >= %{strigi_ver} 
BuildRequires: xz-devel
BuildRequires: zlib-devel
# extra X deps (seemingly needed and/or checked-for by most kde4 buildscripts)
%define x_deps libSM-devel libXcomposite-devel libXdamage-devel libxkbfile-devel libXpm-devel libXScrnSaver-devel libXtst-devel libXv-devel libXxf86misc-devel
%{?x_deps:BuildRequires: %{x_deps}}

Provides: kross(javascript) = %{version}-%{release}
Provides: kross(qtscript) = %{version}-%{release}

%description
Libraries for KDE 4.

%package devel
Summary: Header files for compiling KDE 4 applications
Provides: plasma-devel = %{version}-%{release}
Requires: %{name}
Provides:  kdelibs4-devel = %{version}-%{release}
Requires: attica-devel >= %{attica_ver} 
Requires: automoc4 >= 0.9.88
Requires: cmake >= 2.6.4
Requires: openssl-devel
Requires: phonon-devel
Provides: nepomuk-devel = %{version}-%{release}
Requires: shared-desktop-ontologies-devel soprano-devel
Requires: qt4-devel
#Requires: qt4-webkit-devel

%description devel
This package includes the header files you will need to compile
applications for KDE 4.



%prep
%setup -q -n kdelibs-%{version}%{?alphatag}

%patch14 -p1 -b .libexecdir
%patch18 -p1 -b .kstandarddirs
%patch20 -p1 -b .xxcmake
%patch24 -p1 -b .drkonq
%patch27 -p1 -b .no_rpath

#%patch100 -p1 -b .qubes-cleanup
%build

# add release version
sed -i -e "s|@@VERSION_RELEASE@@|%{version}-%{release}|" kio/kio/kprotocolmanager.cpp

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} -DKDE_DISTRIBUTION_TEXT="%{version}-%{release} Qubes" ..
popd

make %{?_smp_mflags} -C %{_target_platform}

%install
rm -rf $RPM_BUILD_ROOT

make install/fast DESTDIR=$RPM_BUILD_ROOT -C %{_target_platform}

# see also use-of/patching of XDG_MENU_PREFIX in kdebase/kde-settings
mv $RPM_BUILD_ROOT%{_kde4_sysconfdir}/xdg/menus/applications.menu \
   $RPM_BUILD_ROOT%{_kde4_sysconfdir}/xdg/menus/kde4-applications.menu

# create/own, see http://bugzilla.redhat.com/483318
mkdir -p $RPM_BUILD_ROOT%{_kde4_libdir}/kconf_update_bin

# move devel symlinks
mkdir -p %{buildroot}%{_kde4_libdir}/kde4/devel
pushd %{buildroot}%{_kde4_libdir}
for i in lib*.so
do
  case "$i" in
    libkdeinit4_*.so)
      ;;
    ## FIXME/TODO: imo, should leave everything except for known-conflicts -- Rex
    *)
      linktarget=`readlink "$i"`
      rm -f "$i"
      ln -sf "../../$linktarget" "kde4/devel/$i"
      ;;
  esac
done
popd


install -p -m 644 -D %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/kde4.sh
install -p -m 644 -D %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d/kde4.csh

%post
/sbin/ldconfig
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null || :

%postun
/sbin/ldconfig ||:
if [ $1 -eq 0 ] ; then
    update-desktop-database -q &> /dev/null
    update-mime-database %{_kde4_datadir}/mime &> /dev/null
    touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null
    gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :
fi

%posttrans
update-desktop-database -q &> /dev/null
update-mime-database %{_kde4_datadir}/mime >& /dev/null
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null || :


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS README TODO
%doc COPYING.LIB
%config(noreplace) %{_sysconfdir}/profile.d/*
%{_kde4_bindir}/*
%exclude %{_kde4_bindir}/kconfig_compiler
%exclude %{_kde4_bindir}/makekdewidgets
%{_kde4_appsdir}/*
%exclude %{_kde4_appsdir}/kdewidgets/
%exclude %{_kde4_appsdir}/cmake/
%{_kde4_configdir}/*
%{_datadir}/dbus-1/interfaces/*
%{_datadir}/dbus-1/system-services/*
%{_polkit_qt_policydir}/org.kde.kcontrol.kcmremotewidgets.policy
%{_sysconfdir}/dbus-1/system.d/*
%{_kde4_datadir}/mime/packages/kde.xml
%{_kde4_sharedir}/kde4/services/*
%{_kde4_sharedir}/kde4/servicetypes/*
%{_kde4_iconsdir}/hicolor/*/*/*
%{_kde4_docdir}/HTML/en/sonnet/
%{_kde4_docdir}/HTML/en/kioslave/
%{_kde4_libdir}/lib*.so.*
%{_kde4_libdir}/lib*.so
#%{_kde4_libdir}/libkdeinit4_*.so
%{_kde4_libdir}/kconf_update_bin/
%dir %{_kde4_libdir}/kde4/
%{_kde4_libdir}/kde4/*.so
%{_kde4_libexecdir}/filesharelist
%{_kde4_libexecdir}/fileshareset
%{_kde4_libexecdir}/kauth-policy-gen
%{_kde4_libexecdir}/kcmremotewidgetshelper
%{_kde4_libexecdir}/kconf_update
%{_kde4_libexecdir}/kdesu_stub
%{_kde4_libexecdir}/kdontchangethehostname
%{_kde4_libexecdir}/kio_http_cache_cleaner
%{_kde4_libexecdir}/kioslave
%{_kde4_libexecdir}/klauncher
%{_kde4_libexecdir}/kmailservice
# see kio/misc/kpac/README.wpad 
%attr(4755,root,root) %{_kde4_libexecdir}/kpac_dhcp_helper
%{_kde4_libexecdir}/ksendbugmail
%{_kde4_libexecdir}/ktelnetservice
%{_kde4_libexecdir}/lnusertemp
%{_kde4_libexecdir}/start_kdeinit
%{_kde4_libexecdir}/start_kdeinit_wrapper
%{_kde4_libdir}/kde4/plugins/
%{_kde4_sysconfdir}/xdg/menus/*.menu
%{_mandir}/man1/checkXML.1*
%{_mandir}/man1/kde4-config.1*
%{_mandir}/man1/kjs.1*
%{_mandir}/man1/kjscmd.1*
%{_mandir}/man1/kross.1*
%{_mandir}/man7/kdeoptions.7*
%{_mandir}/man7/qtoptions.7*
%{_mandir}/man8/kbuildsycoca4.8*
%{_mandir}/man8/kcookiejar4.8*
%{_mandir}/man8/kded4.8*
%{_mandir}/man8/kdeinit4.8*
%{_mandir}/man8/meinproc4.8*

%{_kde4_docdir}/HTML/en/common/
%{_kde4_datadir}/locale/all_languages/

%files devel
%defattr(-,root,root,-)
%{_mandir}/man1/kdecmake.1*
%{_mandir}/man1/makekdewidgets.1*
%{_kde4_bindir}/kconfig_compiler
%{_kde4_bindir}/makekdewidgets
%{_kde4_appsdir}/cmake/
%{_kde4_appsdir}/kdewidgets/
%{_kde4_includedir}/*
%{_kde4_libdir}/kde4/devel/



%changelog

* Mon May 24 2010 Joanna Rutkowska <joanna@invisiblethingslab.com>
- spec file adapted to Qubes OS (based on Fedora spec)
- based on the original spec from Fedora 12:


