from os import listdir
from os.path import isfile, join


def merge(file_dir, write_dir):
    onlyfiles = [f for f in listdir(file_dir) if isfile(join(file_dir, f))]
    with open(write_dir, "w") as write_file:
        for read_file in onlyfiles:
            print("Merging", read_file)
            with open(file_dir + "/" + read_file, "r") as read:
                write_file.write(read.read())
                write_file.write("\n")


merge("/Users/loganlin/Downloads/meo_grid_sql", "/Users/loganlin/Downloads/merge.sql")
