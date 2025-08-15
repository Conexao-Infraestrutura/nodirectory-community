CHROOT='centos-stream+epel-next-9-x86_64'

copr add-package-custom conexinfra/nodirectory-community \
    --name ndserver-ad \
    --script buildcmd.sh \
    --script-chroot "${CHROOT}" 

copr build-package conexinfra/nodirectory-community --name ndserver-ad
