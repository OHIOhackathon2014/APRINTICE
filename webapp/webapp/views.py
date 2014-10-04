from pyramid.view import view_config

from .models import DBSession, Job, Printer
from pyramid.httpexceptions import HTTPSeeOther, HTTPForbidden, HTTPOk


@view_config(route_name='home', renderer='templates/mytemplate.pt')
def my_view(request):
    return {'project': 'webapp'}

@view_config(route_name="login", renderer="login.html")
def login(req):
    if req.method == "POST":
        username = req.POST.get("username")
        password = req.POST.get("password")

        # TODO: actual auth :|
        req.session["username"] = username

        return HTTPSeeOther("/")
    else:
        return {}

@view_config(route_name="logout")
def logout(req):
    del req.session["username"]
    return HTTPSeeOther("/")

@view_config(route_name="get_jobs", renderer="json")
def get_jobs(req):
    user = req.session.get("username")
    if not user:
        return HTTPForbidden()

    results = []

    q = DBSession.query(Job)
    q = q.filter(Job.user_name == user)

    for row in q.all():
        results.append({
            "id": row.id,
            "file": row.file_name,
            "pages": row.pages,
            "percentC": row.percent_c,
            "percentM": row.percent_m,
            "percentY": row.percent_y,
            "percentK": row.percent_k,
            "date": row.time.strftime("%m-%d-%Y %I:%M:%S %p"),
            })

    return results

@view_config(route_name="get_printers", renderer="json")
def get_printers(req):
    q = DBSession.query(Printer)
    results = []

    for row in q.all():
        results.append({
            "name": row.name,
            "title": row.title,
            "description": row.description,
            "costPerPage": row.cost_per_page,
            "costC": row.cost_c,
            "costM": row.cost_m,
            "costY": row.cost_y,
            "costK": row.cost_k,
            })

    return results

@view_config(route_name="delete_job", request_method="DELETE", renderer="json")
def delete_job(req):
    user = req.session.get("username")
    job_id = req.matchdict["id"]

    if not user:
        return HTTPForbidden()

    q = DBSession.query(Job)
    q = q.filter(Job.id == job_id)
    q = q.filter(Job.user_name == user)
    q = q.delete()

    return None
