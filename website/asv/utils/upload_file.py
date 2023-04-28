from os.path import abspath
from datetime import date, timedelta
import datetime as dt
import csv

def handle_uploaded_file(f):
    name = format(dt.date.today().replace(day=1) - dt.timedelta(days=1), '%B_%Y.csv')
    path = abspath('../website/uploads/' + name)
    with open(path, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    '''TURN CSV TO LIST OF DICTIONARIES'''
    dict_list = []
    with open(path, 'rt') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dict_list.append(row)

    return dict_list