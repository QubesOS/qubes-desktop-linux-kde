# This is a meta package that makes installing all KDE components easy

Name:    qubes-kde-dom0
Summary: Metapackage for installing all KDE components needed for Qubes Dom0
Version: %{version}
Release: %{rel}

License: GPL2
URL: http://qubes-os.org

BuildArch: noarch

Requires: kde-filesystem >= %{version}
Requires: kde-settings >= %{version}
Requires: kde-settings-kdm >= %{version}
Requires: kdelibs >= %{version}
Requires: kdebase-workspace >= %{version}
Requires: kdebase-workspace-libs >= %{version}
#Requires: kdebase-workspace-wallpapers
Requires: kdebase-runtime >= %{version}
Requires: kdebase-runtime-libs >= %{version}
Requires: kdebase-runtime-flags >= %{version}
Requires: kdebase >= %{version}
Requires: kdm >= %{version}
Requires: ksysguardd
Requires: oxygen-cursor-themes
Requires: oxygen-icon-theme
Requires: kdemultimedia

# other 3rd party packages that are useful in Dom0...

# The konsole really looks awful without those fonts:
Requires: dejavu-sans-mono-fonts
Requires: dejavu-sans-fonts

# This is for people who don't use NetVM (i.e. don't have VT-d hardware)
# This should be left to the user IMO
#Requires: knetworkmanager

# Qubes-customized menus
Requires: qubes-menus

Source0: kfileplaces-bookmarks.xml

%description
%{summary}.

%install
install -D %{SOURCE0} %{buildroot}%{_sysconfdir}/skel/.kde/share/apps/kfileplaces/bookmarks.xml

%files
%defattr (-,root,root,-)
%{_sysconfdir}/skel/.kde/share/apps/kfileplaces/bookmarks.xml
%changelog
* Mon May 24 2010 Joanna Rutkowska <joanna@invisiblethingslab.com>
- spec file adapted to Qubes OS (based on Fedora spec)
- based on the original spec from Fedora 12:

