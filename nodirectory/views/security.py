import pyramid.httpexceptions as exc
import os

def logged(request, inputed_session):
    if os.getenv('ND_LOGIN_DISABLE'):
        if not request.session:
            request.session['user'] = 'Manager'
    else:
        if not inputed_session:
            raise exc.HTTPFound(request.route_url("login"))
        else:
            if not inputed_session['user']:
                raise exc.HTTPFound(request.route_url("login"))
            elif inputed_session['user'] == '':
                raise exc.HTTPFound(request.route_url("login"))

def logged_out(request):
    request.session.pop('user')
    raise exc.HTTPFound(request.route_url("login"))