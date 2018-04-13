import csv


def write_csv(row, file_name):
    csv_file = open(file_name, 'a')
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(row)
    csv_file.close()
