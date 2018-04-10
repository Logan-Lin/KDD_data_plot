from database_process import mysql_connect
from os import listdir
from os.path import isfile, join


def read_sql_file(file_name):
    with open(file_name) as file:
        sql_string = file.read()
        sql_list = sql_string.split(";")
        mysql_connect.batch_commit(sql_list)


def write_all_grid(file_list):
    read_sql_file(file_list)


file_dir = '../database_process'
onlyfiles = [f for f in listdir(file_dir) if isfile(join(file_dir, f))]
print(onlyfiles)
write_all_grid(onlyfiles)
