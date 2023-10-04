from pyramid.view import view_config
from .security import logged_out, logged
import subprocess
import hashlib
import base64

# - Validate LDAPPASS
def checkSecret(tagged_digest_salt, password):
    tagged_digest_salt = tagged_digest_salt.encode('utf-8')
    digest_salt_b64 = tagged_digest_salt[6:]
    digest_salt = base64.decodebytes(digest_salt_b64)
    digest = digest_salt[:20]
    salt = digest_salt[20:]
    sha = hashlib.sha1(password.encode('utf-8'))
    sha.update(salt)
    return digest == sha.digest()

# - default page
@view_config(
    route_name = 'login',
    renderer = 'nodirectory:templates/login.jinja2',
)

def login(request):
    return{
        'title': 'Login',
        'autor': 'ConexInfra',
        'project': 'NoDirectory',
    }

# - Challenge pass/user against LDAP e create a sessiom
@view_config(
    route_name = 'logsession',
    renderer = 'json',
)

def logsession(request):

    session = request.session
    user_name_info = request.params['sent_user']
    user_pass_info = request.params['sent_pass']

    admin_info = subprocess.run(
        ['ldapsearch -H ldapi:// -LLL -Q -Y EXTERNAL -b "cn=config" "(olcRootDN=*)" olcRootDN olcRootPW | tr -d "[:blank:]"'],
        capture_output=True,
        text=True,
        shell=True
        )
    
    ldap_return = admin_info.stdout.splitlines()
    ldap_return.pop(0)
    ldap_return.pop(-1)

    ldap_admin_user = ldap_return[0].split(':')[1].split(',')[0].split('=')[1]
    ldap_admin_pass = ldap_return[1].split(':')[1]

    if checkSecret(ldap_admin_pass, user_pass_info) and user_name_info == ldap_admin_user:
        result = 'ok'
        message = ''
        session['user'] = user_name_info
    else:
        result = 'err'
        message = ''
    
    return {'result': result, 'message': message}

# - Logout user
@view_config(
    route_name = 'logout',
    renderer = 'json',
)

def logout(request):

    logged(request, request.session)
    
    logged_out(request)