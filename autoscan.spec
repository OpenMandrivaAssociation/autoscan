%define	rname autoscan-network

Summary:        Utility for network exploration (Samba,Nessus client)
Name:           autoscan
Version:        1.12
Release: 	%mkrel 1
License:        GPLv2
Group:		Networking/Other
URL:            http://autoscan-network.com/
Source0:        http://autoscan.fr/download/autoscan-network-%{version}.tar.gz
Patch0:		Autoscan-x86_64-build-fix.patch
BuildRequires:  libsmbclient-devel
BuildRequires:  gnomeui2-devel
BuildRequires:  libxml2-devel
BuildRequires:  openssl-devel
BuildRequires:	libao-devel
BuildRequires:	libvorbis-devel
BuildRequires:	net-snmp-devel
BuildRequires:  libtool
BuildRequires:  elfutils-devel
BuildRequires:  gtk+2-devel
BuildRequires:  gnome-keyring-devel
BuildRequires:  gnome-vfs2-devel
BuildRequires:  glib-devel
BuildRequires:  vte-devel
BuildRequires:  desktop-file-utils
Requires:       samba-client
Requires:	webclient
Requires:       %{name}-agent
Provides:	%{rname} = %{version}
Obsoletes:	AutoScan
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot 

%description
AutoScan is an application designed to explore and to manage your network. 
Entire subnets can be scanned simultaneously without human intervention. 
It features OS detection, automatic network discovery, a port scanner, 
a Samba share browser, and the ability to save the network state.

%package 	agent
Summary: 	AutoScan daemon
Group: 		Networking/Other
Provides: 	%{name} = %{version}-%{release}
Provides:	%{rname} = %{version}
Obsoletes:	%{rname}
Provides:	%{rname}-agent = %{version}
Obsoletes:	%{rname}-agent

%description 	agent
Scans network in the background


%prep  

%setup -q -n %{rname}-%{version} -a 0
#%patch0

%build
./configure --distrib-mandriva
%make

%install
rm -rf %{buildroot}

#Daemon install
install -d %{buildroot}%{_sbindir}/
install -d %{buildroot}%{_initrddir}/
install -m755 bin/autoscan-network-daemon %{buildroot}%{_sbindir}/
install -m755 init.d/autoscan-network-mandriva %{buildroot}%{_initrddir}/autoscan-network

#Gui install
install -d %{buildroot}%{_datadir}/apps/%{rname}
install -d %{buildroot}%{_datadir}/pixmaps/%{rname}
install -d %{buildroot}%{_datadir}/sounds/%{rname}
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_iconsdir}
install -d %{buildroot}%{_datadir}/applications/

install -m755 bin/autoscan-network %{buildroot}%{_bindir}/

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --remove-key='Encoding'  --remove-key='MultipleArgs' \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications usr/share/applications/*.desktop

install usr/share/icons/autoscan-network.png %{buildroot}%{_iconsdir}
cp -r usr/share/pixmaps/autoscan-network/* %{buildroot}%{_datadir}/pixmaps/%{rname}/

install -m644 usr/share/apps/autoscan-network/* %buildroot%_datadir/apps/%{rname}
install -m 644 usr/share/sounds/autoscan-network/* %{buildroot}%{_datadir}/sounds/%{rname}/

install -D -m644 usr/share/apps/autoscan-network/autoscan-network.schemas %buildroot%{_sysconfdir}/gconf/schemas/%{name}.schemas

%post
%post_install_gconf_schemas %{name}
%update_menus

%postun
%clean_menus

%preun
%preun_uninstall_gconf_schemas %{name}

%post agent
%_post_service %{name}-network

%postun agent
%_preun_service %{name}-network

%clean
rm -rf %{buildroot}

%files
%defattr(755,root,root)
%doc AUTHORS CHANGELOG
%{_sysconfdir}/gconf/schemas/%{name}.schemas
%{_bindir}/*
%{_datadir}/apps/%{rname}
%{_datadir}/pixmaps/%{rname}
%{_iconsdir}/*
%{_datadir}/sounds/%{rname}/*  
%{_datadir}/applications/*.desktop

%files agent
%defattr(755,root,root)
%{_sbindir}/*
%{_initrddir}/*
