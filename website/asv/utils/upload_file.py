from os.path import abspath
from datetime import date, timedelta
import datetime as dt

def handle_uploaded_file(f):
    name = format(dt.date.today().replace(day=1) - dt.timedelta(days=1), '%B_%Y.csv')
    path = abspath('../website/uploads/' + name)
    with open(path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)