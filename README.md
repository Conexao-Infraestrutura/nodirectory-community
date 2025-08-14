# NoDirectory community edition

A simple Openldap User/Group Management for Linux and Samba.

NoDirectory is conceived to be a "ridiculously simple implementation" to substitute
an old group of software's used to manage directory systems.

The project was built in Python 3.XX, Pyramid 2.XX and Bootstrap 5.XX and acts like
a web interface for the SmbLdap-Tools, which is normally the base to build a SMB-PDC,

To achieve this implementation commonly both PHPLdapAdmin and SmbLdap-Tools 
have to be used, but they are no longer update or improved for a long time.

In this direction, NoDirectory aim to be modern web interface to substitute 
PHPLdapAdmin and additionally manage just not only OpenLdap stuff, but services, 
users, passwords, groups, clients, and other future stuff,

If you need a **complete solution focused in directory services** NoDirectory isn’t what you looking for! 

In this case check [Freeipa Project](https://www.freeipa.org/).

If you need a **complete solution focused in SMB services** NoDirectory isn’t what you looking for too!

In this case check [Fedora and SambaTool](https://fedoramagazine.org/samba-as-ad-and-domain-controller/). 
 
**But if you need Linux client authentication and SMB client authentication with web and command-line interface for Samba and OpenLdap.** 

**Them YES !! NoDirectory is what you looking for** !!

With the time we intended to rewrite the SmbLdap-Tools in Python and extend his capabilities.
But remember! We aren’t intended to extend all possible capabilities which OpenLdap have into NoDirectory.

So, stay tuned for more.

## How use it ?

First off all:

This was tested in [Centos Stream 9](https://mirror.stream.centos.org/9-stream/BaseOS/x86_64/iso), with Firewalld and Selinux active.

Samba Custom compile by DNF

```
curl -L https://raw.githubusercontent.com/conexao-infraestrutura/nodirectory-community/refs/heads/main/dnf/ndserver.repo -o /etc/yum.repos.d/ndserver.repo
dnf -y install epel-release && dnf -y install ndserver-ad
```

Install [Docker](https://docs.docker.com/engine/install/centos/) as usually.

Then build your environment file:
```
cat << EOF > /usr/local/etc/ndserver_environment
ND_MASTER_PASSWORD='ndserver'
ND_MASTER_DOMAIN='dc=prototype,dc=foo,dc=bar'
ND_MASTER_NAME='ndserver'
EOF
```

Add the rules to Firewalld:
```
firewall-cmd --zone public --add-port=6543/tcp --permanent \
firewall-cmd --zone public --add-service=samba --permanent \
firewall-cmd --reload
```

Run your NDserver:
```
docker run -dit \
  --privileged \
  --net=host \
  -v /usr/local/etc/ndserver_environment:/etc/ndserver_env \
  felipediefenbach/nodirectory-community:latest
```

When you done, you should be able to access the web interface by your web browser at: http://some_ip_address:6543

## Addicional Information:

There are 3 main variables:

**ND_MASTER_PASSWORD='ndserver'** => Which is the Manager Openlap ROOT administrator (***The default MASTER USER is always: Manager***)

**ND_MASTER_DOMAIN='dc=prototype,dc=foo,dc=bar'** => Which is the BASE DN of the main DNS TREE (***Usually***)

**ND_MASTER_NAME='ndserver'** => Which is de DNS name which will compose the FQDN for the PRIMARY server. (***Need a separete DNS SERVER***, check Bind, etc...)

Addicionally (and normally) you cloud be do this in a router-box, which cloud be include the masquerade setup to Firewalld, like that:

```
firewall-cmd --zone public --add-interface=enpXsX --permanent \
firewall-cmd --zone public --add-masquerade --permanent \
firewall-cmd --reload
```

