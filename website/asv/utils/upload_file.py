import csv

def parse_csv_file(file_path):
    dict_list = []
    with open(file_path, 'rt') as f:
        reader = csv.DictReader(f)
        for row in reader:
            dict_list.append(row)
    
    return dict_list


def handle_uploaded_file(file_read_path, file_write_path):
    # Open the input CSV file for reading
    with open(file_read_path, mode='r') as input_file:
        reader = csv.reader(input_file)

        # Open the output CSV file for writing
        with open(file_write_path, mode='w', newline='') as output_file:
            writer = csv.writer(output_file)

            # Loop through each row in the input CSV file
            for row in reader:
                # Write the row to the output CSV file
                writer.writerow(row)

    # Return file contents as list of dictionaries
    dict_list = parse_csv_file(file_write_path)

    return dict_list