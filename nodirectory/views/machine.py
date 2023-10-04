from pyramid.view import view_config
import subprocess
import uuid
import os
from .security import logged

default_domain = '.redecobaia.foo.bar'

# - default page
@view_config (
    route_name = 'machine',
    renderer = 'nodirectory:templates/machine.jinja2',
)

def machine(request):

    #logged(request, request.session)

    return {
        'title': 'Machine',
        'autor': 'ConexInfra',
        'project': 'NoDirectory',
        }

# - List of ingressed machines
@view_config (
    route_name = 'machinelist',
    renderer = 'json'
)

def machinelist(request):

    # Verify if there is a session
    logged(request, request.session)

    uids=[]
    machinenames=[]

    machines_list = subprocess.run(
        ['/usr/sbin/smbldap-userlist'],
        capture_output=True,
        text=True
    )
    
    smbldap_return = machines_list.stdout.splitlines()
    smbldap_return.pop(0)

    for lines in smbldap_return:
        cleanlines = lines.split('|')
        if len(cleanlines) > 1 and '$' in cleanlines[1]:
                uids.append(cleanlines[0])
                machinenames.append(cleanlines[1].replace('$', default_domain))

    return {'machinenames': machinenames, 'uids': uids}

# - Receive the uid and delete the machine
@view_config (
    route_name = 'machinedel',
    renderer = 'json',
)

def machinedel(request):

    # Verify if there is a session
    logged(request, request.session)
    
    machine_info_uid = request.params['uid']

    machines_list = subprocess.check_output(
        ['/usr/sbin/smbldap-userlist'],
    )

    smbldap_return = machines_list.decode('utf-8').splitlines()
    del smbldap_return[0]

    for lines in smbldap_return:
        cleanlines = lines.split('|')
        if len(cleanlines) > 1:
            if int(cleanlines[0]) == int(machine_info_uid):
                username = str(cleanlines[1])

    machines_delete = subprocess.run(
        ['/usr/sbin/smbldap-userdel', username],
        capture_output=True,
        text=True
    )

    if machines_delete.returncode == 0:
        result = 'ok'
        message = machines_delete.stdout
    else:
        result = 'err'
        message = machines_delete.stderr

    return {'result': result, 'message': message}

@view_config(
    route_name = 'machineadd',
    renderer = 'json',
)

def machineadd(request):

    def masterNameExtract(server_name, domain_name):
        geted_dom = str(domain_name).split(',')
        fqdn = str(server_name)
        for name in geted_dom:
            fqdn = fqdn + '.' + name[3:]
        return fqdn

    def callIngressCommand(auth_type, auth_pass, auth_sudo_pass, auth_cred):

        if str(auth_type).strip() == 'unchecked':

            server_name = os.getenv('ND_MASTER_NAME')
            domain_name = os.getenv('ND_MASTER_DOMAIN')
            mserver = masterNameExtract(server_name, domain_name)
            ansible_pass = str(auth_pass).strip()
            ansible_sudo = str(auth_pass).strip()
            ansible_user = str(auth_cred.split('@')[0]).strip()
            ansible_target = str(auth_cred.split('@')[1]).strip()

            ansible_cmd = f'ansible-playbook -i {ansible_target}, \
                -e "ansible_user={ansible_user}" \
                -e "ansible_password={ansible_pass}" \
                -e "ansible_sudo_pass={ansible_sudo}" \
                -e "master_server={mserver}" \
                /srv/include/linux-remote-ingress.yml'
            
            ansible_return = subprocess.run(
                [ansible_cmd],
                capture_output=True,
                text=True,
                shell=True,
            )

            return ansible_return

        else:
            sshkey_filename = '/tmp/sshkey_' + str(uuid.uuid4())
            with open(sshkey_filename, 'w') as ansible_pass:
                ansible_pass.write(auth_pass)
            ansible_pass.close()
            os.chmod(sshkey_filename, 0o600)
            
            server_name = os.getenv('ND_MASTER_NAME')
            domain_name = os.getenv('ND_MASTER_DOMAIN')
            mserver = masterNameExtract(server_name, domain_name)
            ansible_sudo = str(auth_sudo_pass).strip()
            ansible_user = str(auth_cred.split('@')[0]).strip()
            ansible_target = str(auth_cred.split('@')[1]).strip()

            ansible_cmd = f'ansible-playbook -i {ansible_target}, \
                -e "ansible_user={ansible_user}" \
                -e "ansible_ssh_private_key_file={sshkey_filename}" \
                -e "ansible_sudo_pass={ansible_sudo}" \
                -e "master_server={mserver}" \
                /srv/include/linux-remote-ingress.yml'
             
            ansible_return = subprocess.run(
                [ansible_cmd],
                capture_output=True,
                text=True,
                shell=True,
            )

            os.remove(sshkey_filename)            
            return ansible_return

    inputed_credentials = request.params['cred']
    inputed_password = request.params['auth']
    inputed_sudo_password = request.params['sudo']
    selected_pass_or_key = request.params['passkey']

    smbldap_ingress_machine = callIngressCommand(selected_pass_or_key, inputed_password, inputed_sudo_password, inputed_credentials)
    print(smbldap_ingress_machine)

    if smbldap_ingress_machine.returncode == 0:
        smbldap_ingress_machine_name = str(inputed_credentials.split('@')[1]).strip()
        smbldap_ingress_machine_cmd = f'/usr/sbin/smbldap-useradd -w {smbldap_ingress_machine_name}'
        smbldap_create_machine = subprocess.run(
            [smbldap_ingress_machine_cmd],
            capture_output=True,
            text=True,
            shell=True,
        )
    else:
        result = 'err'
        message = smbldap_ingress_machine.stdout
        return {'result': result, 'message': message}

    if smbldap_create_machine.returncode == 0:
        result = 'ok'
        message = smbldap_create_machine.stdout
    else:
        result = 'err'
        message = smbldap_create_machine.stderr

    return {'result': result, 'message': message}