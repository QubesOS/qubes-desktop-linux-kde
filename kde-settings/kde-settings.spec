Summary: Config files for KDE in Qubes Dom0
Name:    kde-settings
Version: %{version}
Release: %{rel}.qbs1
Epoch:   1000

License: Public Domain
BuildArch: noarch

Source: kde-settings.tar.bz2
BuildRequires: kde-filesystem

Requires: kde-filesystem
Requires: oxygen-icon-theme
Requires: xdg-user-dirs
Requires: coreutils
Provides: kde-settings-dom0

###############################################################
# Qubes Patches:
Patch100: kde-settings-4.4.5-plastik-for-qubes.patch
###############################################################

%description
%{summary}.

%package kdm
Summary: Configuration files for kdm
Requires: xorg-x11-xdm
Requires(pre): coreutils
Requires(post): coreutils grep sed
Requires(post): kde4-macros(api) = %{_kde4_macros_api}
# failsafe session (rhbz#491251)
Requires: xterm
%description kdm
%{summary}.

%prep
%setup -q -n %{name}
%patch100 -p1

%build
# Intentionally left blank.  Nothing to see here.

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT{%{_datadir}/config,%{_sysconfdir}/kde/kdm}

tar cpf - . | tar --directory $RPM_BUILD_ROOT -xvpf -

# kdebase/kdm symlink
rm -rf   $RPM_BUILD_ROOT%{_datadir}/config/kdm
ln -sf ../../../etc/kde/kdm $RPM_BUILD_ROOT%{_datadir}/config/kdm

# own these
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/lib/kdm
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/run/kdm

# own as part of plymouth/kdm integration hacks (#551310)
mkdir -p -m775 $RPM_BUILD_ROOT%{_localstatedir}/spool/gdm

%clean
rm -rf $RPM_BUILD_ROOT

%post

%postun

%pre kdm
## KDM fixup(s)
# handle move from /etc/X11/xdm/kdmrc to /etc/kde/kdm/kdmrc
[ -L %{_sysconfdir}/kde/kdm/kdmrc ] && \
  %{__mv} -v %{_sysconfdir}/kde/kdm/kdmrc %{_sysconfdir}/kde/kdm/kdmrc.rpmorig ||:
# handle %%_datadir/config/kdm -> /etc/kde/kdm
[ -d %{_datadir}/config/kdm -a ! -L %{_datadir}/config/kdm ] && \
  %{__mv} -v %{_datadir}/config/kdm %{_datadir}/config/kdm.rpmorig ||:

%post kdm
## KDM fixup(s)
# handle move from /etc/X11/xdm/kdmrc to /etc/kde/kdm/kdmrc
[ ! -f %{_sysconfdir}/kde/kdm/kdmrc -a -f %{_sysconfdir}/kde/kdm/kdmrc.rpmnew ] && \
  %{__cp} -a %{_sysconfdir}/kde/kdm/kdmrc.rpmnew %{_sysconfdir}/kde/kdm/kdmrc ||:
# kdm v3 themes don't work (#444730)
# this hack assumes %_datadir != %_kde4_datadir
(grep "^Theme=%{_datadir}/apps/kdm/themes/" %{_sysconfdir}/kde/kdm/kdmrc > /dev/null && \
 sed -i -e "s|^Theme=%{_datadir}/apps/kdm/themes/.*|Theme=%{_kde4_appsdir}/kdm/themes/Constantine|" \
 %{_sysconfdir}/kde/kdm/kdmrc
) ||:


%files 
%defattr(-,root,root,-)
%config(noreplace) %{_sysconfdir}/profile.d/kde.*
%{_sysconfdir}/kde/env/env.sh
%config(noreplace) /etc/pam.d/kcheckpass
%config(noreplace) /etc/pam.d/kscreensaver
# drop noreplace, so we can be sure to get the new kiosk bits
%config %{_sysconfdir}/kderc
%config %{_sysconfdir}/kde4rc
%{_datadir}/kde-settings/

%files kdm
%defattr(-,root,root,-)
%config(noreplace) /etc/pam.d/kdm*
# compat symlink
%{_datadir}/config/kdm
%dir %{_sysconfdir}/kde/kdm
%config(noreplace) %{_sysconfdir}/kde/kdm/backgroundrc
%config(noreplace) %{_sysconfdir}/kde/kdm/kdmrc
%ghost %config(missingok,noreplace) %verify(not md5 size mtime) %{_sysconfdir}/kde/kdm/README*
%{_sysconfdir}/kde/kdm/Xaccess
%{_sysconfdir}/kde/kdm/Xresources
%{_sysconfdir}/kde/kdm/Xsession
%{_sysconfdir}/kde/kdm/Xwilling
%{_sysconfdir}/kde/kdm/Xsetup
%dir %{_localstatedir}/lib/kdm
%attr(1777,root,root) %dir %{_localstatedir}/run/kdm
%attr(0775,root,root) %dir %{_localstatedir}/spool/gdm

%changelog
* Mon May 24 2010 Joanna Rutkowska <joanna@invisiblethingslab.com>
- spec file adapted to Qubes OS (based on Fedora spec) 4.4.3-1
- based on the original spec from Fedora 12

