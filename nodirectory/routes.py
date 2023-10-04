def includeme(config):
    
    # static content
    config.add_static_view('static', 'static', cache_max_age=0)

    # login
    config.add_route('login', '/')
    config.add_route('logsession', '/logsession')
    config.add_route('logout', '/logout')

    # front
    config.add_route('loggeduser', '/loggeduser')
    
    # services/home routes
    config.add_route('service', '/service')
    config.add_route('servicelist', '/servicelist')

    # users routes
    config.add_route('user', '/user')
    config.add_route('userlist', '/userlist')
    config.add_route('userinfo', '/userinfo')
    config.add_route('userdel', '/userdel')
    config.add_route('useradd', '/useradd')
    config.add_route('userpass', '/userpass')

    # groups routes
    config.add_route('group', '/group')
    config.add_route('grouplist', '/grouplist')
    config.add_route('groupinfo', '/groupinfo')
    config.add_route('groupdel', '/groupdel')
    config.add_route('groupadd', '/groupadd')

    # machines routes
    config.add_route('machine', '/machine')
    config.add_route('machinelist', '/machinelist')
    config.add_route('machinedel', '/machinedel')
    config.add_route('machineadd', '/machineadd')
