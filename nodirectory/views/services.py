from pyramid.view import view_config
from .security import logged
import psutil

# - Check process on system
def processIsRun(process_name):
    for proc in psutil.process_iter():
        try:
            if process_name in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

# - default page
@view_config (
    route_name = 'service',
    renderer = 'nodirectory:templates/services.jinja2',
)

def service(request):

    # Verify if there is a session
    logged(request, request.session)

    return {
        'title': 'Service',
        'autor': 'ConexInfra',
        'project': 'NoDirectory',
        }

# - List service status
@view_config (
    route_name = 'servicelist',
    renderer = 'json'
)

def servicelist(request):

    # Verify if there is a session
    logged(request, request.session)

    service = []
    state = []

    if processIsRun('smbd'):
        service.append('samba')
        state.append('running')
    else:
        service.append('samba')
        state.append('stopped')

    if processIsRun('slapd'):
        service.append('openldap')
        state.append('running')
    else:
        service.append('openldap')
        state.append('stopped')

    dict_to_return = []
    for i in range(0, len(service)):
        dict_to_return.append([service[i], state[i]])
    
    return {'services': dict_to_return}
