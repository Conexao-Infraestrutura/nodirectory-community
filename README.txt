NoDirectory

Simple docker use:

docker login felipediefenbach
pass: ***********

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
    felipediefenbach/nodirectory