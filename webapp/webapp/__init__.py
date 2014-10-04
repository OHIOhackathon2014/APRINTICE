from pyramid.config import Configurator

from .models import configure_database, create_tables


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """

    config = Configurator(settings=settings)

    configure_database(settings["database"])
    create_tables()

    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.scan()



    return config.make_wsgi_app()
