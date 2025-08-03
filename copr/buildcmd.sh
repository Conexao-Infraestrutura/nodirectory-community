#!/usr/bin/bash

SAMBA_VERSAO='4.22.3'
NDS_VERSAO='0.1'
NDS_NOME='ndserver-ad'

curl -O -L https://github.com/samba-team/samba/archive/refs/tags/samba-${SAMBA_VERSAO}.tar.gz
curl -O https://raw.githubusercontent.com/Conexao-Infraestrutura/nodirectory-community/refs/heads/main/copr/ndserver-ad.spec
tar xzf samba-${SAMBA_VERSAO}.tar.gz
mv samba-samba-${SAMBA_VERSAO} ${NDS_NOME}-${NDS_VERSAO}.${SAMBA_VERSAO}
tar czf ~/build/SOURCES/${NDS_NOME}-${NDS_VERSAO}.${SAMBA_VERSAO}.tar.gz ${NDS_NOME}-${NDS_VERSAO}.${SAMBA_VERSAO}
rpmbuild -bb ndserver-ad.spec
