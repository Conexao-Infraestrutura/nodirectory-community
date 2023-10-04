FROM quay.io/centos/centos:stream9

ENV TZ='America/Sao_paulo'
RUN echo 'alias ll="ls -lh --color=auto"' >> /etc/bashrc

WORKDIR /srv
COPY . /srv/

RUN dnf -y install epel-release
RUN dnf --nobest -y install \
python3.11-pip \
perl \
samba \
openldap \
openldap-servers \
openldap-devel \
openldap-clients \
sssd \
sssd-ldap \
openssl-perl \
authselect \
git \
vim \
procps-ng \
htop \
iputils \
ansible \
chromedriver \
chromium

RUN dnf -y localinstall /srv/perl-Crypt-SmbHash-0.12-42.fc34.noarch.rpm 
RUN dnf -y localinstall /srv/smbldap-tools-0.9.11-18.fc34.noarch.rpm
RUN rm /srv/*.rpm

ENV ANSIBLE_HOST_KEY_CHECKING=False
ENV ND_LOGIN_DISABLE=False
ENV ND_MASTER_PASSWORD=''
ENV ND_MASTER_DOMAIN=''
ENV ND_MASTER_NAME=''

WORKDIR /srv
COPY . /srv/

ENV VIRTUAL_ENV=/srv/venv
RUN python3.11 -m venv ${VIRTUAL_ENV}
ENV PATH="${VIRTUAL_ENV}/bin:$PATH"
RUN pip install --upgrade pip setuptools
RUN pip install -e .

RUN chmod 755 /srv/include/entrypoint.sh
ENTRYPOINT ["/srv/include/entrypoint.sh"]
