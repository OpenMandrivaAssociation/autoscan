%define name    AutoScan
%define oname	autoscan
%define	daemon	agent
%define version 1.01
%define release %mkrel 3

Name:           %{name} 
Summary:        Utility for network exploration (Samba,Nessus client)
Version:        %{version} 
Release: 	%{release}
Source0:        http://autoscan.fr/%{name}-%{version}.tar.bz2
Patch0:		Autoscan-x86_64-build-fix.patch
URL:            http://autoscan.fr
Group:		Networking/Other
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot 
License:        GPLv2
BuildRequires:  libsmbclient-devel
BuildRequires:  gnomeui2-devel
BuildRequires:  libxml2-devel
BuildRequires:  zvt-devel
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
Requires:       mozilla-firefox
Requires:       AutoScan-agent

%description
AutoScan is an application designed to explore and to manage your network. 
Entire subnets can be scanned simultaneously without human intervention. 
It features OS detection, automatic network discovery, a port scanner, 
a Samba share browser, and the ability to save the network state.

%package 	%{daemon}
Group: 		Networking/Other
Summary: 	AutoScan daemon
Provides: 	%name = %version-%release

%description 	%{daemon}
Scans network in the background


%prep  

%setup -q -a 0
%patch0

%build
./configure mandriva
%make AutoScan_Agent
%make AutoScan_Network 

%install
rm -rf %{buildroot}

#Daemon install
install -d %{buildroot}/usr/sbin/
install -d %{buildroot}/etc/rc.d/init.d/
install -m755 src/AutoScan_Agent/AutoScan_Agent %{buildroot}/usr/sbin/
install -m755 init.d/autoscan_mandriva %{buildroot}/etc/rc.d/init.d/autoscan

#Gui install
install -d %{buildroot}/usr/share/doc/AutoScan/
install -d %{buildroot}/usr/share/pixmaps/AutoScan/
install -d %{buildroot}/usr/share/apps/AutoScan/
install -d %{buildroot}/usr/lib/menu/
install -d %{buildroot}/usr/bin/
install -d %{buildroot}/usr/share/icons/
install -d %{buildroot}/usr/share/sounds/AutoScan/
install -d %{buildroot}/usr/share/applications/

pwd
install -m755 src/AutoScan/AutoScan_Network_Gui %{buildroot}/usr/bin/
install -m755 Script/* %{buildroot}/usr/bin/
cp -R usr/* %{buildroot}/usr/

#file listed twice
rm %{buildroot}/usr/share/doc/AutoScan/copyright

#drop old debian menu included in tarball
rm -rf %{buildroot}/usr/lib/menu

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --remove-key="MultipleArgs" \
  --add-category="Settings" \
  --add-category="X-MandrivaLinux-System-Configuration-Networking" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

%clean
rm -rf %{buildroot}


%post %{daemon}
%_post_service %{oname}


%postun %{daemon}
%_preun_service %{oname}


%post
export GCONF_CONFIG_SOURCE="$(gconftool-2 --get-default-source)"
%post_install_gconf_schemas %{name}
%update_menus


%postun
%clean_menus


%files %{daemon}
%defattr(755,root,root)
%{_sbindir}/AutoScan_Agent
%{_initrddir}/%{oname}

%files
%defattr(755,root,root)
%doc AUTHORS CHANGELOG copyright
%{_bindir}/%{name}_Network
%{_bindir}/%{name}_Network_Gui
%{_bindir}/%{name}_Network_Error.sh
%{_datadir}/apps/%{name}/*
%{_datadir}/pixmaps/%{name}/*
%{_iconsdir}/*
%{_datadir}/sounds/%{name}/*  
%{_datadir}/applications/*.desktop

