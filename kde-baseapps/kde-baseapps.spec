%if 0%{?qubes_builder}
%define _sourcedir %(pwd)/kde-baseapps
%endif

# trim changelog included in binary rpms
%global _changelog_trimtime %(date +%s -d "1 year ago")

# enable tests
%global tests 1

Name:    kde-baseapps
Summary: KDE Core Applications 
Epoch:   2000
Version: 15.12.3
Release: 2%{?dist}

License: GPLv2 and GFDL
URL:     https://projects.kde.org/kde-baseapps
%global revision %(echo %{version} | cut -d. -f3)
%if %{revision} >= 50
%global stable unstable
%else
%global stable stable
%endif
Source0: http://download.kde.org/%{stable}/applications/%{version}/src/kde-baseapps-%{version}.tar.xz

## upstreamable patches
# search path for plugins
Patch0: kdebase-4.1.80-nsplugins-paths.patch

# make menuitem Home visible
Patch2: kdebase-4.2.1-home-icon.patch

# fix disabling automatic spell checking in the Konqueror UI (kde#228593)
Patch3: kdebase-4.4.0-konqueror-kde#228593.patch

# add x-scheme-handler/http for konqueror so it can be set
# as default browser in GNOME
Patch5: kde-baseapps-4.14.3-konq_mimetype.patch

## upstream patches

# optional runtime dep for kcm_useraccount, see https://git.reviewboard.kde.org/r/110875/
%if 0%{?fedora} || 0%{?rhel} > 6
Requires: accountsservice
%endif

## Qubes patches
Patch100: kde-baseapps-4.12-qubes.patch

%ifnarch s390 s390x
Requires: eject
%endif

# kdepasswd uses chfn
Requires: util-linux

Obsoletes: kdebase < 6:4.7.97-10
Provides:  kdebase = 6:%{version}-%{release}

Obsoletes: kdebase4 < %{version}-%{release}
Provides:  kdebase4 = %{version}-%{release}

BuildRequires: gcc-c++
BuildRequires: desktop-file-utils
%if 0%{fedora} < 22
BuildRequires: baloo-devel >= 4.14
BuildRequires: baloo-widgets-devel >= 4.14
BuildRequires: kactivities-devel
BuildRequires: kfilemetadata-devel >= 4.14
%endif
BuildRequires: kdelibs4-devel >= 4.14
%if 0%{?fedora} > 21
BuildRequires: libappstream-glib
%endif
%if 0%{?fedora}
BuildRequires: libtidy-devel
%endif
BuildRequires: pkgconfig
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(xrender)
BuildRequires: pkgconfig(zlib)

%if 0%{?tests}
%global _kde4_build_tests -DKDE4_BUILD_TESTS:BOOL=ON
# %%%check
BuildRequires: dbus-x11 xorg-x11-server-Xvfb
%endif

Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: kdepasswd = %{epoch}:%{version}-%{release}
Requires: kdialog = %{epoch}:%{version}-%{release}

# for upgrade path, when konsole, kwrite were split out since 4.7.90
%if 0%{?fedora} < 17 && 0%{?rhel} < 7
Requires: konsole
Requires: kwrite
%endif

%description
Metapackage for Core applications of KDE 4, including:
kdepasswd : Changes a UNIX password
kdialog : Nice dialog boxes from shell scripts
keditbookmarks : Bookmark organizer and editor
kfind : File find utility
konqueror : Web browser, file manager and document viewer

%package common
Summary: Common files for %{name}
Conflicts: kde-baseapps < 4.12.0-2
Obsoletes: kde-plasma-folderview < 6:%{version}-%{release}
BuildArch: noarch
%description common
%{summary}

%package libs
Summary: Runtime libraries for %{name}
Obsoletes: kdebase-libs < 6:4.7.97-10
Provides:  kdebase-libs < 6:%{version}-%{release}
Provides:  kdebase-libs%{?_isa} < 6:%{version}-%{release}
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: libkonq%{?_isa} = %{epoch}:%{version}-%{release}
%description libs
%{summary}.

%package devel
Summary:  Development files for %{name}
Obsoletes: kdebase-devel < 6:4.7.97-10
Provides:  kdebase-devel = 6:%{version}-%{release}
Obsoletes: kdebase4-devel < %{version}-%{release}
Provides:  kdebase4-devel = %{version}-%{release}
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: libkonq%{?_isa} = %{epoch}:%{version}-%{release}
Requires: kdelibs4-devel
%description devel
%{summary}.

%package -n kdepasswd
Summary: Changes your UNIX password
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%{?kde_runtime_requires}
%description -n kdepasswd
This application allows you to change your UNIX password.

%package -n kdialog
Summary:  Nice dialog boxes from shell scripts
Requires: %{name}-common = %{epoch}:%{version}-%{release}
%{?kde_runtime_requires}
%description -n kdialog
KDialog can be used to show nice dialog boxes from shell scripts.

%package -n libkonq
Summary: Libkonq shared resources
Requires: %{name}-common = %{epoch}:%{version}-%{release}
Requires: kdelibs4%{?_isa}%{?_kde4_version: >= %{_kde4_version}}
%description -n libkonq
%{summary}.

