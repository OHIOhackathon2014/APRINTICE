from pyramid.config import Configurator

from .models import configure_database, create_tables

from pyramid.session import SignedCookieSessionFactory


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    config = Configurator(settings=settings)
    config.include("pyramid_tm")
    config.include("pyramid_jinja2")
    config.include('pyramid_chameleon')

    # Configure database
    configure_database(settings["database"])
    create_tables()

    # Templates
    config.add_jinja2_renderer(".html")
    config.add_jinja2_search_path("webapp:templates/", name=".html")

    config.set_session_factory(SignedCookieSessionFactory("TODO~CHANGEME"))

    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')

    config.add_route("login", "/login")
    config.add_route("logout", "/logout")

    config.add_route("get_jobs", "/jobs")
    config.add_route("get_printers", "/printers")
    config.add_route("delete_job", "/jobs/{id}/delete")
    config.add_route("release_job", "/jobs/{id}/release/{printer_name}")

    config.scan()

    return config.make_wsgi_app()
