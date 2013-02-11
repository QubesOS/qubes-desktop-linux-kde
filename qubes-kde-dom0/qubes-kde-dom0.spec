# This is a meta package that makes installing all KDE components easy

Name:    qubes-kde-dom0
Summary: Metapackage for installing all KDE components needed for Qubes Dom0
Version: %{version}
Release: %{rel}

License: GPL2
URL: http://qubes-os.org

BuildArch: noarch

Requires: kde-filesystem
Requires: kde-settings
Requires: kde-settings-kdm
Requires: kdelibs >= %{version}
Requires: kde-workspace >= %{version}
Requires: kde-workspace-libs >= %{version}
#Requires: kde-workspace-wallpapers
Requires: kde-runtime >= %{version}
Requires: kde-runtime-libs >= %{version}
Requires: kde-runtime-flags >= %{version}
Requires: kde-baseapps >= %{version}
Requires: kdm >= %{version}
Requires: ksysguardd
Requires: oxygen-cursor-themes
Requires: oxygen-icon-theme

# other 3rd party packages that are useful in Dom0...

# The konsole really looks awful without those fonts:
Requires: dejavu-sans-mono-fonts
Requires: dejavu-sans-fonts

# This is for people who don't use NetVM (i.e. don't have VT-d hardware)
# This should be left to the user IMO
#Requires: knetworkmanager

# Qubes-customized menus
Requires: qubes-menus

Requires: kde-style-plastik-for-qubes

Source0: kfileplaces-bookmarks.xml
Source1: kickoffrc
source2: kscreensaverrc

%description
%{summary}.

%install
install -D %{SOURCE0} %{buildroot}%{_sysconfdir}/skel/.kde/share/apps/kfileplaces/bookmarks.xml
install -D %{SOURCE1} %{buildroot}%{_sysconfdir}/skel/.kde/share/config/kickoffrc
install -D %{SOURCE2} %{buildroot}%{_sysconfdir}/skel/.kde/share/config/kscreensaverrc

%files
%defattr (-,root,root,-)
%{_sysconfdir}/skel/.kde/share/apps/kfileplaces/bookmarks.xml
%{_sysconfdir}/skel/.kde/share/config/kickoffrc
%{_sysconfdir}/skel/.kde/share/config/kscreensaverrc
%changelog
* Mon May 24 2010 Joanna Rutkowska <joanna@invisiblethingslab.com>
- spec file adapted to Qubes OS (based on Fedora spec)
- based on the original spec from Fedora 12:

