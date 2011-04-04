%define _unpackaged_files_terminate_build 0

Name:    kdemultimedia
Summary: KDE sound support for Qubes Dom0
Version: %{version}
Release: %{rel}.qubes
Epoch:   1000

# see also: http://techbase.kde.org/Policies/Licensing_Policy
License: GPLv2+
URL:     http://www.kde.org/
Source0: kdemultimedia-%{version}.tar.bz2

# Some of the Fedora patches used for their kdemultimedia package
###############################################################
#
# git clone git://colin.guthr.ie/kdemultimedia
# git checkout -t origin/pulse
# git diff master..pulse > kmix_pa-<date>.patch
# See also, http://svn.mandriva.com/cgi-bin/viewvc.cgi/packages/cooker/kdemultimedia4/current/SOURCES/kmix-pulse.patch
Patch3: kmix-pulse.patch

###############################################################
# Qubes Patches:

Patch100: kdemultimedia-4.4.3-qubes-cleanup.patch

#
# END of Patches
###############################################################

BuildRequires: alsa-lib-devel
BuildRequires: glib2-devel
BuildRequires: kdebase-workspace-devel >= %{version}
BuildRequires: pulseaudio-libs-devel

Requires: kdelibs4%{?_isa} >= %{version}
Requires: kdebase-workspace >= %{version}

%description
%{summary}.

%prep
%setup -q -n kdemultimedia-%{version}

#%patch3 -p1 -b .kmix-pulse

%patch100 -p1 -b .qubes-cleanup

%build

mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}


%clean
rm -rf %{buildroot}


%post
touch --no-create %{_kde4_iconsdir}/hicolor &> /dev/null ||:
touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null ||:

/sbin/ldconfig

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

/sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc COPYING README
%{_kde4_bindir}/*
%{_kde4_appsdir}/kmix/
%{_kde4_datadir}/applications/kde4/*
%{_kde4_datadir}/autostart/*
%{_kde4_datadir}/kde4/services/*
%{_datadir}/dbus-1/interfaces/*
%{_kde4_docdir}/HTML/en/kmix/
%{_kde4_docdir}/HTML/en/kioslave/
%{_kde4_iconsdir}/hicolor/*/*/*
%{_kde4_libdir}/libkdeinit*.so
#%{_kde4_libdir}/lib*.so.*
#%{_kde4_libdir}/kde4/*.so

%changelog
* Mon May 31 2010 Joanna Rutkowska <joanna@invisiblethingslab.com>
- spec file adapted to Qubes OS (based on Fedora spec)
- based on the original spec from Fedora 12:

