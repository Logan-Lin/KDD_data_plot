import pymysql
import requests


def insert_current_grid_data(start_time, end_time):
    cursor.execute("delete from " + database_name +".bj_current_meo_grid " +
                   "where utctime >= '" + start_time + "' and utctime <= '" + end_date + "'")
    print("Fetching grid meteorology data...")
    url = "https://biendata.com/competition/meteorology/bj_grid/" + \
          date_string_convert(start_date) + "/" + date_string_convert(end_date) + "/2k0d1d8"
    responses = requests.get(url)
    rows = responses.text.split('\n')
    print("Inserting into database...")
    aggregate = len(rows)
    duplicate = []
    for i in range(1, aggregate - 1):
        row = rows[i].rstrip()
        data_array = row.split(",")
        header = "','".join([data_array[1], data_array[2], data_array[3]])
        data = ",".join([data_array[4], data_array[5], data_array[6], data_array[7], data_array[8]])
        try:
            cursor.execute("insert into " + database_name + ".bj_current_meo_grid " +
                           "(stationName, utctime, weather, temperature, " +
                           "pressure, humidity, wind_direction, wind_speed) VALUE " +
                           "('" + header + "'," + data + ")")
        except:
            duplicate.append(str(i))
    print("Duplicate key at ", ", ".join(duplicate), "(Can be ignored)", sep='')
    db.commit()


def insert_current_aq_data(start_time, end_time):
    cursor.execute("delete from " + database_name + ".bj_current_aq " +
                   "where utctime >= '" + start_time + "' and utctime <= '" + end_time + "'")
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
        try:
            sql = "insert into " + database_name + ".bj_current_aq (" + ",".join(valid_row_names) + ") VALUE " + \
                        "('" + header_string + "'" + temp + data_string + ")"
            cursor.execute(sql)
        except:
            print("Error at ", i, sep='')
    db.commit()


def date_string_convert(date_string):
    date_and_time = date_string.split(" ")
    hms = date_and_time[1].split(":")
    array = [date_and_time[0], str(int(hms[0]))]
    return "-".join(array)


start_date = "2018-04-01 00:00:00"
end_date = "2018-04-05 23:00:00"
database_name = "KDD"

db = pymysql.connect("localhost", "root", "094213", database_name)
cursor = db.cursor()

insert_current_grid_data(start_date, end_date)
insert_current_aq_data(start_date, end_date)