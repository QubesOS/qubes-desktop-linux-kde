# THIS SPECFILE IS FOR F18 ONLY!
%if 0%{?qubes_builder}
%define _sourcedir %(pwd)/kde-settings
%define kde_settings_epoch %(cat epoch)
%else
%define kde_settings_epoch 0
%endif
%{!?epoch: %define epoch %(cat epoch)}

%global rel 19
%global system_kde_theme_ver 17.91

Summary: Config files for kde
Name:    kde-settings
Epoch:   %{kde_settings_epoch}
Version: 4.9
Release: %{rel}.7%{?dist}

License: MIT
Url:     http://fedorahosted.org/kde-settings
Source0: https://fedorahosted.org/releases/k/d/kde-settings/%{name}-%{version}-%{rel}.tar.xz
Source1: COPYING
Source100: 10-qubes.js
Source101: qubes-systray.js
BuildArch: noarch

BuildRequires: kde-filesystem
BuildRequires: systemd

Requires: kde-filesystem
# /etc/pam.d/ ownership
Requires: pam
Requires: xdg-user-dirs
Requires: adwaita-cursor-theme
# /usr/share/polkit-1/rules.d/ ownership
Requires: polkit >= 0.106
Requires: qubes-artwork

Requires(post): coreutils sed

###############################################################
# Qubes Patches:
Patch100: kde-settings-4.9-plastik-for-qubes.patch
Patch101: qubes-menus-prefix.patch
Patch102: kdm-settings.patch
Patch103: disable-nepomuk.patch
Patch104: hide-knetattach.patch
Patch105: disable-klipper.patch
Patch106: hide-kde-help.patch
Patch107: kdm-disable-switch-user.patch
###############################################################

%description
%{summary}.

%package minimal
Summary: Minimal configuration files for KDE
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: kde-workspace-ksplash-themes
Requires: xorg-x11-xinit
%description minimal
%{summary}.

%package kdm
Summary: Configuration files for kdm
# MinShowUID=-1 is only supported from 4.7.1-2 on
Requires: kdm >= 4.7.1-2
Requires: kdm-themes

Requires: xorg-x11-xinit
Requires(pre): coreutils
Requires(post): coreutils grep sed
Requires(post): kde4-macros(api) = %{_kde4_macros_api}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%description kdm
%{summary}.

%package ksplash
Summary: Configuration files for ksplash
Requires: %{name} = %{epoch}:%{version}-%{release}
%description ksplash 
%{summary}.

%package plasma
Summary: Configuration files for plasma 
Requires: %{name} = %{epoch}:%{version}-%{release}
%description plasma 
%{summary}.

%package pulseaudio
Summary: Enable pulseaudio support in KDE
# nothing here to license
License: Public Domain
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: pulseaudio
Requires: pulseaudio-module-x11
## kde3
Requires: alsa-plugins-pulseaudio
## kde4: -pulseaudio plugins are installed for all phonon backends by default
%description pulseaudio
%{summary}.

%package -n qt-settings
Summary: Configuration files for Qt 
# qt-graphicssystem.* scripts use lspci
Requires: pciutils
%description -n qt-settings
%{summary}.


%prep
%setup -q -n %{name}-%{version}-%{rel}

%patch100 -p1
%patch101 -p1
%patch102 -p1
%patch103 -p1
%patch104 -p1
%patch105 -p1
%patch106 -p1
%patch107 -p1

%build
# Intentionally left blank.  Nothing to see here.


%install
mkdir -p %{buildroot}{%{_datadir}/config,%{_sysconfdir}/kde/kdm}

tar cpf - . | tar --directory %{buildroot} -xvpf -

cp -p %{SOURCE1} .

# kdebase/kdm symlink
rm -rf   %{buildroot}%{_datadir}/config/kdm
ln -sf ../../../etc/kde/kdm %{buildroot}%{_datadir}/config/kdm

# own these
mkdir -p %{buildroot}%{_localstatedir}/lib/kdm
mkdir -p %{buildroot}%{_localstatedir}/run/{kdm,xdmctl}

# Remove Fedora branding
rm -f %{buildroot}%{_datadir}/kde-settings/kde-profile/default/share/apps/plasma-desktop/updates/00-start-here-kde-fedora-2.js
rm -f %{buildroot}%{_datadir}/kde-settings/kde-profile/default/share/config/plasmarc
rm -f %{buildroot}%{_datadir}/kde-settings/kde-profile/default/share/config/ksplashrc

