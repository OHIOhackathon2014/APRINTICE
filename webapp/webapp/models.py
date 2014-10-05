# Models

from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base

from zope.sqlalchemy import ZopeTransactionExtension

import cups
import subprocess
import os

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

    id = Column(Integer, primary_key=True)
    user_name = Column(String(64), nullable=False)
    file_name = Column(String(256))
    pages = Column(Integer, nullable=False, default=1, server_default="1")
    percent_c = Column(Float, default=0, server_default="1")
    percent_m = Column(Float, default=0, server_default="1")
    percent_y = Column(Float, default=0, server_default="1")
    percent_k = Column(Float, default=0, server_default="1")
    time = Column(DateTime)

    def release(self, printer):
        """Releases the job to the selected printer object
        """

        # Connect to local server
        subprocess.call([
            "/usr/bin/lp",
            "-d",
            printer.name,
            self.file_name,
            ])

    def get_cost(self, printer):
        """Calculate the cost to print this job
        """

        return printer.cost_per_page * self.pages + printer.cost_c * self.percent_c + printer.cost_m * self.percent_m + printer.cost_y * self.percent_y + printer.cost_k * self.percent_k

    def delete(self):
        os.unlink(self.file_name)

    def get_data(self):
        with open(self.file_name, "r") as f:
            data = f.read()

        return data

class Printer(Base):
    __tablename__ = "printers"

    name = Column(String(64), primary_key=True)
    title = Column(String(256))
    description = Column(Text)

    cost_per_page = Column(Float, nullable=False)
    cost_c = Column(Float, default=0, server_default="1")
    cost_m = Column(Float, default=0, server_default="1")
    cost_y = Column(Float, default=0, server_default="1")
    cost_k = Column(Float, default=0, server_default="1")

