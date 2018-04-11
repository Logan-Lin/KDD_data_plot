from database_process import mysql_connect


def get_aq_data(station_id, start_time, end_time, data_matrix=None):
    print("Fetching", station_id, "air quality data from MySQL...")
    data_matrix = []
    data_rows = [1, 2, 3, 4, 5, 6, 7]
    temp_value = -1
    result = mysql_connect.get_result("SELECT * FROM KDD.bj_17_18_aq" +
                                      " WHERE utctime >= '" + start_time + "' AND utctime <= '" + end_time + "'" +
                                      " AND stationid LIKE '" + station_id + "'")
    for row_index in data_rows:
        array = []
        for row in result:
            if row_index == 1:
                array.append(row[row_index])
            else:
                value = row[row_index]
                if value < -10:
                    value = temp_value
                else:
                    temp_value = value
                array.append(value)
        data_matrix.append(array)
    return data_matrix


def get_flat_aq_data(station_id, time):
    result = mysql_connect.get_result("SELECT * FROM KDD.bj_17_18_aq" +
                                      " WHERE utctime like '" + time + "'" +
                                      " AND stationid LIKE '" + station_id + "'")
    return result[0]
