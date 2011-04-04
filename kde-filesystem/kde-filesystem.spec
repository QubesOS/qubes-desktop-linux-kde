
%define _kde4_prefix %_prefix
%define _kde4_sysconfdir %_sysconfdir
%define _kde4_libdir %_libdir
%define _kde4_libexecdir %_libexecdir/kde4
%define _kde4_datadir %_datadir
%define _kde4_sharedir %_datadir
%define _kde4_iconsdir %_kde4_sharedir/icons
%define _kde4_configdir %_kde4_sharedir/config
%define _kde4_appsdir %_kde4_sharedir/kde4/apps
%define _kde4_docdir %_kde4_prefix/share/doc
%define _kde4_bindir %_kde4_prefix/bin
%define _kde4_sbindir %_kde4_prefix/sbin
%define _kde4_includedir %_kde4_prefix/include/kde4
%define _kde4_buildtype release
%define _kde4_macros_api 2

%define exclude_sounds 1

Summary: KDE filesystem layout
Name: kde-filesystem
Version: %{version}
Release: %{rel}.qubes
Epoch:   1000

License: Public Domain
BuildArch: noarch

# teamnames (locales) borrowed from kde-i18n packaging
Source1: teamnames

Source2: macros.kde4
# increment whenever dirs change in an incompatible way
# kde4 apps built using macros.kde4 should

Provides: kde4-macros(api) = %{_kde4_macros_api} 
Provides: kde-filesystem-dom0

BuildRequires: gawk

Requires:  filesystem
Requires:  rpm

%description
This package provides some directories that are required/used by KDE in Qubes Dom0. 

%prep

%build

%install
rm -f $RPM_BUILD_DIR/%{name}.list
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/rpm \
      -p $RPM_BUILD_ROOT%{_kde4_sysconfdir}/kde/env \
      -p $RPM_BUILD_ROOT%{_kde4_sysconfdir}/kde/shutdown \
      -p $RPM_BUILD_ROOT%{_kde4_sysconfdir}/kde/kdm \
      -p $RPM_BUILD_ROOT%{_kde4_includedir} \
      -p $RPM_BUILD_ROOT%{_kde4_libexecdir} \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/applications/kde4 \
      -p $RPM_BUILD_ROOT%{_kde4_appsdir} \
      -p $RPM_BUILD_ROOT%{_kde4_appsdir}/color-schemes \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/autostart \
      -p $RPM_BUILD_ROOT%{_kde4_configdir} \
      -p $RPM_BUILD_ROOT%{_kde4_sharedir}/config.kcfg \
      -p $RPM_BUILD_ROOT%{_kde4_sharedir}/emoticons \
      -p $RPM_BUILD_ROOT%{_kde4_sharedir}/kde4/services/ServiceMenus \
      -p $RPM_BUILD_ROOT%{_kde4_sharedir}/kde4/servicetypes \
      -p $RPM_BUILD_ROOT%{_kde4_sharedir}/templates/.source \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/icons/locolor/16x16/actions \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/icons/locolor/16x16/apps \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/icons/locolor/16x16/mimetypes \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/icons/locolor/22x22/actions \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/icons/locolor/22x22/apps \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/icons/locolor/22x22/mimetypes \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/icons/locolor/32x32/actions \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/icons/locolor/32x32/apps \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/icons/locolor/32x32/mimetypes \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/icons/locolor/48x48/actions \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/icons/locolor/48x48/apps \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/icons/locolor/48x48/mimetypes \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/sounds \
      -p $RPM_BUILD_ROOT%{_kde4_datadir}/wallpapers \
      -p $RPM_BUILD_ROOT%{_kde4_docdir}/HTML/en/common

for locale in $(grep '=' %{SOURCE1} | awk -F= '{print $1}') ; do
  mkdir -p $RPM_BUILD_ROOT%{_kde4_docdir}/HTML/${locale}/common
  echo "%lang($locale) %{_kde4_docdir}/HTML/$locale/" >> %{name}.list
done

# rpm macros
cat >$RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.kde4<<EOF
%%_kde4_prefix %%_prefix
%%_kde4_sysconfdir %%_sysconfdir
%%_kde4_libdir %%_libdir
%%_kde4_libexecdir %%_libexecdir/kde4
%%_kde4_datadir %%_datadir
%%_kde4_sharedir %%_datadir
%%_kde4_iconsdir %%_kde4_sharedir/icons
%%_kde4_configdir %%_kde4_sharedir/config
%%_kde4_appsdir %%_kde4_sharedir/kde4/apps
%%_kde4_docdir %_kde4_prefix/share/doc
%%_kde4_bindir %%_kde4_prefix/bin
%%_kde4_sbindir %%_kde4_prefix/sbin
%%_kde4_includedir %%_kde4_prefix/include/kde4
%%_kde4_buildtype %_kde4_buildtype
%%_kde4_macros_api %_kde4_macros_api
EOF
cat %{SOURCE2} >> $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.kde4


%clean
rm -rf $RPM_BUILD_ROOT %{name}.list


%files -f %{name}.list
%defattr(-,root,root,-)

# KDE4
%config /etc/rpm/macros.kde4
%{_kde4_sysconfdir}/kde/
%{_kde4_libexecdir}/
%{_kde4_includedir}/
%{_kde4_datadir}/applications/kde4/
%{_kde4_appsdir}/
%{_kde4_configdir}/
%{_kde4_sharedir}/config.kcfg/
%{_kde4_sharedir}/emoticons/
%{_kde4_sharedir}/kde4/
%{_kde4_sharedir}/templates/
%{_kde4_datadir}/autostart/
%{_kde4_datadir}/icons/locolor
%{?exclude_sounds:%exclude }%{_kde4_datadir}/sounds/
%{_kde4_datadir}/wallpapers/
%dir %{_kde4_docdir}/HTML/
%lang(en) %{_kde4_docdir}/HTML/en/


%changelog
* Mon May 24 2010 Joanna Rutkowska <joanna@invisiblethingslab.com>
- spec file adapted to Qubes OS (based on Fedora spec) 4.4.3-1
- based on the original spec from Fedora 12

