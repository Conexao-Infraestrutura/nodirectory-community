#!/usr/bin/bash

SAMBA_VERSAO='4.22.3'
NDS_VERSAO='0.1'
NDS_NOME='ndserver-ad'

# get build elements spec/sources
curl -O -L https://github.com/samba-team/samba/archive/refs/tags/samba-${SAMBA_VERSAO}.tar.gz
curl -O https://raw.githubusercontent.com/Conexao-Infraestrutura/nodirectory-community/refs/heads/main/copr/ndserver-ad.spec

# extract/rename/compress/delete
tar xzf samba-${SAMBA_VERSAO}.tar.gz
mv samba-samba-${SAMBA_VERSAO} ${NDS_NOME}-${NDS_VERSAO}.${SAMBA_VERSAO}
tar czf ${NDS_NOME}-${NDS_VERSAO}.${SAMBA_VERSAO}.tar.gz ${NDS_NOME}-${NDS_VERSAO}.${SAMBA_VERSAO}
rm -rf samba-samba-${SAMBA_VERSAO} samba-${SAMBA_VERSAO}.tar.gz
