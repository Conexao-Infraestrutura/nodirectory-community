Name:           ndserver-ad
Version:        0.1.4.22.3
Release:        0.%(bash -c 'date +%s')%{?dist}
Summary:        NDServer-AD Official Release
Source0:        %{name}-%{version}.tar.gz
License:        GPLv3+
URL:            https://github.com/Conexao-Infraestrutura/nodirectory-community

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
