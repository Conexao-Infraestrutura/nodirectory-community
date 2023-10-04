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

With the time we intended to rewrite the SmbLdap-Tools in Python and extend his capabilities, but remember!
We aren’t intended to extend all possible capabilities which OpenLdap have into NoDirectory.

So, stay tuned for more.

## How use it ?

There are 3 main variables:

**ND_MASTER_PASSWORD='ndserver'** => Which is the Manager Openlap ROOT administrator (***The default MASTER USER is always: Manager***)

**ND_MASTER_DOMAIN='dc=prototype,dc=foo,dc=bar'** => Which is the BASE DN of the main DNS TREE (***Usually***)

**ND_MASTER_NAME='ndserver'** => Which is de DNS name which will compose the FQDN for the PRIMARY server. (***Need a separete DNS SERVER***, check Bind, etc...)

The other parameters are ports, source networks and protocols, followed by the image name. Just do that as follow in a machine with docker installed, and you will be fine :)

After do this go to, http://your_ip_address:6543/

```
docker run -dit \
    -p 0.0.0.0:6543:6543/tcp \
    -p 0.0.0.0:389:389/tcp \
    -p 0.0.0.0:137:137/udp \
    -p 0.0.0.0:138:138/udp \
    -p 0.0.0.0:139:139/tcp \
    -p 0.0.0.0:445:445/tcp \
    -e ND_MASTER_PASSWORD='ndserver' \
    -e ND_MASTER_DOMAIN='dc=prototype,dc=foo,dc=bar' \
    -e ND_MASTER_NAME='ndserver' \
    felipediefenbach/nodirectory-community
```
