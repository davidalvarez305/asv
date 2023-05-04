import csv

def handle_uploaded_file(f, localpath):
    with open(localpath, "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    '''TURN CSV TO LIST OF DICTIONARIES'''
    dict_list = []
    with open(localpath, 'rt') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dict_list.append(row)

    return dict_list