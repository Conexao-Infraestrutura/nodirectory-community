from pyramid.view import view_config
from .security import logged
import subprocess

# - default page
@view_config (
    route_name = 'user',
    renderer = 'nodirectory:templates/users.jinja2',
)

def user(request):

    # Verify if there is a session
    logged(request, request.session)

    return {
        'title': 'Users',
        'autor': 'ConexInfra',
        'project': 'NoDirectory',
        }

# - Return the current list of users in openldap
@view_config (
    route_name = 'userlist',
    renderer = 'json',
)

def userlist(request):

    # Verify if there is a session
    logged(request, request.session)

    uids=[]
    usernames=[]

    users_list = subprocess.run(
        ['/usr/sbin/smbldap-userlist'],
        capture_output=True,
        text=True
    )
    
    smbldap_return = users_list.stdout.splitlines()
    smbldap_return.pop(0)

    for lines in smbldap_return:
        cleanlines = lines.split('|')
        if len(cleanlines) > 1 and '$' not in cleanlines[1]:
                uids.append(cleanlines[0])
                usernames.append(cleanlines[1])

    return {'usernames': usernames, 'uids': uids}

# - Receive the uid and return user info
@view_config (
    route_name = 'userinfo',
    renderer = 'json',
)

def userinfo(request):
    
    # Verify if there is a session
    logged(request, request.session)

    user_info_uid = request.params['uid']

    users_list = subprocess.run(
        ['/usr/sbin/smbldap-userlist'],
        capture_output=True,
        text=True
    )
    
    smbldap_return = users_list.stdout.splitlines()
    smbldap_return.pop(0)

    for lines in smbldap_return:
        cleanlines = lines.split('|')
        if len(cleanlines) > 1:
            if int(cleanlines[0]) == int(user_info_uid):
                username = str(cleanlines[1])

    users_show = subprocess.run(
        ['/usr/sbin/smbldap-usershow', username],
        capture_output=True,
        text=True
    )

    smbldap_return = users_show.stdout.splitlines()

    return {'info': smbldap_return}

# - Receive the uid and delete the user
@view_config (
    route_name = 'userdel',
    renderer = 'json',
)

def userdel(request):

    # Verify if there is a session
    logged(request, request.session)
    
    user_info_uid = request.params['uid']

    users_list = subprocess.check_output(
        ['/usr/sbin/smbldap-userlist'],
    )

    smbldap_return = users_list.decode('utf-8').splitlines()
    del smbldap_return[0]

    for lines in smbldap_return:
        cleanlines = lines.split('|')
        if len(cleanlines) > 1:
            if int(cleanlines[0]) == int(user_info_uid):
                username = str(cleanlines[1])

    users_delete = subprocess.run(
        ['/usr/sbin/smbldap-userdel', username],
        capture_output=True,
        text=True
    )

    if users_delete.returncode == 0:
        result = 'ok'
        message = users_delete.stdout
    else:
        result = 'err'
        message = users_delete.stderr

    return {'result': result, 'message': message}
    
# - Adds a new user
@view_config (
    route_name = 'useradd',
    renderer = 'json',
)

def useradd(request):

    logged(request, request.session)

    input_smbuser = str(request.params['smbuser'])
    input_username = str(request.params['username'])
    input_primgroup = int(request.params['primgroup'])
    input_supgroups = request.params['supgroups']

    def translateGid(gid):
        groups_list = subprocess.run(
            ['/usr/sbin/smbldap-grouplist'],
            capture_output=True,    
            text=True
        )
    
        smbldap_return = groups_list.stdout.splitlines()
        smbldap_return.pop(0)

        for lines in smbldap_return:
            cleanlines = lines.split('|')
            if len(cleanlines) > 1:
                if int(cleanlines[0]) == int(gid):
                    return str(cleanlines[1]).strip()

    smbldap_comp_groups = []

    for g in input_supgroups.split(','):
        if int(g) != input_primgroup:
            smbldap_comp_groups.append(translateGid(g))

    primary_group =  translateGid(input_primgroup)
    compplementary_group = ','.join(smbldap_comp_groups)

    if input_smbuser.strip() == 'checked':
        
        users_add = subprocess.run(
            ['/usr/sbin/smbldap-useradd', '-g', primary_group, '-G', compplementary_group, '-a', input_username.strip()],
            capture_output=True,
            text=True,
        )
        
        if users_add.returncode == 0:
            result = 'ok'
            message = users_add.stdout
        else:
            result = 'err'
            message = users_add.stderr

    if input_smbuser.strip() == 'unchecked':

        users_add = subprocess.run(
            ['/usr/sbin/smbldap-useradd', '-g', primary_group, '-G', compplementary_group, input_username.strip()],
            capture_output=True,
            text=True,
        )

        if users_add.returncode == 0:
            result = 'ok'
            message = users_add.stdout
        else:
            result = 'err'
            message = users_add.stderr

    return {'result': result, 'message': message}

# - Change pass of an user
@view_config(
    route_name = 'userpass',
    renderer = 'json',
)

def userpass(request):
    
    # Verify if there is a session
    logged(request, request.session)

    input_uid = int(request.params['uid'])
    input_pass = str(request.params['pass'])

    def translateUid(uid):
        users_list = subprocess.run(
            ['/usr/sbin/smbldap-userlist'],
            capture_output=True,    
            text=True
        )
    
        smbldap_return = users_list.stdout.splitlines()
        smbldap_return.pop(0)

        for lines in smbldap_return:
            cleanlines = lines.split('|')
            if len(cleanlines) > 1:
                if int(cleanlines[0]) == int(uid):
                    return str(cleanlines[1]).strip()

    change_user = translateUid(input_uid)

    users_pass = subprocess.run(
        ['/usr/sbin/smbldap-passwd', '-p', change_user],
        input=input_pass.strip(),
        capture_output=True,
        text=True,
    )

    if users_pass.returncode == 0:
        result = 'ok'
        message = users_pass.stdout
    else:
        result = 'err'
        message = users_pass.stderr

    return {'result': result, 'message': message}