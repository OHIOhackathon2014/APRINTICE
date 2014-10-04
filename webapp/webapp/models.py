# Models

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

from zope.sqlalchemy import ZopeTransactionExtension

Base = declarative_base()

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

def configure_database(uri):
    engine = create_engine(uri)
    DBSession.configure(bind=engine)


