import csv


def write_csv(header_array, content_matrix, file_name):
    csv_file = open(file_name, 'w')
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(header_array)
    for content_row in content_matrix:
        writer.writerow(content_row)
    csv_file.close()
