from pyramid.view import view_config
from .security import logged

# - Return the name of a logged user
@view_config(
    route_name = 'loggeduser',
    renderer = 'json',
)

def loggeduser(request):

    # Verify if there is a session
    logged(request, request.session)

    return {'result': request.session['user'], 'message': ''}