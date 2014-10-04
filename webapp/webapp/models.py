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

def create_tables():
    Base.metadata.create_all(bind=DBSession.bind)

class UserData(Base):
    __tablename__ = "user_data"

    user_name = Column(String(64), primary_key=True)
    balance = Column(Float, nullable=False, default=0, server_default="0")

class Job(Base):
    __tablename__ = "jobs"

    user_name = Column(String(64), primary_key=True)
    file_name = Column(String(256))
    pages = Column(Integer, nullable=False, default=1, server_default="1")
    time = Column(DateTime)

class Printer(Base):
    __tablename__ = "printers"

    name = Column(String(64), primary_key=True)
    title = Column(String(256))
    description = Column(Text)

    cost_per_page = Column(Float, nullable=False)

