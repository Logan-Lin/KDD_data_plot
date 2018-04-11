import csv


def get_all(file_name):
    with open(file_name) as csv_file:
        reader = csv.reader(csv_file)
        data_matrix = []
        for row in reader:
            data_matrix.append(row)
    return data_matrix
