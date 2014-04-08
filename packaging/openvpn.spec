Name:       openvpn
Summary:    A full-featured SSL VPN solution
Version:    2.3.2
Release:    0
Group:      Security/Network
License:    GPL-2.0
URL:        http://openvpn.net/
Source0:    http://swupdate.openvpn.org/community/releases/%{name}-%{version}.tar.gz
Source1001: 	openvpn.manifest
BuildRequires:  lzo-devel
BuildRequires:  openssl-devel
BuildRequires:  pam-devel
BuildRequires:  iproute2
Requires:   	iproute2

%description
OpenVPN is a robust and highly flexible tunneling application that uses all
of the encryption, authentication, and certification features of the
OpenSSL library to securely tunnel IP networks over a single UDP or TCP
port.  It can use the Marcus Franz Xaver Johannes Oberhumer's LZO library
for compression.

%prep
%setup -q
cp %{SOURCE1001} .

%build
export CFLAGS
export LDFLAGS
%configure --disable-static \
    --enable-pthread \
    --enable-password-save \
    --enable-iproute2 \
    --with-ifconfig-path=/sbin/ifconfig \
    --with-iproute-path=/sbin/ip \
    --with-route-path=/sbin/route \
    CFLAGS="$CFLAGS -fPIE" \
    LDFLAGS="$LDFLAGS -pie"

make %{?jobs:-j%jobs}

%install
%make_install
install -d -m 0755 $RPM_BUILD_ROOT%{_sysconfdir}/%{name}

chmod -x sample/sample-scripts/*
chmod -x sample/sample-config-files/*
chmod -x contrib/openvpn-fwmarkroute-1.00/*

%post   -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%manifest %{name}.manifest
%defattr(-,root,root)
%license COPYING
%doc AUTHORS ChangeLog PORTS
%doc contrib sample/sample-keys sample/sample-scripts sample/sample-config-files
%{_mandir}/man8/%{name}.8*
%{_datadir}/doc/%{name}/
%{_sbindir}/%{name}
%{_libdir}/%{name}/
%config %dir %{_sysconfdir}/%{name}/
%{_includedir}/%{name}-plugin.h
%exclude %{_datadir}/doc/%{name}/COPYING

%changelog
