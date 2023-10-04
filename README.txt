NoDirectory

    NoDirectory is conceived to be a "ridiculously simple implementation" to substitute
an old conjunct of software's used to manage directory systems integrated 
with a “nom proprietary” samba tools.

    The project was built in Python 3.XX, Pyramid 2.XX, Bootstrap 5.XX, and acts like
a web interface for the SmbLdap-Tools, which is normally the base to build a PDC
and control a SMB based Network.

    To achieve this implementation, commonly both PHPLdapAdmin and SmbLdap-Tools 
have to be used, but they are no longer update or improved for a long time, 
and just be recompiled over and over again across many distributions.

    In this direction, NoDirectory aim to be modern web interface to substitute 
PHPLdapAdmin and additionally manage just not only OpenLdap stuff, but too, services, 
users, passwords, groups, clients, and other future stuff needed in SMB and Linux
network authentication systems

    If you need a complete solution focused in directory services, 
NoDirectory isn’t for you ! In this case check Freeipa Project.

    If you need a complete solution focused in SMB services, 
NoDirectory isn’t for you too ! In this case check Fedora 38 and SambaTool. 
 
    But if need Linux client authentication and/or SMB client authentication
with web and command-line interface and Samba and OpenLdap, them YES, NoDirectory is what you looking for.

    With the time, we intended to rewrite the SmbLdap-Tools in Python and extend his capabilities, 
but remember ! We aren’t intended to extend all possible capabilities which OpenLdap have.

So, stay tuned for more.

Simple docker use:

    docker run -dit \
        -p 0.0.0.0:6543:6543/tcp \
        -p 0.0.0.0:389:389/tcp \
        -p 0.0.0.0:137:137/udp \
        -p 0.0.0.0:138:138/udp \
        -p 0.0.0.0:139:139/tcp \
        -p 0.0.0.0:445:445/tcp \
        nodirectory