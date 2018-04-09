from utility import mysql_connect
import requests


def insert_current_grid_data(start_time, end_time):
    mysql_connect.commit_sql("delete from KDD.bj_current_meo_grid " +
                             "where utctime >= '" + start_time + "' and utctime <= '" + end_time + "'")
    print("Fetching grid meteorology data...")
    url = "https://biendata.com/competition/meteorology/bj_grid/" + \
          date_string_convert(start_time) + "/" + date_string_convert(end_time) + "/2k0d1d8"
    responses = requests.get(url)
    rows = responses.text.split('\n')
    print("Inserting into database...")
    aggregate = len(rows)
    header_rows = [1, 2, 3]
    data_rows = [4, 5, 6, 7, 8]
    row_names = ["id", "stationName", "utctime", "weather", "temperature", "pressure",
                 "humidity", "wind_direction", "wind_speed"]

    sql_array = []
    for i in range(1, aggregate - 1):
        row = rows[i].rstrip()
        data_array = row.split(",")
        valid_row_names = []
        header = []
        for header_row in header_rows:
            if len(data_array[header_row]) > 0:
                header.append(data_array[header_row])
                valid_row_names.append(row_names[header_row])
        valid_data = []
        for data_row in data_rows:
            if len(data_array[data_row]) > 0:
                valid_data.append(data_array[data_row])
                valid_row_names.append(row_names[data_row])
        header_string = "','".join(header)
        data_string = ",".join(valid_data)
        temp = ","
        if len(valid_data) == 0:
            temp = ""
        sql = "insert into KDD.bj_current_meo_grid (" + ",".join(valid_row_names) + ") VALUE " + \
              "('" + header_string + "'" + temp + data_string + ")"
        sql_array.append(sql)
    error_row = mysql_connect.batch_commit(sql_array)
    if len(error_row) > 0:
        print("Error at row", ",".join(error_row))



def insert_current_aq_data(start_time, end_time):
    mysql_connect.commit_sql("DELETE FROM KDD.bj_current_aq " +
                             "WHERE utctime >= '" + start_time + "' AND utctime <= '" + end_time + "'")
    print("Fetching air quality data...")
    url = "https://biendata.com/competition/airquality/bj/" + \
          date_string_convert(start_time) + "/" + date_string_convert(end_time) + "/2k0d1d8"
    responses = requests.get(url)
    rows = responses.text.split("\n")
    print("Inserting into database...")
    aggregate = len(rows)
    header_rows = [1, 2]
    data_rows = [3, 4, 5, 6, 7, 8]
    row_names = ["id", "stationid", "utctime", "`PM2.5`", "PM10", "NO2", "CO", "O3", "SO2"]

    sql_array = []
    for i in range(1, aggregate - 1):
        row = rows[i].rstrip()
        data_array = row.split(",")
        valid_row_names = []
        header = []
        for header_row in header_rows:
            header.append(data_array[header_row])
            valid_row_names.append(row_names[header_row])
        valid_data = []
        for data_row in data_rows:
            if len(data_array[data_row]) > 0:
                valid_data.append(data_array[data_row])
                valid_row_names.append(row_names[data_row])
        header_string = "','".join(header)
        data_string = ",".join(valid_data)
        temp = ","
        if len(valid_data) == 0:
            temp = ""
        sql = "insert into KDD.bj_current_aq (" + ",".join(valid_row_names) + ") VALUE " + \
              "('" + header_string + "'" + temp + data_string + ")"
        sql_array.append(sql)
    error_row = mysql_connect.batch_commit(sql_array)
    if len(error_row) > 0:
        print("Error at row", ",".join(error_row))


def date_string_convert(date_string):
    date_and_time = date_string.split(" ")
    hms = date_and_time[1].split(":")
    array = [date_and_time[0], str(int(hms[0]))]
    return "-".join(array)


start_date = "2018-04-02 00:00:00"
end_date = "2018-04-02 23:00:00"

insert_current_grid_data(start_date, end_date)
insert_current_aq_data(start_date, end_date)
