Name:           ndserver-ad
Version:        0.1.4.22.3
Release:        0.%(bash -c 'date +%s')%{?dist}
Summary:        NDServer-AD Official Release
Source0:        %{name}-%{version}.tar.gz
License:        GPLv3+
URL:            https://github.com/Conexao-Infraestrutura/nodirectory-community

BuildRequires: acl
BuildRequires: attr
BuildRequires: autoconf
BuildRequires: avahi-devel
BuildRequires: bind-utils
BuildRequires: binutils
BuildRequires: bison
BuildRequires: cargo
BuildRequires: ccache
BuildRequires: chrpath
BuildRequires: clang-devel
BuildRequires: crypto-policies-scripts
BuildRequires: cups-devel
BuildRequires: dbus-devel
BuildRequires: docbook-dtds
BuildRequires: docbook-style-xsl
BuildRequires: flex
BuildRequires: gawk
BuildRequires: gcc
BuildRequires: gdb
BuildRequires: git
BuildRequires: glib2-devel
BuildRequires: glibc-common
BuildRequires: glibc-langpack-en
BuildRequires: gnutls-devel
BuildRequires: gnutls-utils
BuildRequires: gpgme-devel
BuildRequires: gzip
BuildRequires: hostname
BuildRequires: htop
BuildRequires: jansson-devel
BuildRequires: jq
BuildRequires: keyutils-libs-devel
BuildRequires: krb5-devel
BuildRequires: krb5-server
BuildRequires: krb5-workstation
BuildRequires: libacl-devel
BuildRequires: libarchive-devel
BuildRequires: libattr-devel
BuildRequires: libblkid-devel
BuildRequires: libbsd-devel
BuildRequires: libcap-devel
BuildRequires: libicu-devel
BuildRequires: libpcap-devel
BuildRequires: libtasn1-devel
BuildRequires: libtasn1-tools
BuildRequires: libtirpc-devel
BuildRequires: libunwind-devel
BuildRequires: liburing-devel
BuildRequires: libuuid-devel
BuildRequires: libxslt
BuildRequires: lmdb
BuildRequires: lmdb-devel
BuildRequires: lsb_release
BuildRequires: make
BuildRequires: mingw64-gcc
BuildRequires: ncurses-devel
BuildRequires: openldap-devel
BuildRequires: openssl-devel
BuildRequires: pam-devel
BuildRequires: patch
BuildRequires: perl
BuildRequires: perl-Archive-Tar
BuildRequires: perl-ExtUtils-MakeMaker
BuildRequires: perl-Parse-Yapp
BuildRequires: perl-Test-Simple
BuildRequires: perl-generators
BuildRequires: perl-interpreter
BuildRequires: pkgconfig
BuildRequires: popt-devel
BuildRequires: procps-ng
BuildRequires: psmisc
BuildRequires: python3
BuildRequires: python3-cryptography
BuildRequires: python3-devel
BuildRequires: python3-dns
BuildRequires: python3-gpg
BuildRequires: python3-iso8601
BuildRequires: python3-libsemanage
BuildRequires: python3-markdown
BuildRequires: python3-policycoreutils
BuildRequires: python3-pyasn1
BuildRequires: python3-requests
BuildRequires: python3-setproctitle
BuildRequires: quota-devel
BuildRequires: readline-devel
BuildRequires: rng-tools
BuildRequires: rpcgen
BuildRequires: rpcsvc-proto-devel
BuildRequires: rsync
BuildRequires: sed
BuildRequires: sudo
BuildRequires: systemd-devel
BuildRequires: tar
BuildRequires: tracker-devel
BuildRequires: tree
BuildRequires: utf8proc-devel
BuildRequires: wget
BuildRequires: which
BuildRequires: xfsprogs-devel
BuildRequires: xz
BuildRequires: yum-utils
BuildRequires: zlib-devel

Requires:       python3-cryptography
Requires:       python3-markdown
Requires:       python3-dns

%description
A Centos Stream 9 Compile of NDServer-AD

%prep
%autosetup

%build
%configure \
    --with-systemd \
    --with-shared-modules=ALL \
    --with-ads \
    --with-acl-support \
    --with-pam \
    --with-syslog \
    --with-quotas \
    --with-winbind \
    --enable-fhs \
    --prefix=/srv/%{name}/usr \
    --sysconfdir=/srv/%{name}/etc \
    --localstatedir=/srv/%{name}/var \
    --libdir=/srv/%{name}/usr/lib64 \
    --with-piddir=/srv/%{name}/run/samba \
    --with-privatedir=/srv/%{name}/var/lib/samba/private \
    --with-statedir=/srv/%{name}/var/lib/samba \
    --with-cachedir=/srv/%{name}/var/cache/samba \
    --exec-prefix=/srv/%{name}/usr \
    --bindir=/srv/%{name}/usr/bin \
    --sbindir=/srv/%{name}/usr/sbin \
    --datadir=/srv/%{name}/usr/share \
    --includedir=/srv/%{name}/usr/include \
    --libexecdir=/srv/%{name}/usr/libexec \
    --localstatedir=/srv/%{name}/var \
    --sharedstatedir=/srv/%{name}/var/lib \
    --mandir=/srv/%{name}/usr/share/man \
    --infodir=/srv/%{name}/usr/share/info \

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}
cp -r bin/default/packaging/systemd/samba.service %{buildroot}/srv/%{name}/%{name}.service

%files
/srv/%{name}/*

%post
cp -f /srv/%{name}/%{name}.service /usr/lib/systemd/system/%{name}.service >/dev/null 2>&1 || :
if [ $1 -ge 1 ]; then  # Run on both install and upgrade
    systemctl daemon-reload >/dev/null 2>&1 || :
    systemctl try-restart %{name}.service >/dev/null 2>&1 || :
fi

if [ $1 -eq 1 ]; then  # Only on fresh install
    systemctl enable %{name}.service >/dev/null 2>&1 || :
fi

%changelog
* Tue Jul 01 2025 Conex Infra <conexinfra@gmail.com> - 0.1
- Initial package for CentOS 9 Stream NDServer