%prep
%setup -q -n kde-baseapps-%{version}

%patch0 -p2 -b .nsplugins-paths
%patch2 -p2 -b .home-icon
%patch3 -p2 -b .kde#228593
%patch5 -p1 -b .konq_mimetype

sed -i -e 's|^add_subdirectory(folderview)|#add_subdirectory(folderview)|g' plasma/applets/CMakeLists.txt

%patch100 -p1 -b .qubes

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

# create/own some dirs 
mkdir -p %{buildroot}%{_kde4_appsdir}/konqueror/{kpartplugins,icons,opensearch}

## unpackaged files
# libs for which there is no (public) api
rm -fv %{buildroot}%{_kde4_libdir}/lib{kbookmarkmodel_,konqueror}private.so
rm -fv %{buildroot}%{_kde4_libdir}/libdolphinprivate4.so
# omit konqsidebarplugin api bits (for now), nothing uses it afaict -- rex
rm -fv %{buildroot}%{_kde4_libdir}/libkonqsidebarplugin.so
rm -fv %{buildroot}%{_kde4_includedir}/konqsidebarplugin.h

# move devel symlinks
mkdir -p %{buildroot}%{_kde4_libdir}/kde4/devel
pushd %{buildroot}%{_kde4_libdir}
for i in lib*.so
do
  case "$i" in
    libkonq.so)
      linktarget=`readlink "$i"`
      rm -fv "$i"
      ln -sf "../../$linktarget" "kde4/devel/$i"
      ;;
    *)
      ;;
  esac
done
popd

# fix documentation multilib conflict in index.cache
for f in konqueror; do
   bunzip2 %{buildroot}%{_kde4_docdir}/HTML/en/$f/index.cache.bz2
   sed -i -e 's!name="id[a-z]*[0-9]*"!!g' %{buildroot}%{_kde4_docdir}/HTML/en/$f/index.cache
   sed -i -e 's!#id[a-z]*[0-9]*"!!g' %{buildroot}%{_kde4_docdir}/HTML/en/$f/index.cache
   bzip2 -9 %{buildroot}%{_kde4_docdir}/HTML/en/$f/index.cache
done

# Qubes cleanup
rm -f %{buildroot}%{_kde4_appsdir}/kbookmark/directory_bookmarkbar.desktop
rm -f %{buildroot}/usr/share/man/man1/kbookmarkmerger.1
rm -f %{buildroot}/usr/share/man/man1/kfind.1
rm -rf %{buildroot}/usr/share/doc/HTML/en/kfind
rm -rf %{buildroot}/usr/share/doc/HTML/en/konqueror
# part of konqueror
rm -f %{buildroot}/usr/share/dbus-1/interfaces/org.kde.FavIcon.xml

%find_lang kdepasswd --with-kde --without-mo


