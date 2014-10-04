from pyramid.view import view_config

from .models import DBSession, Job
from pyramid.httpexceptions import HTTPSeeOther


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'webapp'}

@view_config(route_name="listjobs", renderer="listjobs.html")
def listjobs(req):
    q = DBSession.query(Job)

    return {"jobs": q.all()}

@view_config(route_name="deletejob")
def deletejob(req):
    q = DBSession.query(Job)
    q = q.filter(Job.id == req.matchdict["id"])
    job = q.first()

    try:
        job.delete()
        DBSession.delete(job)
    except OSError:
        pass

    return HTTPSeeOther("/listjobs")
