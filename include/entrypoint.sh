#!/bin/bash
[[ ${ND_BUILD_ENVIRONMENT} == 'dev' ]] && set -x

# - Inicia o serviço do ldap
# https://github.com/moby/moby/issues/8231 - it seems to be an issue with user limits
# I tryed this in conteiner level but seem not work to, so I introduce this workround here
ulimit -n 1024 && /usr/sbin/slapd -u ldap -h "ldap:/// ldaps:/// ldapi:///"

[[ -e /var/lib/ldap/initialized ]] || {

    # - Extract netbios workgroup
    WK=$(tr '[:lower:]' '[:upper:]' <<<"$(cut -d '=' -f 2 <<<"$(cut -d ',' -f 1 <<<"${ND_MASTER_DOMAIN}")")")

    for file in config.ldif raiz.ldif ldap.conf smb.conf smbldap.conf smbldap_bind.conf
    do
        sed "s/WORKGROUP/${WK}/g" -i /srv/include/${file}
        sed "s/ND_MASTER_DOMAIN/${ND_MASTER_DOMAIN}/g" -i /srv/include/${file}
        sed "s/ND_MASTER_PASSWORD/${ND_MASTER_PASSWORD}/g" -i /srv/include/${file}
    done

    # - Hash ldap Manager password
    MP=$(slappasswd -s "$(echo -n "${ND_MASTER_PASSWORD}")")
    echo "olcRootPW: ${MP}" >> /srv/include/config.ldif

    # - Configure Openldap
    ldapadd -Y EXTERNAL -H ldapi:/// -f /srv/include/config.ldif

    # - Add schemas
    ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/cosine.ldif
    ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/nis.ldif
    ldapadd -Y EXTERNAL -H ldapi:/// -f /etc/openldap/schema/inetorgperson.ldif
    ldapadd -Y EXTERNAL -H ldapi:/// -f /usr/share/doc/samba/LDAP/samba.ldif

    # - Add root DNS for net getlocalsid
    ldapadd -x -w "${ND_MASTER_PASSWORD}" -D "cn=Manager,${ND_MASTER_DOMAIN}" -f /srv/include/raiz.ldif
    touch /var/lib/ldap/initialized

    # - Configure samba
    /bin/mv /etc/samba/smb.conf /etc/samba/smb.conf.org
    /bin/cp /srv/include/smb.conf /etc/samba/smb.conf
    smbpasswd -w "$(echo -n "${ND_MASTER_PASSWORD}")"
    SAMBASID=$(net getlocalsid | cut -d ':' -f 2 | tr -d '[:blank:]')

    # - Configre smbldap-tools
    /bin/mv /etc/smbldap-tools/smbldap.conf /etc/smbldap-tools/smbldap.conf.org
    /bin/cp /srv/include/smbldap.conf /etc/smbldap-tools/smbldap.conf
    echo "SID=\"${SAMBASID}\"" >> /etc/smbldap-tools/smbldap.conf
    /bin/mv /etc/smbldap-tools/smbldap_bind.conf /etc/smbldap-tools/smbldap_bind.conf.org
    /bin/cp /srv/include/smbldap_bind.conf /etc/smbldap-tools/smbldap_bind.conf

    # - We run populate and set the root password
    # bug in smbldap-populate, when extracting the ldif for import, later is giving a defect
    # when getting the number of the next gid (smbldap-populate -e /tmp/smbldaptools.ldif)
    # Failed to find sambaUnixIdPool to get next gidNumber at /usr/share/perl5/vendor_perl/smbldap_tools.pm line 1195.
    # So I'll comment out the password request for now and then fix the bug in the utility rewrite
    sed '506,507{s/^/##/}' -i /usr/sbin/smbldap-populate
    smbldap-populate
    smbldap-passwd -p root <<<"$(echo -n "${ND_MASTER_PASSWORD}")"

    # - There is a bug in smbldap-userdel
    # the correct function to get DN need to be less restrictive
    # in search on the tree to get users as machines
    # so at line: 742 in the: /usr/share/perl5/vendor_perl/smbldap_tools.pm
    # we need get_user_dn2() instead get_user_dn()
    sed '742s/get_user_dn/get_user_dn2/' -i /usr/share/perl5/vendor_perl/smbldap_tools.pm

    # - Configure sssd and oddjobd
    /bin/mv /etc/openldap/ldap.conf /etc/openldap/ldap.conf.org
    /bin/cp /srv/include/ldap.conf /etc/openldap/ldap.conf
    /bin/cp /srv/include/sssd.conf /etc/sssd/sssd.conf
    chmod 600 /etc/sssd/sssd.conf
    chown root:root /etc/sssd/sssd.conf
    authselect select sssd --force

}

# - Start sssd and oddjobd
/usr/sbin/sssd -D

# - Start samba
/usr/sbin/smbd -D
/usr/sbin/nmbd -D

case ${ND_BUILD_ENVIRONMENT} 
in
    prod)
        # start in prod mode (all supressed)
        cd /srv && pserve production.ini || exit 1
    ;;
    dev)
        # start in devel mode (full log)
        cd /srv && pserve development.ini --reload || exit 1
    ;;
    *)
        # Default is in prod mode (all supressed)
        cd /srv && pserve production.ini || exit 1
    ;;
esac