%check
%if 0%{?tests}
export CTEST_OUTPUT_ON_FAILURE=1
## setting semi-arbitrary 30 second timeout, KonqPopupMenuTest, seems to hang or take a really long time --rex
time xvfb-run -a dbus-launch --exit-with-session make -C %{_target_platform}/ test ARGS="--output-on-failure --timeout 30" ||:
%endif
for f in %{buildroot}%{_kde4_datadir}/applications/kde4/*.desktop ; do
  desktop-file-validate $f
done


%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:
touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null ||:

%posttrans
gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &> /dev/null ||:
update-desktop-database -q &> /dev/null ||:

%postun
if [ $1 -eq 0 ] ; then
  touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:
  touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null ||:
  gtk-update-icon-cache %{_kde4_iconsdir}/hicolor &> /dev/null ||:
  gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &> /dev/null ||:
  update-desktop-database -q &> /dev/null ||:
fi


%files
# empty metapackage

%files libs
# empty metapackage

%files common
%doc COPYING COPYING.DOC COPYING.LIB


%post -n libkonq -p /sbin/ldconfig
%postun -n libkonq -p /sbin/ldconfig

%files -n libkonq
%{_kde4_libdir}/libkonq.so.5*
%{_kde4_libdir}/kde4/kded_favicons.so
%{_kde4_libdir}/kde4/konq_sound.so
%{_kde4_appsdir}/kbookmark/
%dir %{_kde4_appsdir}/konqueror/
%dir %{_kde4_appsdir}/konqueror/pics/
%{_kde4_appsdir}/konqueror/pics/arrow_*.png
%{_kde4_datadir}/kde4/services/kded/favicons.desktop
%{_kde4_datadir}/kde4/servicetypes/konqdndpopupmenuplugin.desktop
%{_kde4_datadir}/kde4/servicetypes/konqpopupmenuplugin.desktop
%{_kde4_datadir}/templates/.source/*
%{_kde4_datadir}/templates/*.desktop

#files -n libkonq-devel
%files devel
%{_kde4_libdir}/kde4/devel/libkonq.so
%{_kde4_includedir}/knewmenu.h
%{_kde4_includedir}/konq_*.h
%{_kde4_includedir}/konqmimedata.h
%{_kde4_includedir}/kversioncontrolplugin*.h
%{_kde4_includedir}/libkonq_export.h

%files -n kdepasswd -f kdepasswd.lang
%{_kde4_bindir}/kdepasswd
%{_kde4_datadir}/applications/kde4/kdepasswd.desktop
%{_kde4_libdir}/kde4/kcm_useraccount.so
%{_kde4_datadir}/config.kcfg/kcm_useraccount.kcfg
%{_kde4_datadir}/config.kcfg/kcm_useraccount_pass.kcfg
%{_kde4_datadir}//kde4/services/kcm_useraccount.desktop
%dir %{_kde4_appsdir}/kdm
%dir %{_kde4_appsdir}/kdm/pics
%dir %{_kde4_appsdir}/kdm/pics/users/
%{_kde4_appsdir}/kdm/pics/users/*

%files -n kdialog
%{_kde4_bindir}/kdialog
%{_datadir}/dbus-1/interfaces/org.kde.kdialog.ProgressDialog.xml

%changelog
* Sun Mar 13 2016 Rex Dieter <rdieter@fedoraproject.org> - 15.12.3-1
- 15.12.3

* Fri Feb 12 2016 Rex Dieter <rdieter@fedoraproject.org> - 15.12.2-1
- 15.12.2

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 15.12.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 08 2016 Rex Dieter <rdieter@fedoraproject.org> 15.12.1-1
- 15.12.1, update URL

* Sun Dec 20 2015 Rex Dieter <rdieter@fedoraproject.org> 15.12.0-1
- 15.12.0

* Wed Nov 18 2015 Rex Dieter <rdieter@fedoraproject.org> - 15.08.3-1
- 15.08.3

* Wed Nov 18 2015 Rex Dieter <rdieter@fedoraproject.org> 15.08.2-2
- rebuild (tidy)

* Wed Oct 14 2015 Rex Dieter <rdieter@fedoraproject.org> - 15.08.2-1
- 15.08.2

* Wed Oct 14 2015 Rex Dieter <rdieter@fedoraproject.org> 
- 15.08.1-3
- konqueror: +Requires: keditbookmarks
- keditbookmarks-libs: fix description/summary

* Fri Oct 02 2015 Rex Dieter <rdieter@fedoraproject.org> 15.08.1-2
- drop use of kde4-specific /usr/share/autostart

* Tue Sep 15 2015 Rex Dieter <rdieter@fedoraproject.org> - 15.08.1-1
- 15.08.1
- dolphin4-libs: move dolphinpart here, drop dep on main pkg
- konqueror: Requires: dolphin4-libs (instead of dolphin4)

* Wed Sep 02 2015 Rex Dieter <rdieter@fedoraproject.org> - 15.08.0-2
- konqueror: Home.desktop here
- -libs: s/dolphin-libs/dolphin4-libs/

* Thu Aug 20 2015 Than Ngo <than@redhat.com> - 15.08.0-1
- 15.08.0

* Sun Jun 28 2015 Rex Dieter <rdieter@fedoraproject.org> - 15.04.3-1
- 15.04.3

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 15.04.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Jun 02 2015 Rex Dieter <rdieter@fedoraproject.org> - 15.04.2-1
- 15.04.2

* Thu May 14 2015 Rex Dieter <rdieter@fedoraproject.org> 15.04.1-1
- 15.04.1

* Fri May 01 2015 Rex Dieter <rdieter@fedoraproject.org> 15.04.0-3
- Added folders to left panel "Places" disappear (#345174)

* Wed Apr 15 2015 Rex Dieter <rdieter@fedoraproject.org> 15.04.0-2
- dolphin: Recommends: ruby (servicemenuinstallation)

* Tue Apr 14 2015 Rex Dieter <rdieter@fedoraproject.org> - 15.04.0-1
- 15.04.0

* Wed Mar 11 2015 Rex Dieter <rdieter@fedoraproject.org> - 14.12.3-3
- lower kfmclient_dir.desktop IntialPreference to 9, lower than dolphin 10 (f22+)
- omit kde-plasma-folderview (f22+)

* Tue Mar 10 2015 Rex Dieter <rdieter@fedoraproject.org> 14.12.3-2
- drop unused strigi/soprano build deps

* Sun Mar 01 2015 Rex Dieter <rdieter@fedoraproject.org> - 14.12.3-1
- 14.12.3

* Tue Feb 24 2015 Than Ngo <than@redhat.com> - 14.12.2-1
- 14.12.2

* Thu Feb 12 2015 Rex Dieter <rdieter@fedoraproject.org> 14.12.1-2
- dolphin: Requires: konsole4-part

* Sat Jan 17 2015 Rex Dieter <rdieter@fedoraproject.org> - 14.12.1-1
- 14.12.1

* Sat Dec 06 2014 Rex Dieter <rdieter@fedoraproject.org>  14.11.97-1
- 14.11.97

* Mon Nov 17 2014 Rex Dieter <rdieter@fedoraproject.org> 4.14.3-4
- add x-scheme-handler/http to kfmclient_html.desktop (kde#341055)

* Tue Nov 11 2014 Rex Dieter <rdieter@fedoraproject.org> 4.14.3-3
- respin tarball

* Tue Nov 11 2014 Rex Dieter <rdieter@fedoraproject.org> 4.14.3-2
- pull in upstream fix "Unbreak session management" for konqueror

* Sat Nov 08 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.14.3-1
- 4.14.3

* Sat Oct 11 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.14.2-1
- 4.14.2

* Thu Sep 25 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.14.1-2
- pull in upstream fixes, particularly...
- Fix scrollbar appearing on FolderView (kde#294795)

* Mon Sep 15 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.14.1-1
- 4.14.1

* Sat Aug 16 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.14.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Thu Aug 14 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.14.0-1
- 4.14.0

* Tue Aug 05 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.13.97-1
- 4.13.97

* Mon Jul 14 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.13.3-1
- 4.13.3

* Mon Jun 09 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.13.2-1
- 4.13.2

* Sun Jun 08 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.13.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat May 10 2014 Rex Dieter <rdieter@fedoraproject.org> 4.13.1-1
- 4.13.1

* Sat May 03 2014 Rex Dieter <rdieter@fedoraproject.org> 4.13.0-4
- konqueror: omit dup'd servicemenu bits (in dolphin pkg)

* Sat May 03 2014 Rex Dieter <rdieter@fedoraproject.org> 4.13.0-3
- konqueror: Requires: mozilla-filesystem (#1000673)

* Mon Apr 14 2014 Rex Dieter <rdieter@fedoraproject.org> 4.13.0-2
- BR: kfilemetadata-devel

* Sat Apr 12 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.13.0-1
- 4.13.0

* Fri Apr 04 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.12.97-1
- 4.12.97

* Sat Mar 22 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.12.95-1
- 4.12.95

* Wed Mar 19 2014 Rex Dieter <rdieter@fedoraproject.org> 4.12.90-2
- -devel: Requires: kdelibs4-devel (regression, dep got lost in 4.12 somewhere)

* Tue Mar 18 2014 Rex Dieter <rdieter@fedoraproject.org> 4.12.90-1
- 4.12.90

* Sun Mar 09 2014 Rex Dieter <rdieter@fedoraproject.org> 4.12.3-2
- konqueror: Obsoletes/Provides: konq-plugins

* Sat Mar 01 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.12.3-1
- 4.12.3

* Sat Feb 01 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.12.2-2
- rebase chfn patch, +Requires: util-linux (#609039)

* Fri Jan 31 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.12.2-1
- 4.12.2

* Fri Jan 10 2014 Rex Dieter <rdieter@fedoraproject.org> - 4.12.1-1
- 4.12.1

* Tue Dec 31 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.12.0-3
- dolphin,konqueror: Requires: kdialog

* Sun Dec 29 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.12.0-2
- impliment split packaging
- trim changelog
- License: +GFDL

* Thu Dec 19 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.12.0-1
- 4.12.0

* Sun Dec 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.11.97-1
- 4.11.97

* Thu Nov 21 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.11.95-1
- 4.11.95

* Sat Nov 16 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.11.90-1
- 4.11.90

* Sat Nov 09 2013 Rex Dieter <rdieter@fedoraproject.org> 4.11.3-2
- include some post v4.11.3 commits, including fix for dolphin kde bug #318683

* Sat Nov 02 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.11.3-1
- 4.11.3

* Sat Sep 28 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.11.2-1
- 4.11.2

* Tue Sep 03 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.11.1-1
- 4.11.1

* Thu Aug 08 2013 Than Ngo <than@redhat.com> - 4.11.0-1
- 4.11.0

* Thu Jul 25 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.97-1
- 4.10.97

* Tue Jul 23 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.95-1
- 4.10.95

* Thu Jun 27 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.90-1
- 4.10.90

* Tue Jun 11 2013 Rex Dieter <rdieter@fedoraproject.org> 4.10.4-2
- kcm_useraccount: support accountsservice (#950635)

* Sat Jun 01 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.4-1
- 4.10.4

* Mon May 06 2013 Than Ngo <than@redhat.com> - 4.10.3-1
- 4.10.3

* Mon Apr 29 2013 Than Ngo <than@redhat.com> - 4.10.2-2
- fix multilib issue

* Sun Mar 31 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.2-1
- 4.10.2

* Sat Mar 02 2013 Rex Dieter <rdieter@fedoraproject.org> 4.10.1-1
- 4.10.1

* Thu Jan 31 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.10.0-1
- 4.10.0

* Sun Jan 20 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.9.98-1
- 4.9.98

* Fri Jan 04 2013 Rex Dieter <rdieter@fedoraproject.org> - 4.9.97-1
- 4.9.97

* Thu Dec 20 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.95-1
- 4.9.95

* Thu Dec 13 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9.90-3
- Dolphin cannot start due to symbol lookup error (#886964)

* Mon Dec 03 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9.90-2
- BR: kactivites-devel nepomuk-core-devel

* Mon Dec 03 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9.90-1
- 4.9.90 (4.10 beta2)

* Mon Dec 03 2012 Than Ngo <than@redhat.com> - 4.9.4-1
- 4.9.4

* Thu Nov 29 2012 Dan Vrátil <dvratil@redhat.com> - 4.9.3-2
- Dolphin Solid optimizations

* Sat Nov 03 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.3-1
- 4.9.3

* Tue Oct 16 2012 Than Ngo <than@redhat.com> - 4.9.2-3
- add x-scheme-handler/http for konqueror so it can be set as default browser in GNOME

* Sat Sep 29 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9.2-2
- tarball respin

* Fri Sep 28 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9.2-1
- 4.9.2

* Tue Sep 11 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9.1-2
- Cryptsetup crashes Dolphin on Closing of Loop Devic (#842164,kde#306167)

* Mon Sep 03 2012 Than Ngo <than@redhat.com> - 4.9.1-1
- 4.9.1
- drop references to kdepimlibs

* Thu Jul 26 2012 Lukas Tinkl <ltinkl@redhat.com> - 4.9.0-1
- 4.9.0

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.97-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jul 11 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.97-1
- 4.8.97

* Wed Jun 27 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.95-1
- 4.8.95

* Wed Jun 20 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8.90-2
- Please remove kwrite dependency (#834137)

* Sat Jun 09 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.90-1
- 4.8.90

* Fri Jun 01 2012 Jaroslav Reznik <jreznik@redhat.com> 4.8.80-2
- respin

* Mon May 28 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8.80-1
- 4.8.80

* Mon Apr 30 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.3-1
- 4.8.3
- removed Dolphin timeout patch

* Mon Apr 16 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8.2-2
- dolphin keyboard search timeout improvement (kde#297458, kde#297488)

* Fri Mar 30 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.8.2-1
- 4.8.2

* Mon Mar 05 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.1-1
- 4.8.1

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.0-3
- Rebuilt for c++ ABI breakage

* Wed Jan 25 2012 Than Ngo <than@redhat.com> - 4.8.0-2
- fix kde#292250, make sure that Control+click toggles the selection state

* Fri Jan 20 2012 Jaroslav Reznik <jreznik@redhat.com> - 4.8.0-1
- 4.8.0

* Fri Jan 13 2012 Radek Novacek <rnovacek@redhat.com> 4.7.97-12
- Remove unnecessary BRs

* Fri Jan 13 2012 Rex Dieter <rdieter@fedoraproject.org> 6:4.7.97-11
- %%check: desktop-file-validate
- %%doc COPYING
- fix some errant Provides

* Wed Jan 04 2012 Rex Dieter <rdieter@fedoraproject.org> 6:4.7.97-10
- kdebase => kde-baseapps rename

* Wed Jan 04 2012 Rex Dieter <rdieter@fedoraproject.org> 6:4.7.97-1
- 4.7.97

* Wed Dec 21 2011 Radek Novacek <rnovacek@redhat.com> - 6:4.7.95-1
- 4.7.95

* Sun Dec 04 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.90-1
- 4.7.90
- Build with glib support (#759882)

* Mon Nov 21 2011 Jaroslav Reznik <jreznik@redhat.com> 4.7.80-1
- 4.7.80 (beta 1)
- fix conditional for kwebkitpart

* Sat Oct 29 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.3-1
- 4.7.3
- pkgconfig-style deps
- more kde-baseapps Provides

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6:4.7.2-3
- Rebuilt for glibc bug#747377

* Sat Oct 08 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.2-2
- rebase folderview/rename patch (kde#270414)

* Tue Oct 04 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7.2-1
- 4.7.2

* Wed Sep 21 2011 Rex Dieter <rdieter@fedoraproject.org> 6:4.7.1-2
- Rename any file using folderview causes an error message (kde#270414)

* Fri Sep 02 2011 Than Ngo <than@redhat.com> - 6:4.7.1-1
- 4.7.1

* Tue Jul 26 2011 Jaroslav Reznik <jreznik@redhat.com> 6:4.7.0-1
- 4.7.0

* Fri Jul 22 2011 Rex Dieter <rdieter@fedoraproject.org> 6:4.6.95-11
- Requires: konsole kwrite, for upgrade path 

* Thu Jul 21 2011 Rex Dieter <rdieter@fedoraproject.org> 6:4.6.95-10
- drop kate, konsole, to be packaged separately.
- update summary to mention included apps/utilities
- Provides: kde-baseapps (matching new upstream tarball)

* Mon Jul 18 2011 Rex Dieter <rdieter@fedoraproject.org> 6:4.6.95-2
- Provides: konqueror, konsole

* Fri Jul 08 2011 Jaroslav Reznik <jreznik@redhat.com> - 6:4.6.95-1
- 4.6.95 (rc2)

* Mon Jun 27 2011 Than Ngo <than@redhat.com> - 6:4.6.90-1
- 4.6.90 (rc1)

* Wed Jun 01 2011 Radek Novacek <rnovacek@redhat.com> 6:4.6.80-1
- 4.6.80
- import separately packaged kwrite and konsole
- drop upstreamed patches (nsplugins_sdk_headers and nsplugins_flash)
- add konq-plugins

* Mon May 23 2011 Rex Dieter <rdieter@fedoraproject.org> 6:4.6.3-2
- nspluginviewer crashes with flash-plugin 10.3 (kde#273323)

* Thu Apr 28 2011 Rex Dieter <rdieter@fedoraproject.org> 6:4.6.3-1
- 4.6.3

* Wed Apr 06 2011 Than Ngo <than@redhat.com> - 6:4.6.2-1
- 4.6.2

* Sun Mar 06 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 6:4.6.1-3
- fix Dolphin regression

* Thu Mar 03 2011 Rex Dieter <rdieter@fedoraproject.org> 6:4.6.1-2
- respin tarball

* Mon Feb 28 2011 Rex Dieter <rdieter@fedoraproject.org> 6:4.6.1-1
- 4.6.1

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6:4.6.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Jan 21 2011 Jaroslav Reznik <jreznik@redhat.com> 6:4.6.0-1
- 4.6.0

* Wed Jan 05 2011 Jaroslav Reznik <jreznik@redhat.com> 6:4.5.95-1
- 4.5.95 (4.6rc2)

* Wed Dec 22 2010 Rex Dieter <rdieter@fedoraproject.org> 6:4.5.90-1
- 4.5.90 (4.6rc1)

* Sat Dec 04 2010 Thomas Janssen <thomasj@fedoraproject.org> 6:4.5.85-1
- 4.5.85 (4.6beta2)

* Mon Nov 22 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.5.80-2
- drop extraneous BR's

* Sat Nov 20 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.5.80-1
- 4.5.80 (4.6beta1)

* Fri Oct 29 2010 Than Ngo <than@redhat.com> - 6:4.5.3-1
- 4.5.3

* Wed Oct 13 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.5.2-2
- FolderView keeps sorting icons (kde#227157)

* Fri Oct 01 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.5.2-1
- 4.5.2

* Thu Sep 30 2010 Than Ngo <than@redhat.com> - 6:4.5.1-4
- Password & User account becomes non responding

* Wed Sep 29 2010 jkeating - 6:4.5.1-3
- Rebuilt for gcc bug 634757

* Mon Sep 20 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.5.1-2
- konsole minimum tab width is too wide (#632217, kde#166573)

* Fri Aug 27 2010 Jaroslav Reznik <jreznik@redhat.com> - 6:4.5.1-1
- 4.5.1

* Tue Aug 03 2010 Than Ngo <than@redhat.com> - 6:4.5.0-1
- 4.5.0

* Sun Jul 25 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.4.95-1
- 4.5 RC3 (4.4.95)

* Wed Jul 07 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.4.92-1
- 4.5 RC2 (4.4.92)

* Tue Jul 06 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.4.90-2
- update %%summary/%%description
- tighten deps

* Fri Jun 25 2010 Jaroslav Reznik <jreznik@redhat.com> - 6:4.4.90-1
- 4.5 RC1 (4.4.90)

* Mon Jun 07 2010 Jaroslav Reznik <jreznik@redhat.com> - 6:4.4.85-1
- 4.5 Beta 2 (4.4.85)

* Fri May 21 2010 Jaroslav Reznik <jreznik@redhat.com> - 6:4.4.80-1
- 4.5 Beta 1 (4.4.80)

* Sat May 01 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 6:4.4.3-2
- completely drop commented out konsole-session patch (fixed upstream)
- add backwards compatibility hack for a config option change by that patch

* Fri Apr 30 2010 Jaroslav Reznik <jreznik@redhat.com> - 6:4.4.3-1
- 4.4.3

* Mon Mar 29 2010 Lukas Tinkl <ltinkl@redhat.com> - 6:4.4.2-1
- 4.4.2

* Mon Mar 15 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.4.1-2
- drop kappfinder (keep option for -kappfinder subpkg)
- use whitelist for conflicting libs
- libs: Requires: %%name

* Sat Feb 27 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.4.1-1
- 4.4.1

* Fri Feb 26 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 6:4.4.0-5
- fix disabling automatic spell checking in the Konqueror UI (kde#228593)

* Thu Feb 25 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 6:4.4.0-4
- backport fix for folderview getting resorted on file creation (kde#227157)

* Wed Feb 10 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 6:4.4.0-3
- BR webkitpart-devel >= 0.0.5

* Wed Feb 10 2010 Rex Dieter <rdieter@fedoraproject.org> - 6:4.4.0-2
- disable webkitpart support (until upstream naming/api stabilizes)

* Fri Feb 05 2010 Than Ngo <than@redhat.com> - 6:4.4.0-1
- 4.4.0

* Mon Feb 01 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.3.98-2
- remove extra spaces from konsole selections (#560721)

* Sun Jan 31 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.3.98-1
- KDE 4.3.98 (4.4rc3)

* Wed Jan 20 2010 Lukas Tinkl <ltinkl@redhat.com> - 4.3.95-1
- KDE 4.3.95 (4.4rc2)

* Wed Jan 06 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.3.90-1
- kde-4.3.90 (4.4rc1)

* Fri Dec 18 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.85-1
- kde-4.3.85 (4.4beta2)

* Wed Dec 16 2009 Jaroslav Reznik <jreznik@redhat.com> - 4.3.80-4
- Repositioning the KDE Brand (#547361)

* Wed Dec 09 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.3.80-3
- rebuild against Nepomuk-enabled kdelibs

* Wed Dec 09 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.80-2
- BR: shared-desktop-ontologies-devel

* Tue Dec 01 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.3.80-1
- KDE 4.4 beta1 (4.3.80)

* Tue Nov 24 2009 Ben Boeckel <MathStuf@gmail.com> - 4.3.75-0.2.svn1048496
- Fix webkitkde version requirement

* Sun Nov 22 2009 Ben Boeckel <MathStuf@gmail.com> - 4.3.75-0.1.svn1048496
- Update to 4.3.75 snapshot

* Thu Nov 19 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.3-4
- rebuild (for qt-4.6.0-rc1, f13+)

* Wed Nov 11 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.3.3-3
- allow 'Open Folder in Tabs' in Konsole to support SSH bookmarks (kde#177637)
  (upstream patch backported from 4.4)

* Mon Nov 09 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.3-2
- BR: webkitpart-devel >= 0.0.2

* Sat Oct 31 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.3-1
- 4.3.3

* Fri Oct 09 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.3.2-3
- backport upstream patch for bookmark editor drag&drop crash (kde#160679)

* Wed Oct 07 2009 Than Ngo <than@redhat.com> - 4.3.2-2
- fix Dolphin crash (regression)

* Sun Oct 04 2009 Than Ngo <than@redhat.com> - 4.3.2-1
- 4.3.2

* Sun Sep 27 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-4
- BR: webkitpart-devel
- fix Provides: kdebase4%%{?_isa} (not kdelibs)

* Sun Sep 27 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3.1-3
- own %%_kde4_appsdir/konqueror/{kpartplugins,icons,opensearch}
- %%lang'ify HTML docs
- Provides: kdelibs4%%{?_isa} 

* Wed Sep  2 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.3.1-2
- fix context menus in Konsole (kdebug:186745)

* Fri Aug 28 2009 Than Ngo <than@redhat.com> - 4.3.1-1
- 4.3.1
- drop/revert kde-plasma-folderview subpkg

* Tue Aug 25 2009 Rex Dieter <rdieter@fedoraproject.org> 4.3.0-2
- kde-plasma-folderview subpkg
- %%?_isa'ify -libs deps

* Thu Jul 30 2009 Than Ngo <than@redhat.com> - 4.3.0-1
- 4.3.0

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6:4.2.98-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Jul 21 2009 Than Ngo <than@redhat.com> - 4.2.98-1
- 4.3rc3

* Thu Jul 09 2009 Than Ngo <than@redhat.com> - 4.2.96-1
- 4.3rc2

* Thu Jun 25 2009 Than Ngo <than@redhat.com> - 4.2.95-1
- 4.3rc1

* Wed Jun 03 2009 Rex Dieter <rdieter@fedoraproject.org> - 6:4.2.90-1
- KDE-4.3 beta2 (4.2.90)

* Tue Jun 02 2009 Lorenzo Villani <lvillani@binaryhelix.net> - 6:4.2.85-2
- Fedora 8 is EOL'ed, drop conditionals and cleanup the specfile

* Wed May 13 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.85-1
- KDE 4.3 beta 1

* Tue Apr 21 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.2-3
- #496447 -  fix disabling konsole's flow control

* Wed Apr 01 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.2-2
- optimize scriptlets

* Mon Mar 30 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.2-1
- KDE 4.2.2

* Mon Mar 09 2009 Than Ngo <than@redhat.com> - 4.2.1-3
- apply patch to fix regression in konsole, layout regression affecting apps
  using the KPart

* Wed Mar 04 2009 Than Ngo <than@redhat.com> - 4.2.1-2
- apply patch to fix regression in konsole, double-click selection works again

* Fri Feb 27 2009 Than Ngo <than@redhat.com> - 4.2.1-1
- 4.2.1

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 6:4.2.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Feb 16 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.0-6
- unbreak apps like vim or mc under Konsole

* Thu Feb 12 2009 Rex Dieter <rdieter@fedorparoject.org> - 4.2.0-5
- avoid_kde3_services patch
- fix home-icon patch

* Thu Feb 12 2009 Lukáš Tinkl <ltinkl@redhat.com> - 4.2.0-4
- add Home icon to the Applications menu by default (#457756)

* Wed Feb 11 2009 Than Ngo <than@redhat.com> - 4.2.0-3
- apply patch to make dolphin working well with 4.5

* Wed Jan 28 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2.0-2
- KDEInit could not launch '/usr/bin/konsole' (kdebug#162729)

* Thu Jan 22 2009 Than Ngo <than@redhat.com> - 4.2.0-1
- 4.2.0

* Wed Jan 07 2009 Than Ngo <than@redhat.com> - 4.1.96-1
- 4.2rc1

* Thu Dec 11 2008 Than Ngo <than@redhat.com> -  4.1.85-1
- 4.2beta2

* Thu Nov 27 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 6:4.1.80-4
- BR plasma-devel instead of kdebase-workspace-devel

* Sun Nov 23 2008 Lorenzo Villani <lvillani@binaryhelix.net> - 6:4.1.80-3
- rebase nsplugins-path patch

* Thu Nov 20 2008 Than Ngo <than@redhat.com>  4.1.80-2
- merged

* Wed Nov 19 2008 Lorenzo Villani <lvillani@binaryhelix.net> - 6:4.1.80-1
- 4.1.80
- patch100 was backported from 4.2 (4.1.6x), removed from patch list
- ported 4.1.2 konsole patches
- drop the second konsole patch (upstreamed)
- using make install/fast
- BR cmake >= 2.6.2

* Wed Nov 12 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.3-2
- readd kde#156636 patch (Konsole keyboard actions backport)

* Tue Nov  4 2008 Lukáš Tinkl <ltinkl@redhat.com> 4.1.3-1
- KDE 4.1.3

* Thu Oct 16 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.2-5
- backport kbd actions for switching to Nth tab in Konsole from 4.2 (kde#156636)

* Mon Oct 06 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.2-4
- updated konsole session management patch from Stefan Becker

* Mon Oct 06 2008 Than Ngo <than@redhat.com> 4.1.2-3
- bz#465451, backport konsole session management, thanks to Stefan Becker

* Mon Sep 29 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-2
- make VERBOSE=1
- respin against new(er) kde-filesystem

* Fri Sep 26 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1.2-1
- 4.1.2

* Thu Sep 18 2008 Than Ngo <than@redhat.com> 4.1.1-2
- make bookmark silent

* Fri Aug 29 2008 Than Ngo <than@redhat.com> 4.1.1-1
- 4.1.1

* Fri Jul 25 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1.0-1.1
- always check for Plasma actually being present (fixes F8 kdebase4 build)

* Wed Jul 23 2008 Than Ngo <than@redhat.com> 4.1.0-1
- 4.1.0

* Tue Jul 22 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.99-2
 respin (libraw1394)

* Fri Jul 18 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.99-1
- 4.0.99

* Fri Jul 11 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.98-2
- BR: pciutils-devel

* Thu Jul 10 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.98-1
- 4.0.98

* Sun Jul 06 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.85-1
- 4.0.85

* Fri Jun 27 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.84-1
- 4.0.84

* Tue Jun 24 2008 Lukáš Tinkl <ltinkl@redhat.com> - 4.0.83-2
- #426108: Add more directories to konqueror's default
  plugin search path list

* Thu Jun 19 2008 Than Ngo <than@redhat.com> 4.0.83-1
- 4.0.83 (beta2)

* Mon Jun 16 2008 Than Ngo <than@redhat.com> 4.0.82-2
- BR kdebase-workspace-devel (F9+)

* Sun Jun 15 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.82-1
- 4.0.82

* Tue May 27 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.80-3
- respun tarball from upstream

* Tue May 27 2008 Than Ngo <than@redhat.com> 4.0.80-2
- rebuild to fix undefined symbol issue in dolphin

* Mon May 26 2008 Than Ngo <than@redhat.com> 4.0.80-1
- 4.1 beta1

* Sun May 11 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.72-2
- quote semicolon in fix for #442834
- only do the echo when konquerorsu.desktop is actually shipped (#445989)

* Tue May 06 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.72-1
- update to 4.0.72 (4.1 alpha 1)
- drop backported kde#160422 and nspluginviewer patches
- add minimum versions to soprano-devel and strigi-devel BRs

* Fri Apr 18 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.3-9
- kwrite.desktop: Categories += Utility (#438786)

* Thu Apr 17 2008 Than Ngo <than@redhat.com> 4.0.3-8
- konquerorsu only show in KDE, #442834

* Mon Apr 14 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.3-7
- nspluginviewer patch (kde#160413)

* Sun Apr 06 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.3-6
- backport Konsole window size fixes from 4.1 (#439638, kde#160422)

* Thu Apr 03 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.3-5
- rebuild (again) for the fixed %%{_kde4_buildtype}

* Mon Mar 31 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.3-4
- add missing BR libraw1394-devel (thanks to Karsten Hopp)
- don't BR libusb-devel on s390 or s390x

* Mon Mar 31 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.3-3
- rebuild for NDEBUG and _kde4_libexecdir

* Fri Mar 28 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.3-2
- add Requires: kdebase-runtime oxygen-icon-theme (#438632)

* Fri Mar 28 2008 Than Ngo <than@redhat.com> 4.0.3-1
- 4.0.3
- drop fix for favicons infinite loop, it's included in new version
- omit multilib upgrade hacks
- omit extraneous BR's
- (re)include oxgygen/scalable icons

* Fri Feb 29 2008 Lukáš Tinkl <ltinkl@redhat.com> 4.0.2-2
- fix favicons infinite loop

* Thu Feb 28 2008 Than Ngo <than@redhat.com> 4.0.2-1
- 4.0.2

* Mon Feb 18 2008 Than Ngo <than@redhat.com> 4.0.1-4
- fix nsplugins hangs during login

* Mon Feb 04 2008 Than Ngo <than@redhat.com> 4.0.1-3
- respin

* Fri Feb 01 2008 Than Ngo <than@redhat.com> 4.0.1-2
- add flash fix from stable svn branch

* Thu Jan 31 2008 Than Ngo <than@redhat.com> 4.0.1-1
- 4.0.1

* Wed Jan 30 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0.0-3
- resurrect -libs (f9+)
- improve %%description

* Sat Jan 19 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0.0-2.1
- Obsoletes: dolphin, d3lphin, Provides: dolphin everywhere

* Tue Jan 08 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 4.0.0-2
- respun tarball

* Mon Jan 07 2008 Than Ngo <than@redhat.com> 4.0.0-1
- 4.0.0
