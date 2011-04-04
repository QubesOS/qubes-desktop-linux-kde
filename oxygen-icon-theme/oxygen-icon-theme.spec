Name:          oxygen-icon-theme
Summary:       Oxygen icon theme
Version:       %{version}
Release:       %{rel}.qubes
Epoch:         1000

# http://techbase.kde.org/Policies/Licensing_Policy
License:       LGPLv3+ 
URL:           http://www.kde.org/
Source0:       oxygen-icons-%{version}.tar.bz2
BuildArch:     noarch

BuildRequires: cmake
BuildRequires: hardlink
BuildRequires: kde-filesystem

%description
%{summary}.

%prep
%setup -q -n oxygen-icons-%{version}

%build
mkdir -p %{_target_platform}
pushd %{_target_platform}
%{cmake_kde4} ..
popd

make %{?_smp_mflags} -C %{_target_platform} 

%install
rm -rf %{buildroot}

make install/fast DESTDIR=%{buildroot} -C %{_target_platform}

# As of 4.4.0, hardlink reports 724 dupes, and savings of 5349376 bytes
/usr/sbin/hardlink -c -v %{buildroot}%{_kde4_iconsdir}/oxygen

%clean
rm -rf %{buildroot}


%post 
touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null || :

%posttrans 
gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &> /dev/null || :

%postun 
if [ $1 -eq 0 ] ; then
touch --no-create %{_kde4_iconsdir}/oxygen &> /dev/null || :
gtk-update-icon-cache %{_kde4_iconsdir}/oxygen &> /dev/null || :
fi


%files 
%defattr(-,root,root,-)
%doc AUTHORS CONTRIBUTING COPYING TODO*
%{_kde4_iconsdir}/oxygen/


%changelog
* Mon May 24 2010 Joanna Rutkowska <joanna@invisiblethingslab.com>
- spec file adapted to Qubes OS (based on Fedora spec) 4.4.3-1
- based on the original spec from Fedora 12

