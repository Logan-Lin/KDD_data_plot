from database_process import mysql_connect
from utility import location


def get_meo_flat_data(grid_id, time, data_matrix=None):
    if data_matrix is None:
        meo_result = mysql_connect.get_result("SELECT * FROM KDD.bj_meo_grid_" + location.get_grid_number(grid_id) +
                                              " WHERE stationName LIKE '" + grid_id +
                                              "' AND utctime LIKE '" + time + "'")
        return meo_result[0]


def get_grid_all_meo(grid_id):
    meo_result = mysql_connect.get_result("SELECT * FROM KDD.bj_historical_meo_grid " +
                                          "WHERE stationName LIKE '" + grid_id + "'")
    return meo_result


# def search_meo_matrix(data_matrix, grid_id, date_time):
#     return data_matrix[data_matrix[:, 0] == grid_id]
