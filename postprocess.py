# TODO: use correct env

import sys
import datetime

file_name = sys.argv[1]
user_name = sys.argv[2]
time = datetime.datetime.now()

pages = 1 # TODO: use library for this

# TODO: use actual package name
from webapp.models import configure_database, DBSession, Job
import transaction

# TODO: database info
configure_database("postgres:///wweber")

job = Job()
job.user_name = user_name
job.file_name = file_name
job.pages = pages
job.time = time

DBSession.add(job)

transaction.commit()


exit(0)
