from database_process import mysql_connect
from os import listdir
from os.path import isfile, join


def read_sql_file(file_name):
    with open(file_name) as file:
        sql_string = file.read()
        sql_list = sql_string.split(";")
        mysql_connect.batch_commit(sql_list)


def write_all_grid(file_list):
    for file in file_list:
        print("Processing file", file)
        read_sql_file(file)


# file_dir = '../database_process'
result = mysql_connect.get_result("select * from KDD.bj_grid_location")
for row in result:
    grid_name = row[0]
    try:
        mysql_connect.commit_sql("CREATE TABLE " + grid_name + " (stationName VARCHAR(128)"
                                 " NOT NULL,utctime DATETIME NOT NULL,"
                                 "temperature FLOAT NULL,"
                                 "pressure FLOAT NULL,"
                                 "humidity FLOAT NULL,"
                                 "wind_direction FLOAT NULL,"
                                 "wind_speed FLOAT NULL,"
                                 "PRIMARY KEY (stationName, utctime))")
    except:
        print("", end='')
# onlyfiles = [f for f in listdir(file_dir) if isfile(join(file_dir, f))]
# write_all_grid(onlyfiles)
read_sql_file("merge.sql")
