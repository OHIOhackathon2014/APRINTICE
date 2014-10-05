from pyramid.view import view_config

from .models import DBSession, Job, Printer, UserData
from pyramid.httpexceptions import (HTTPSeeOther, HTTPForbidden, HTTPOk,
        HTTPNotFound)


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

@view_config(route_name="get_user_info", renderer="json")
def get_user_info(req):
    user = req.session.get("username")
    if not user:
        return HTTPForbidden()

    q = DBSession.query(UserData)
    q = q.filter(UserData.user_name == user)
    user = q.first()

    if not user:
        return HTTPNotFound()


    return {
            "username": user.user_name,
            "balance": user.balance,
            }

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

@view_config(route_name="release_job", request_method="POST")
def release_job(req):
    user = req.session.get("username")
    job_id = req.matchdict["id"]
    printer_name = req.matchdict["printer_name"]

    if not user:
        return HTTPForbidden()

    q = DBSession.query(Job)
    q = q.filter(Job.id == job_id)
    q = q.filter(Job.user_name == user)
    job = q.first()

    q = DBSession.query(Printer)
    q = q.filter(Printer.name == printer_name)
    printer = q.first()

    q = DBSession.query(UserData)
    q = q.filter(UserData.user_name == user)
    user = q.first()

    if not printer or not job:
        return HTTPNotFound()

    cost = job.get_cost(printer)

    # Check balance
    if cost > user.balance:
        return HTTPForbidden()

    # Otherwise good to go
    user.balance -= cost
    DBSession.add(user)

    job.release(printer)
    job.delete()
    DBSession.delete(job)

    return HTTPOk()

@view_config(route_name="get_pdf")
def get_pdf(req):
    user = req.session.get("username")
    id = req.matchdict["id"]

    if not user:
        return HTTPForbidden()

    q = DBSession.query(Job)
    q = q.filter(Job.id == job_id)
    q = q.filter(Job.user_name == user)
    job = q.first()

    if not job:
        return HTTPNotFound()

    return HTTPOk(job.get_data())

