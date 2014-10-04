from pyramid.view import view_config


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'webapp'}

@view_config(route_name="listjobs", renderer="listjobs.html")
def listjobs(req):
    return {}