# Qubes defaults
install -m 644 %{SOURCE100} %{buildroot}%{_datadir}/kde-settings/kde-profile/default/share/apps/plasma-desktop/init/
install -m 644 %{SOURCE101} %{buildroot}%{_datadir}/kde-settings/kde-profile/default/share/apps/plasma-desktop/init/

%files 
%doc COPYING
%config(noreplace) %{_sysconfdir}/profile.d/kde.*
%{_sysconfdir}/kde/env/env.sh
%{_sysconfdir}/kde/env/gtk2_rc_files.sh
%{_sysconfdir}/kde/env/fedora-kde-display-handler.sh
%if 0%{?fedora}
%{_sysconfdir}/kde/env/fedora-bookmarks.sh
%{_datadir}/kde-settings/
%{_prefix}/lib/rpm/plasma4.prov
%{_prefix}/lib/rpm/plasma4.req
%{_prefix}/lib/rpm/fileattrs/plasma4.attr
%{_datadir}/polkit-1/rules.d/11-fedora-kde-policy.rules
%endif
%config(noreplace) /etc/pam.d/kcheckpass
%config(noreplace) /etc/pam.d/kscreensaver
# drop noreplace, so we can be sure to get the new kiosk bits
%config %{_sysconfdir}/kderc
%config %{_sysconfdir}/kde4rc
%dir %{_datadir}/kde-settings/
%dir %{_datadir}/kde-settings/kde-profile/
%{_datadir}/kde-settings/kde-profile/default/

%files minimal
%{_datadir}/kde-settings/kde-profile/minimal/
%{_sysconfdir}/X11/xinit/xinitrc.d/20-kdedirs-minimal.sh

%post kdm
%systemd_post kdm.service
(grep '^UserAuthDir=/var/run/kdm$' %{_sysconfdir}/kde/kdm/kdmrc > /dev/null && \
 sed -i.rpmsave -e 's|^UserAuthDir=/var/run/kdm$|#UserAuthDir=/tmp|' \
 %{_sysconfdir}/kde/kdm/kdmrc
) ||:

%preun kdm
%systemd_preun kdm.service

%postun kdm
%systemd_postun

%files kdm
%doc COPYING
%config(noreplace) /etc/pam.d/kdm*
# compat symlink
%{_datadir}/config/kdm
%dir %{_sysconfdir}/kde/kdm
%config(noreplace) %{_sysconfdir}/kde/kdm/kdmrc
%dir %{_localstatedir}/lib/kdm
%config(noreplace) %{_localstatedir}/lib/kdm/backgroundrc
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/kde/kdm/README*
%config(noreplace) %{_sysconfdir}/kde/kdm/Xaccess
%config(noreplace) %{_sysconfdir}/kde/kdm/Xresources
%config(noreplace) %{_sysconfdir}/kde/kdm/Xsession
%config(noreplace) %{_sysconfdir}/kde/kdm/Xsetup
%config(noreplace) %{_sysconfdir}/kde/kdm/Xwilling
# own logrotate.d/ avoiding hard dep on logrotate
%dir %{_sysconfdir}/logrotate.d
%config(noreplace) %{_sysconfdir}/logrotate.d/kdm
%{_prefix}/lib/tmpfiles.d/kdm.conf
%attr(0711,root,root) %dir %{_localstatedir}/run/kdm
%attr(0711,root,root) %dir %{_localstatedir}/run/xdmctl
%{_unitdir}/kdm.service
%{_unitdir}-preset/81-fedora-kdm.preset

%files ksplash

%files plasma

%files pulseaudio
# nothing, this is a metapackage

%files -n qt-settings
%doc COPYING
%config(noreplace) %{_sysconfdir}/Trolltech.conf
%config(noreplace) %{_sysconfdir}/profile.d/qt-graphicssystem.*


%changelog
* Sat Feb 09 2013 Marek Marczykowski <marmarek@invisiblethingslab.com>
- adopt for Qubes OS

