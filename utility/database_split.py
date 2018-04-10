from database_process import mysql_connect
from data_export import meo


string_indexes = [0, 1]
number_indexes = [2, 3, 4, 5, 6]


def create_grid_table(grid_id):
    grid_number = grid_id.split("_")[2]
    mysql_connect.commit_sql("create table bj_meo_grid_" + grid_number + " "
                             "(stationName varchar(128) not null,"
                             "utctime datetime not null,"
                             "temperature float null,"
                             "pressure float null,"
                             "humidity float null,"
                             "wind_direction float null,"
                             "wind_speed float null,"
                             "primary key (stationName, utctime))")


def delete_grid_table(grid_id):
    grid_number = grid_id.split("_")[2]
    mysql_connect.commit_sql("drop table bj_meo_grid_" + grid_number)


grid_id_result = mysql_connect.get_result("SELECT stationName from KDD.bj_grid_location")
for temp_grid_id in grid_id_result:
    grid_id = temp_grid_id[0]
    grid_number = grid_id.split("_")[2]
    if int(grid_number) < 250:
        continue
    print("Spliting into", grid_id)
    try:
        delete_grid_table(grid_id)
    except:
        print(end='')
    try:
        create_grid_table(grid_id)
    except:
        print(end='')
    meo_result = meo.get_grid_all_meo(grid_id)
    sql_array = []
    for row in meo_result:
        real_row = []
        for data in row:
            real_row.append(str(data))
        sql = "insert into bj_meo_grid_" + grid_number + \
              " value ('" + "','".join(real_row[0:2]) + "'," + ",".join(real_row[2:7]) + ")"
        sql_array.append(sql)
    mysql_connect.batch_commit(sql_array)
