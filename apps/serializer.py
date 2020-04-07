import datetime
from collections import namedtuple

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()
