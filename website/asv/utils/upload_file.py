import csv

def parse_csv_file(file_path):
    dict_list = []
    with open(file_path, 'rt') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dict_list.append(row)
    
    return dict_list


def handle_uploaded_file(file, file_write_path):
    # Open the input CSV file for reading
    with open(file_write_path, "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    # Return file contents as list of dictionaries
    dict_list = parse_csv_file(file_write_path)

    return dict_list