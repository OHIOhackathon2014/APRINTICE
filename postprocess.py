# TODO: use correct env

import sys
import datetime
import subprocess
import re

file_name = sys.argv[1]
user_name = sys.argv[2]
time = datetime.datetime.now()

# get pages
pages = int(subprocess.check_output([
    "/usr/bin/pkpgcounter",
    file_name,
    ]))

# calculate ink percentages
pcts = subprocess.check_output([
    "/usr/bin/pkpgcounter",
    "-c",
    "cmyk",
    file_name,
    ])

pct_c = 0
pct_m = 0
pct_y = 0
pct_k = 0

re_iter = re.finditer("C *: *([0-9.]+)% *M *: *([0-9.]+)% *Y *: *([0-9.]+)% *K *: *([0-9.]+)%", pcts)

for match in re_iter:
    pct_c += float(match.group(1))
    pct_m += float(match.group(2))
    pct_y += float(match.group(3))
    pct_k += float(match.group(4))

pct_c /= 100.0
pct_m /= 100.0
pct_y /= 100.0
pct_k /= 100.0

# TODO: use actual package name
from webapp.models import configure_database, DBSession, Job
import transaction

# TODO: database info
configure_database("postgres:///wweber")


job = Job()
job.user_name = user_name
job.file_name = file_name
job.pages = pages
job.percent_c = pct_c
job.percent_m = pct_m
job.percent_y = pct_y
job.percent_k = pct_k
job.time = time

DBSession.add(job)

transaction.commit()


exit(0)