* Tue Jan 29 2013 Dan Vrátil <dvratil@redhat.com> 4.9-19
- use return instead of exit in fedora-kde-display-handler.sh (#905371)

* Mon Jan 28 2013 Rex Dieter <rdieter@fedoraproject.org> 4.9-18
- +fedora-kde-display-handler.sh

* Tue Dec 04 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9-17
- plasma4.req: allow for > 1 scriptengine

* Tue Nov 27 2012 Dan Vratil <dvratil@redhat.com> 4.9-16
- provide kwin rules to fix maximization of some Gtk2 apps

* Sat Nov 10 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9-15.1
- fixup kdmrc for upgrader's who had UserAuthDir=/var/run/kdm

* Thu Nov 08 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9-15
- tighten permissions on /var/run/kdm (#830433)
- support /var/run/xdmctl

* Fri Oct 12 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.9-14
- kslideshow.kssrc: use xdg-user-dir instead of hardcoding $HOME/Pictures

* Fri Oct 12 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.9-13
- port 11-fedora-kde-policy from old pkla format to new polkit-1 rules (#829881)
- nepomukstrigirc: index translated xdg-user-dirs (dvratil, #861129)

* Thu Sep 27 2012 Dan Vratil <dvratil@redhat.com> 4.9-11
- fix indexing paths in nepomukstrigirc (#861129)

* Mon Sep 24 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9-10
- -minimal subpkg

* Tue Sep 04 2012 Dan Vratil <dvratil@redhat.com> 4.9-9
- start kdm.service after livesys-late.service

* Wed Aug 29 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9-8
- add 81-fedora-kdm.preset (#852844)

* Wed Aug 29 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9-7
- kdm.pam: pam_gnome_keyring.so should be loaded after pam_systemd.so (#852723)

* Tue Aug 21 2012 Martin Briza <mbriza@redhat.com> 4.9-5
- Change strings to Fedora 18 (Spherical Cow)
- bump system_kde_theme_ver to 17.91

* Sat Aug 11 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9-2.1
- -kdm: drop old stuff, fix systemd scriptlets

* Thu Aug 09 2012 Rex Dieter <rdieter@fedoraproject.org> 4.9-2
- /etc/pam.d/kdm missing: -session optional pam_ck_connector.so (#847114)

* Wed Aug 08 2012 Rex Dieter <rdieter@fedoraproject.org> - 4.9-1
- adapt kdm for display manager rework feature (#846145)

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8-16.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 29 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8-16
- qt-graphicssystem.csh: fix typo s|/usr/bin/lspci|/usr/sbin/lspci| (#827440)

* Wed Jun 13 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8-15.1
- kde-settings-kdm conflicts with gdm (#819254)

* Wed Jun 13 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8-15
- qt-settings does NOT fully quallify path to lspci in /etc/profile.d/qt-graphicssystem.{csh,sh} (#827440)

* Fri May 25 2012 Than Ngo <than@redhat.com> - 4.8-14.1
- rhel/fedora condtion

* Wed May 16 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8-14
- Pure Qt applications can't use KDE styles outside of KDE (#821062)

* Tue May 15 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8-13
- kdmrc: GUIStyle=Plastique (#810161)

* Mon May 14 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8-12
- drop hack/workaround for bug #750423
- move /etc/tmpfiles.d => /usr/lib/tmpfiles.d

* Thu May 10 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8-10
- +qt-settings: move cirrus workaround(s) here (#810161)

* Wed May 09 2012 Than Ngo <than@redhat.com> - 4.8-8.2
- fix rhel condition

* Tue May 08 2012 Than Ngo <than@redhat.com> - 4.8-8.1
- add workaround for cirrus

* Mon Apr 30 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8-8
- fix application/x-rpm mimetype defaults

* Wed Apr 18 2012 Than Ngo <than@redhat.com> - 4.8-7.1
- add rhel condition

* Mon Mar 19 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.8-7
- plasma4.prov: change spaces in runner names to underscores

* Tue Feb 28 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8-6
- kslideshow.kssrc: include some sane/working defaults

* Tue Feb 14 2012 Jaroslav Reznik <jreznik@redhat.com> 4.8-5
- fix plasmarc Beefy Miracle reference

* Tue Feb 14 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.8-4
- kdmrc: GreetString=Fedora 17 (Beefy Miracle)
- kdmrc, ksplashrc, plasmarc: s/Verne/BeefyMiracle/g (for the artwork themes)
- bump system_kde_theme_ver to 16.91

* Mon Jan 16 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.8-3
- merge the plasma-rpm tarball into the SVN trunk and thus the main tarball

* Mon Jan 16 2012 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.8-2
- allow org.kde.kcontrol.kcmclock.save without password for wheel again
- Requires: polkit (instead of polkit-desktop-policy)

* Mon Jan 16 2012 Rex Dieter <rdieter@fedoraproject.org> 4.8-1
- kwinrc: drop [Compositing] Enabled=false

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7-14.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Nov 19 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7-14
- add explicit apper defaults
- add script to init $XDG_DATA_HOME (to workaround bug #750423)

* Mon Oct 31 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7-13.4
- make new-subpkgs Requires: %%name for added safety

* Mon Oct 31 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7-13.3
- -ksplash: Requires: system-ksplash-theme >= 15.90
- -plasma: Requires: system-plasma-desktoptheme >= 15.90

* Mon Oct 31 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7-13.2
- -kdm: Requires: system-kdm-theme >= 15.90

* Mon Oct 31 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7-13.1
- -kdm: Requires: verne-kdm-theme (#651305) 

* Fri Oct 21 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7-13
- s/kpackagekit/apper/ configs
- drop gpg-agent scripts (autostarts on demand now)

* Sat Oct 15 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7-12
- disable the default Plasma digital-clock's displayEvents option by default

* Wed Oct 12 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7-11
- krunnerrc: org.kde.events_runnerEnabled=false
- follow Packaging:Tmpfiles.d guildelines

* Wed Oct 05 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7-10
- don't spam syslog if pam-gnome-keyring is not present (#743044)

* Fri Sep 30 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7-9
- -kdm: add explicit Requires: xorg-x11-xinit

* Tue Sep 27 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7-8
- plasma4.prov: don't trust the Name of script engines, always use the API

* Thu Sep 22 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7-7
- ship the Plasma RPM dependency generators only on F17+
- use xz tarball
- don't rm Makefile, no longer in the tarball
- set up a folder view on the desktop by default for new users (#740676)
- kdmrc: set MinShowUID=-1 (use /etc/login.defs) instead of 500 (#717115)
- -kdm: Requires: kdm >= 4.7.1-2 (required for MinShowUID=-1)

* Wed Aug 31 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7-6
- put under the MIT license as agreed with the other contributors

* Sun Aug 21 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7-5
- fix the RPM dependency generators to also accept ServiceTypes= (#732271)

* Sun Aug 21 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.7-4
- add the RPM dependency generators for Plasma (GSoC 2011), as Source1 for now

* Tue Aug 02 2011 Jaroslav Reznik <jreznik@redhat.com> 4.7-3
- update to Verne theming/branding

* Wed Jul 13 2011 Rex Dieter <rdieter@fedoraproject.org> 4.7-2
- kmixrc: [Global] startkdeRestore=false

* Thu Mar 24 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6-10
- konq webbrowsing profile: start.fedoraproject.org
- konq tabbedbrowsing : start.fedoraproject.org, fedoraproject.org/wiki/KDE

* Tue Mar 22 2011 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.6-9
- Requires: polkit-desktop-policy

* Thu Mar 10 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6-8
- s/QtCurve/oxygen-gtk/

* Mon Mar 07 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6-7
- use adwaita-cursor-theme

* Mon Mar 07 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6-6
- use lovelock-kdm-theme
- /var/log/kdm.log is never clean up (logrotate) (#682761)
- -kdm, move xterm dep to comps (#491251)

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.6-4.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Feb 07 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6-4
- de-Laughlin-ize theming, be genericish/upstream (for now)
- kcminputrc: theme=dmz-aa, Requires: dmz-cursor-themes (#675509)

* Tue Feb 01 2011 Rex Dieter <rdieter@fedoraproject.org> 4.6-3
- add support for the postlogin PAM stack to kdm (#665060)

* Wed Dec 08 2010 Rex Dieter <rdieter@fedoraproject.org> 4.6-2.1
- %%post kdm : sed -e 's|-nr|-background none|' kdmrc (#659684)
- %%post kdm : drop old stuff

* Fri Dec 03 2010 Rex Dieter <rdieter@fedoraproject.org> - 4.6-2
- drop old Conflicts
- Xserver-1.10: Fatal server error: Unrecognized option: -nr (#659684)

* Mon Nov 29 2010 Rex Dieter <rdieter@fedoraproject.org> 4.6-1 
- init 4.6 
- /var/run/kdm/ fails to be created on boot (#657785)

* Thu Nov 11 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-11
- kdebugrc: DisableAll=true (#652367)

* Fri Oct 29 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-10
- kdmrc: UserList=false

* Thu Oct 14 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-9
- drop plasma-{desktop,netbook}-appletsrc
- plasmarc: set default plasma(-netbook) themes (#642763)

* Sat Oct 09 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-8
- rename 00-start-here script to ensure it runs (again).

* Fri Oct 08 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-7
- make 00-start-here-kde-fedora.js look for simplelauncher too (#615621)

* Tue Sep 28 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-6
- move plasma-desktop bits into kde-settings/kde-profile instead

* Tue Sep 28 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-5
- 00-start-here-kde-fedora.js plasma updates script (#615621)

* Fri Sep 03 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-4
- kdeglobals : drop [Icons] Theme=Fedora-KDE (#615621)

* Tue Aug 03 2010 Jaroslav Reznik <jreznik@redhat.com> 4.5-3
- laughlin kde theme as default

* Mon Apr 26 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-2
- kde-settings-kdm depends on xorg-x11-xdm (#537608)

* Tue Apr 13 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-1.1
- -kdm: own /var/spool/gdm (#551310,#577482)

* Tue Feb 23 2010 Rex Dieter <rdieter@fedoraproject.org> 4.5-1
- 4.5 branch for F-14
- (re)enable kdebug

* Tue Feb 23 2010 Rex Dieter <rdieter@fedoraproject.org> 4.4-13
- disable kdebug by default (#560508)

* Mon Feb 22 2010 Jaroslav Reznik <jreznik@redhat.com> 4.4-12
- added dist tag to release

* Mon Feb 22 2010 Jaroslav Reznik <jreznik@redhat.com> 4.4-11
- goddard kde theme as default

* Sat Jan 30 2010 Rex Dieter <rdieter@fedoraproject.org> 4.4-10
- move /etc/kde/kdm/backgroundrc => /var/lib/kdm/backgroundrc (#522513)
- own /var/lib/kdm (regression, #442081)

* Fri Jan 29 2010 Rex Dieter <rdieter@fedoraproject.org> 4.4-9
- krunnerrc: disable nepomuksearch plugin by default (#559977)

* Wed Jan 20 2010 Rex Dieter <rdieter@fedoraproject.org> 4.4-8
- plasma-netbook workspace has no wallpaper configured (#549996)

* Tue Jan 05 2010 Rex Dieter <rdieter@fedoraproject.org> 4.4-7
- externalize fedora-kde-icon-theme (#547701)

* Wed Dec 30 2009 Rex Dieter <rdieter@fedoraproject.org> 4.4-6.1
- -kdm: Requires: kdm

* Fri Dec 25 2009 Rex Dieter <rdieter@fedoraproject.org> 4.4-6
- use qtcurve-gtk2 by default (#547700)

* Wed Dec 23 2009 Rex Dieter <rdieter@fedoraproject.org> 4.4-4
- enable nepomuk, with some conservative defaults (#549436)

* Tue Dec 01 2009 Rex Dieter <rdieter@fedoraproject.org> 4.4-3
- kdmrc: ServerArgsLocal=-nr , for better transition from plymouth

* Tue Dec 01 2009 Rex Dieter <rdieter@fedoraproject.org> 4.4-2
- kdmrc: revert to ServerVTs=-1 (#475890)

* Sun Nov 29 2009 Rex Dieter <rdieter@fedoraproject.org> 4.4-1
- -pulseaudio: drop xine-lib-pulseaudio (subpkg no longer exists)

* Sun Nov 29 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.3-12.2
- bump for F13 devel

* Sun Nov 29 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.3-12.1
- -pulseaudio: Requires: xine-lib-pulseaudio

* Tue Oct 27 2009 Rex Dieter <rdieter@fedoraproject.org> 4.3-12
- plasma-desktop-appletsrc: Constantine wallpaper
- drop /etc/kde/kdm/Xservers (#530660)

* Thu Sep 24 2009 Than Ngo <than@redhat.com> - 4.3-10.1
- rhel cleanup

* Wed Sep 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3-10
- include /etc/profile.d/kde.(sh|csh) here, renable KDE_IS_PRELINKED

* Mon Sep 21 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3-9
- kdmrc: ForceUserAuthDir=true (#524583)

* Mon Sep 21 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3-8
- kdmrc: use /var/run/kdm for pid/xauth (#524583)

* Mon Sep 14 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3-7
- plasma-desktop-appletsrc: Constantine_Mosaico virus wallpaper default (#519320)

* Sat Sep 12 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3-6.1
- -kdm: fix up %%post, s/oxygen-air/Constantine/
- -kdm: Requires: system-kdm-theme

* Tue Sep 08 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3-6
- konversationrc: preconfigure #fedora #fedora-kde #kde #konversation channels
- kdmrc: Theme=.../Constantine
- ksplashrc: Theme=Constantine

* Thu Sep 03 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3-5
- plasma-desktop-appletsrc: wallpaper=/usr/share/wallpapers/Constantine_Mosaico/

* Wed Aug 26 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3-4.2
- drop Requires: system-backgrounds-kde (move to kdebase-workspace)

* Thu Aug 20 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3-4.1
- Requires: system-backgrounds-kde

* Tue Aug 18 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3-4
- KPackageKit: [CheckUpdate] interval=86400

* Wed Aug 12 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3-3
- kdm/ksplash: use default/air until constantine-themed bits land
- plasma-desktop-appletsrc: constantine slideshow
- pulseaudio: drop hard-coded pa-related phonon bits

* Fri Aug 07 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3-2
- add default plasmarc, plasma-desktop-appletrc (#516263)

* Fri Aug 07 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.3-1
- upstream branch for F-12 (kde-4.3)

* Sat Jul 25 2009 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.2-11.20090430svn
- rebuild for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild
- rename %%{rel} to %%{svndate} to fix automated bumps

* Thu Apr 30 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2-10.20090430svn
- nepomukserverrc: disable nepomuk

* Wed Apr 29 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2-9.20090429svn
- krunnerrc: disable contacts plugin, avoids akonadi launch on first login

* Mon Apr 27 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2-8.20090427svn
- -kdm: Requires: xterm (#491251), touchup Summary a bit

* Tue Apr 21 2009 Than Ngo <than@redhat.com> - 4.2-7.20090416svn
- get rid of requires on solar-kde-theme, it should leonidas-kde-theme for F11

* Thu Apr 16 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2-6.20090416
- update for leonidas-kde-theme

* Tue Apr 14 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2-5.20090414
- include kde-centric defaults.list
- kcmnspluginrc: include nspluginwrapper paths (#495632)

* Wed Feb 25 2009 Jaroslav Reznik <jreznik@redhat.com> - 4.2-4.20090225svn
- disable desktop effects by default

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.2-3.20090219svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Feb 18 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2-3
- gpg-agent-startup.sh: use gpg-agent --with-env-file (#486025)

* Fri Feb 06 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2-2
- remove defaults.list, add mimeapps.list, including
  prefs to fix "mime-type/extension for .rpm is wrong" (#457783)

* Fri Jan 23 2009 Rex Dieter <rdieter@fedoraproject.org> - 4.2-1
- rev/branch 4.2 for F-11

* Fri Jan 16 2009 Than Ngo <than@redhat.com> - 4.1-5
- wallpaper theme for new plasma in 4.2

* Fri Oct 31 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1-4
- KPackageKit: [CheckUpdate] autoUpdate=0 (#469375)

* Tue Oct 28 2008 Rex Dieter <rdieter@fedoraproject.org> 4.1-3
- kdmrc: ServerVTs=1 , drop tty1 from ConsoleTTYs
- kde-settings-20081028
- Url: fedorahosted.org/kde-settings

* Mon Oct 27 2008 Jaroslav Reznik <jreznik@redhat.com> 4.1-2
- Fedoraproject homepages for Konqueror

* Sun Oct 26 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.1-1
- default to Solar artwork

* Sat Sep 27 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0-29
- remove /etc/kde/env/pulseaudio.sh, no longer needed in F10 (#448477)

* Sat Sep 27 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0-28
- kxkbrc: set default keyboard model to evdev (matches F10+ X11 setup, #464101)

* Tue Sep 16 2008 Than Ngo <than@redhat.com> 4.0-27
- remove unneeded symlinks in Fedora-KDE icon theme

* Tue Sep 16 2008 Than Ngo <than@redhat.com> 4.0-26
- fix, systemsettings->icons doesn't show icons by Fedora-KDE
  icon theme

* Wed Jul 30 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0-25
- kcminputrc: [Mouse] cursorTheme=default

* Tue May 20 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0-24
- kdm pam settings need to sync with gdm (#447245)

* Fri May 16 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0-23
- don't set XDG_CONFIG_DIRS (#249109)

* Thu May 01 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0-22.1
- use correct _kde4_appsdir for kdm theme upgrade hack (#444730)

* Thu May 01 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0-22
- kdmrc: TerminateServer=true hack until Xserver fixed properly (#443307)
- %%post kdm: don't try to use old kde3 kdm themes (#444730)
- add/fix scriptlet deps

* Fri Apr 18 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0-21
- kglobalshortsrc: add keyboard shortcuts for Virtual desktop switching (#440415)

* Fri Apr 11 2008 Than Ngo <than@redhat.com> 4.0-20
- set Fedora_Waves wallpaper theme default

* Thu Apr 10 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0-19
- kmixrc: Visible=false
- ksmserverrc: start kmix (could use autostart for this too)
- kwalletrc: (sane defaults)

* Thu Apr 10 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0-18
- kdmrc: [X-*-Greeter] Theme=FedoraWaves
- ksplashrc: [KSplash] Theme=FedoraWaves
- kdmrc: [Shutdown] BootManager=None (#441313)

* Wed Apr 09 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0-17
- env.sh: XDG_CONFIG_DATA -> XDG_DATA_DIRS (oops)
- kdmrc: [X-*-Greeter] ColorScheme=ObsidianCoast
- include Fedora-KDE icon theme (#438973)
- kdeglobals: [Icons] Theme=Fedora-KDE (#438973)

* Mon Apr 07 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0-16.1
- -pulseaudio: Requires: xine-lib-pulseaudio

* Mon Apr 07 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0-16
- backgroundrc,kdmrc: first stab at F9/sulfur theming (#441167)
- kdmrc: ServerArgsLocal=-br (suggested by ajax)

* Thu Mar 27 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0-15
- ksplashrc: [KSplash] Theme=Waves

* Thu Mar 20 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0-14.1
- Requires: oxygen-icon-theme

* Tue Mar 11 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0-14
- kde4rc: omit userProfileMapFile key

* Mon Mar 10 2008 Than Ngo <than@redhat.com> 4.0-13.1
- make oxygen the default windows manager

* Mon Mar 10 2008 Than Ngo <than@redhat.com> 4.0-12.1
- gestures disable as default
- omit kdesktoprc

* Sun Mar 09 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> 4.0-11.1
- symlink /etc/kderc to /etc/kde4rc

* Tue Feb 19 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0-11
- kdmrc: BootManager=Grub (#374011)
- omit errant clock_pannelapplet_wkid..._rc (#431890)
- include (initially empty) applications/defaults.list
- env.sh: set XDG_CONFIG_DATA
- ksplashrc: disable FedoraInfinity (for now, doesn't work)
- kdeglobals: cleanup, set oxygen defaults mostly
- kickerrc 'n friends: nuke

* Fri Feb 15 2008 Than Ngo <than@redhat.com> 4.0-10
- added default bookmarks (imported from fedora-bookmarks),
  thanks Sebastian Vahl 

* Wed Jan 23 2008 Rex Dieter <rdieter@fedoraproject.org> 4.0-9.1
- include gpg-agent scripts here (#427316)

* Sat Jan 19 2008 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.0-9
- kdeglobals: also set K3Spell_Client=4 and K3Spell_Encoding=11

* Thu Jan 10 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 4.0-8
- include /etc/kde/env/env.sh (#426115)
- move extra sources into tarball
- -kdm: cleanup deps

* Fri Jan 04 2008 Rex Dieter <rdieter[AT]fedoraproject.org> 4.0-7
- omit legacy/crufy etc/skel bits
- -pulseaudio: -Requires: xine-lib-extras (too buggy)

* Sat Dec 22 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.0-6
- kdeglobals: KSpell_Client=4 (Hunspell), add KSpell_Encoding=11 (UTF-8)

* Wed Dec 12 2007 Than Ngo <than@redhat.com> 4.0-5
- add missing kdm-np pam, bz421931

* Fri Dec 07 2007 Than Ngo <than@redhat.com> 4.0-4
- kdmrc: ServerTimeout=30

* Wed Dec 05 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 4.0-3
- include pam configs
- -pulseaudio: +Requires: xine-lib-extras

* Tue Dec 04 2007 Than Ngo <than@redhat.com> 4.0-2
- kdmrc: circles as kdm default theme

* Mon Dec 03 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> - 4.0-1
- kdmrc: fix ClientLogFile and EchoMode->EchoPasswd for KDE 4 KDM
- kdmrc: disable Infinity theme (revert to circles), incompatible with KDE 4
- Require kde-filesystem instead of kdelibs3
- don't Require redhat-artwork

* Wed Oct 31 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 3.5-35
- kdeglobals: remove [WM] section, which overrides ColorScheme

* Mon Oct 29 2007 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.5-34
- ksplashrc: Theme=FedoraInfinity (thanks to Chitlesh Goorah)

* Tue Oct 23 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 3.5-33.1
- -pulseaudio: new subpkg, to enable pulseaudio support

* Tue Oct 23 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 3.5-33
- kdmrc: ColorScheme=FedoraInfinityKDM
- ksplashrc: drop Theme=Echo (ie, revert to Default)
- kdeglobals: colorScheme=FedoraInfinity.kcsrc

* Tue Oct 02 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 3.5-32
- f8: Requires: fedorainfinity-kdm-theme (#314041)
      kdmrc: [X-*-Greeter] Theme=.../FedoraInfinity
      kdmrc: [X-*-Greeter] ColorScheme=FedoraInfinity

* Wed Sep 26 2007 Rex Dieter <rdieter[AT]fedoraproject.org> - 3.5-31
- kdesktoprc: [Desktop0] Wallpaper=/usr/share/backgrounds/images/default.png
  (#290571)
- kopeterc: [ContactList] SmoothScrolling=false

* Mon Jul 02 2007 Than Ngo <than@redhat.com> -  3.5-30
- fix bz#245100

* Mon Jun 18 2007 Than Ngo <than@redhat.com> -  3.5-29
- cleanup kde-setings, bz#242564

* Mon May 21 2007 Than Ngo <than@redhat.com> - 3.5-28
- don't hardcode locale in kdeglobals config
- cleanup clock setting
- plastik as default colorscheme
- use bzip2

* Fri May 18 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-27
- kdeglobals: [Icons] Theme = crystalsvg
- kdeglobals: [Paths] Trash[$e]=$(xdg-user-dir DESKTOP)/Trash/
- Requires: xdg-user-dirs

* Thu May 17 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-26
- omit kde-profile/default/share/icons

* Tue May 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-25
- ksplashrc does not contain Echo (#233881)
- kdmrc: MaxShowUID=65530, so we don't see nfsnobody
- kdmrc: HiddenUsers=root (MinShowUID=500 doesn't work?)

* Tue May 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-24
- omit FedoraFlyingHigh.kcsrc (it's now in redhat-artwork-kde)
- kdeglobals: xdg-user-dirs integration: Desktop, Documents (#238371)

* Tue May 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-23
- backgroundrc: Background=default.jpg 
- kderc: kioskAdmin=root:
- omit (previously accidentally included) alternative konq throbbers

* Tue May 15 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-21
- kiosk-style configs (finally)
- kdm use UserLists, FedoraFlyingHigh color scheme (#239701) 

* Tue May 01 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-20
- don't mix tab/spaces
- %%setup -q
- Source0 URL comment

* Mon Apr 30 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-19
- omit xdg_hack (for now)
- fc7+: Req: redhat-artwork-kde
- reference: kdelibs: use FHS-friendly /etc/kde (vs. /usr/share/config), bug #238136

* Wed Feb 14 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-18
- rename to kde-settings, avoid confusion with builtin %%_bindir/kde-config

* Wed Feb 14 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-17
- put back awol: Obsoletes/Provides: kde-config-kdebase

* Wed Jan 17 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-16
- kcmnspluginrc: scanPaths: +/usr/lib/firefox/plugins (flash-plugin-9 compat)

* Sat Jan 06 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-15
- xdg_env-hack: handle XDG_MENU_PREFIX too

* Fri Jan 05 2007 Rex Dieter <rdieter[AT]fedoraproject.org> 3.5-14
- +Requires: kdelibs
- -kdm: +Requires: kdebase-kdm

* Fri Nov 17 2006 Rex Dieter <rexdieter[AT]users.sf.net> 3.5-13
- mv xdg_config_dirs-hack to env startup script instead of autostart konsole app.
- rename -kdebase -> -kdm
- drop circular dependency crud.

* Fri Oct 27 2006 Rex Dieter <rexdieter[AT]users.sf.net> 3.5-12
- %%exclude %%_datadir/config/kdm (from main pkg)
- ksmserverrc: loginMode=restoreSavedSession

* Fri Oct 27 2006 Rex Dieter <rexdieter[AT]users.sf.net> 3.5-10
- kwinrc: PluginLib=kwin_plastik (from kwin_bluecurve)
- xdg_config_dirs-hack: backup existing $HOME/.config/menus

* Tue Oct 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 3.5-7
- fixup %%pre/%%post to properly handle kdmrc move
- xdg_config_dirs-hack: don't run on *every* login

* Tue Oct 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 3.5-6
- xdg_config_dirs-hack: hack to force (re)run of kbuildsycoca if a
  change in $XDG_CONFIG_DIRS is detected. 

* Tue Oct 24 2006 Rex Dieter <rexdieter[AT]users.sf.net> 3.5-5
- kdmrc: prefer FedoraDNA,Bluecurve Themes respectively (if available)
- kdeglobals: (Icon) Theme=Bluecurve (minimize migration pain)

* Mon Oct 23 2006 Rex Dieter <rexdieter[AT]users.sf.net> 3.5-4
- kdeglobals: [Locale] US-centric defaults

* Tue Oct 17 2006 Rex Dieter <rexdieter[AT]users.sf.net> 3.5-3
- -kdebase: own %%_sysconfdir/kde/kdm, %%_datadir/config/kdm

* Wed Oct 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 3.5-2
- actually include something this time

* Wed Oct 11 2006 Rex Dieter <rexdieter[AT]users.sf.net> 3.5-1
- first try

