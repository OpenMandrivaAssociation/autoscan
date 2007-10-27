%define	rname autoscan-network

Summary:        Utility for network exploration (Samba,Nessus client)
Name:           autoscan
Version:        1.10
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
%make AutoScan_Agent
%make AutoScan_Network 

%install
rm -rf %{buildroot}

#Daemon install
install -d %{buildroot}%{_sbindir}/
install -d %{buildroot}%{_initrddir}/
install -m755 src/AutoScan_Agent/AutoScan_Agent %{buildroot}%{_sbindir}/
install -m755 init.d/autoscan_mandriva %{buildroot}%{_initrddir}/autoscan

#Gui install
install -d %{buildroot}%{_datadir}/doc/AutoScan/
install -d %{buildroot}%{_datadir}/pixmaps/AutoScan/
install -d %{buildroot}%{_datadir}/apps/AutoScan/
install -d %{buildroot}%{_bindir}/
install -d %{buildroot}%{_datadir}/icons/
install -d %{buildroot}%{_datadir}/sounds/AutoScan/
install -d %{buildroot}%{_datadir}/applications/

pwd
install -m755 src/AutoScan/AutoScan_Network_Gui %{buildroot}%{_bindir}/
install -m755 Script/* %{buildroot}%{_bindir}/
cp -R usr/* %{buildroot}%{_prefix}/

#file listed twice
rm %{buildroot}%{_datadir}/doc/AutoScan/copyright

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --remove-key="MultipleArgs" \
  --add-category="Network" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

%post
export GCONF_CONFIG_SOURCE="$(gconftool-2 --get-default-source)"
%post_install_gconf_schemas %{name}
%update_menus

%postun
%clean_menus

%post agent
%_post_service %{name}

%postun agent
%_preun_service %{name}

%clean
rm -rf %{buildroot}

%files
%defattr(755,root,root)
%doc AUTHORS CHANGELOG copyright
%{_bindir}/*
%{_bindir}/*
%{_bindir}/*
%{_datadir}/apps/%{rname}/*
%{_datadir}/pixmaps/%{rname}/*
%{_iconsdir}/*
%{_datadir}/sounds/%{rname}/*  
%{_datadir}/applications/*.desktop

%files agent
%defattr(755,root,root)
%{_sbindir}/AutoScan_Agent
%{_initrddir}/%{name}
