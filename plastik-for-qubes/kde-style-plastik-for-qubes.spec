Name: kde-style-plastik-for-qubes
Version: 1.0
Release: 1%{?dist}
URL: http://www.qubes-os.org/
Source: .
Group: User Interface/Desktops
License: GPLv3
BuildRequires: qt4-devel
BuildRequires: kde-filesystem
BuildRequires: kdelibs4-devel
BuildRequires: kdebase-workspace-devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Summary: Plastik for Qubes


%{?_kde4_macros_api:Requires: kde4-macros(api) = %{_kde4_macros_api} }


%description
Plastik KDE decorations with Qubes color labels.

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd
   
make VERBOSE=1 %{?_smp_mflags} -C %{_target_platform}


%install
rm -rf %{buildroot}
mkdir %{buildroot}
make install DESTDIR=%{buildroot} -C %{_target_platform}
    

%clean
rm -rf %{buildroot}


%files
%defattr(-, root, root)
%{_kde4_libdir}/kde4/kwin3_plastik_for_qubes.so
%{_kde4_libdir}/kde4/kwin_plastik_for_qubes_config.so
%{_kde4_appsdir}/kwin/plastik_for_qubes.desktop


%changelog
* Wed Feb 06 2013 Marek Marczykowski - 1.0-1
- extract to separate package

