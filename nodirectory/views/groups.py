from pyramid.view import view_config
from .security import logged
import subprocess

# - default page
@view_config (
    route_name = 'group',
    renderer = 'nodirectory:templates/groups.jinja2',
)

def group(request):

    # Verify if there is a session
    logged(request, request.session)

    return {
        'title': 'Group',
        'autor': 'ConexInfra',
        'project': 'NoDirectory',
        }

# - Return the current list of groups in openldap
@view_config (
    route_name = 'grouplist',
    renderer = 'json',
)

def grouplist(request):

    # Verify if there is a session
    logged(request, request.session)

    gids=[]
    groupnames=[]

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
            gids.append(cleanlines[0])
            groupnames.append(cleanlines[1])

    return {'groupnames': groupnames, 'gids': gids}

# - Receive the gid and return group info
@view_config (
    route_name = 'groupinfo',
    renderer = 'json',
)

def groupinfo(request):

    # Verify if there is a session
    logged(request, request.session)
    
    group_info_gid = request.params['gid']

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
            if int(cleanlines[0]) == int(group_info_gid):
                groupname = str(cleanlines[1])

    groups_show = subprocess.run(
        ['/usr/sbin/smbldap-groupshow', groupname],
        capture_output=True,
        text=True
    )

    smbldap_return = groups_show.stdout.splitlines()

    return {'info': smbldap_return}

# - Receive the gid and delete the group
@view_config (
    route_name = 'groupdel',
    renderer = 'json',
)

def groupdel(request):

    # Verify if there is a session
    logged(request, request.session)

    group_info_gid = request.params['gid']

    groups_list = subprocess.check_output(
        ['/usr/sbin/smbldap-grouplist'],
    )

    smbldap_return = groups_list.decode('utf-8').splitlines()
    del smbldap_return[0]

    for lines in smbldap_return:
        cleanlines = lines.split('|')
        if len(cleanlines) > 1:
            if int(cleanlines[0]) == int(group_info_gid):
                groupname = str(cleanlines[1])

    groups_delete = subprocess.run(
        ['/usr/sbin/smbldap-groupdel', groupname],
        capture_output=True,
        text=True
    )

    if groups_delete.returncode == 0:
        result = 'ok'
        message = groups_delete.stdout
    else:
        result = 'err'
        message = groups_delete.stderr

    print({'result': result, 'message': message})
    return {'result': result, 'message': message}
    
# - Added a new group
@view_config (
    route_name = 'groupadd',
    renderer = 'json',
)

def groupadd(request):

    # Verify if there is a session
    logged(request, request.session)

    input_groupname = str(request.params['groupname'])
    input_smbgroup = str(request.params['smbgroup'])

    if input_smbgroup.strip() == 'checked':
        
        groups_add = subprocess.run(
            ['/usr/sbin/smbldap-groupadd', '-a', input_groupname.strip()],
            capture_output=True,
            text=True,
        )
        
        if groups_add.returncode == 0:
            result = 'ok'
            message = groups_add.stdout
        else:
            result = 'err'
            message = groups_add.stderr

    if input_smbgroup.strip() == 'unchecked':

        groups_add = subprocess.run(
            ['/usr/sbin/smbldap-groupadd', input_groupname.strip()],
            capture_output=True,
            text=True,
        )

        if groups_add.returncode == 0:
            result = 'ok'
            message = groups_add.stdout
        else:
            result = 'err'
            message = groups_add.stderr

    return {'result': result, 'message': message}