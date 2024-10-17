%define	rname autoscan-network

Summary:	Utility for network exploration (Samba,Nessus client)
Name:		autoscan
Version:	1.50
Release: 	%mkrel 8
License:        GPLv2+
Group:		Networking/Other
URL:		https://autoscan-network.com/
Source0:	http://autoscan.fr/download_files/autoscan-network-%{version}.tar.gz
Source1:	autoscan-network.init
# this .xml file is missing in the tarball, and the GUI doesn't load without it
# mdv bug #58012
Source2:	Finger_Printing.xml
Patch0:		autoscan-1.41-x86_64-build-fix.patch
Patch1:		autoscan-1.50-fix-str-fmt.patch
BuildRequires:	gnomeui2-devel
BuildRequires:	libxml2-devel
BuildRequires:	openssl-devel
BuildRequires:	libao-devel
BuildRequires:	libvorbis-devel
BuildRequires:	net-snmp-devel
BuildRequires:	libtool
BuildRequires:	elfutils-devel
BuildRequires:	gtk+2-devel
BuildRequires:	libgnome-keyring-devel
BuildRequires:	gnome-vfs2-devel
BuildRequires:	glib-devel
BuildRequires:	vte-devel
BuildRequires:	desktop-file-utils
BuildRequires:	libcurl-devel
Requires:	webclient
Requires:	%{name}-agent
Provides:	%{rname} = %{version}
Obsoletes:	AutoScan
Provides:	AutoScan
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot 

%description
AutoScan is an application designed to explore and to manage your network. 
Entire subnets can be scanned simultaneously without human intervention. 
It features OS detection, automatic network discovery, a port scanner, 
and the ability to save the network state.

%package	agent
Summary:	AutoScan daemon
Group:		Networking/Other
Provides:	%{name} = %{version}-%{release}
Provides:	%{rname} = %{version}
Obsoletes:	%{rname}
Provides:	%{rname}-agent = %{version}
Obsoletes:	%{rname}-agent
Obsoletes:	AutoScan-agent < %version

%description	agent
Scans network in the background


%prep  
%setup -q -n %{rname}-%{version}
%patch0 -p0
%patch1 -p0

install -m 644 %{SOURCE2} %{_builddir}/%{rname}-%{version}/usr/share/apps/autoscan-network/

%build
./configure --distrib-mandriva
%make OPTIONS_COMPILE="%optflags %ldflags"

%install
rm -rf %{buildroot}

# Daemon install
install -d %{buildroot}%{_sbindir}/
install -d %{buildroot}%{_initrddir}/
install -m755 bin/autoscan-network-daemon %{buildroot}%{_sbindir}/
install -m755 %{SOURCE1} %{buildroot}%{_initrddir}/autoscan-network

# Gui install
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
  --dir %{buildroot}%{_datadir}/applications usr/share/applications/*.desktop

install -m644 usr/share/icons/autoscan-network.png %{buildroot}%{_iconsdir}
cp -r usr/share/pixmaps/autoscan-network/* %{buildroot}%{_datadir}/pixmaps/%{rname}/

install -m644 usr/share/apps/autoscan-network/* %buildroot%_datadir/apps/%{rname}
install -m 644 usr/share/sounds/autoscan-network/* %{buildroot}%{_datadir}/sounds/%{rname}/


%if %mdkversion < 200900
%post
%post_install_gconf_schemas %{name}
%update_menus
%endif

%if %mdkversion < 200900
%postun
%clean_menus
%endif

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
%doc AUTHORS 
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
