from csv_process import csv_read, csv_write
from database_process import mysql_connect


def split_csv():
    data_matrix = csv_read.get_all("../data/Beijing_historical_meo_grid.csv")
    count = 0
    all_grid = mysql_connect.get_result("SELECT stationName FROM KDD.bj_grid_location")
    for grid_id_ in all_grid:
        grid_id = grid_id_[0]
        grid_matrix = data_matrix[count + 1::651]
        csv_write.write_csv(None, grid_matrix, "../data/meo_data/" + grid_id + ".csv")
        count += 1
