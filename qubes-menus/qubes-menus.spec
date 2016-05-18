%if 0%{?qubes_builder}
%define _sourcedir %(pwd)/qubes-menus
%define _builddir %(pwd)/qubes-menus
%endif

%define gettext_package redhat-menus
%define desktop_file_utils_version 0.9

Summary: Configuration and data files for the desktop menus
Name: qubes-menus
Version: 1.1
Release: 1
URL: http://www.qubes-os.org
License: GPL+
Group: User Interface/Desktops
BuildArch: noarch
BuildRequires: desktop-file-utils >= %{desktop_file_utils_version}
Requires(post): desktop-file-utils >= %{desktop_file_utils_version}
Requires(postun): desktop-file-utils >= %{desktop_file_utils_version}

## old nautilus contained start-here stuff
Conflicts: nautilus <= 2.0.3-1
## desktop files in redhat-menus point to icons in new artwork
Conflicts: redhat-artwork < 0.35
## old evolution packages point to a no-longer-existing symlink
Conflicts: evolution <= 2.4.1-5

Provides: redhat-menus
Obsoletes: redhat-menus

%description
This package contains the XML files that describe the menu layout for
GNOME and KDE, and the .desktop files that define the names and icons
of "subdirectories" in the menus.
_
%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_sysconfdir}/xdg/menus
install -m 644 menus/*.menu $RPM_BUILD_ROOT%{_sysconfdir}/xdg/menus/

ln -s applications.menu $RPM_BUILD_ROOT%{_sysconfdir}/xdg/menus/kde4-qubes-applications.menu
ln -s applications.menu $RPM_BUILD_ROOT%{_sysconfdir}/xdg/menus/kf5-qubes-applications.menu

install -d $RPM_BUILD_ROOT%{_datarootdir}/desktop-directories
install -m 644 directory-files/*.directory $RPM_BUILD_ROOT%{_datarootdir}/desktop-directories/

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xdg/menus/applications-merged ||:
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xdg/menus/preferences-merged ||:
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xdg/menus/preferences-post-merged ||:
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xdg/menus/settings-merged ||:

# create the settings-merged to prevent gamin from looking for it
# in a loop
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xdg/menus/settings-merged ||:

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- authconfig-gtk
rm -f %{_datadir}/applications/authconfig.desktop

%triggerin -- gnome-packagekit
rm -f %{_datadir}/applications/gpk-application.desktop
rm -f %{_datadir}/applications/gpk-update-viewer.desktop

%triggerin -- system-config-date
rm -f %{_datadir}/applications/system-config-date.desktop

%triggerin -- system-config-users
rm -f %{_datadir}/applications/system-config-users.desktop

%triggerin -- system-config-keyboard
rm -f %{_datadir}/applications/system-config-keyboard.desktop

%triggerin -- nepomuk-core
rm -f %{_datadir}/applications/kde4/nepomukbackup.desktop

%posttrans
update-desktop-database %{_datadir}/applications

%files
%defattr(-,root,root)
%doc README
%dir %{_sysconfdir}/xdg/menus
%dir %{_sysconfdir}/xdg/menus/applications-merged
%dir %{_sysconfdir}/xdg/menus/preferences-merged
%dir %{_sysconfdir}/xdg/menus/preferences-post-merged
%dir %{_sysconfdir}/xdg/menus/settings-merged
%config %{_sysconfdir}/xdg/menus/*.menu
%{_datadir}/desktop-directories/*.directory

%changelog
* Thu May  3 2012 Marek Marczykowski <marmarek@invisiblethingslab.com>
- Initial package based on redhat-menus
