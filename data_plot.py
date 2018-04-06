import numpy as np
import matplotlib.pyplot as plt
import pymysql as pm
import sys

database = pm.connect("localhost", "root", "094213", "KDD")
cursor = database.cursor()

rows = ["PM2.5", "PM10", "NO2", "CO", "O3", "SO2"]


def get_aq_data(station_id, start_time, end_time, row_index):
    data_array = []
    time_array = []
    temp_value = -1
    cursor.execute("select " + "utctime," + "`" + rows[row_index] + "`" + " from KDD.bj_17_18_aq" +
                   " where utctime >= '" + start_time + "' and utctime <= '" + end_time + "'" +
                   " and stationid like '" + station_id + "'")
    result = cursor.fetchall()
    for row in result:
        time_array.append(row[0])
        value = float(row[1])
        if float(row[1]) < -10:
            value = temp_value
        else:
            temp_value = float(row[1])
        data_array.append(float(value))
    return np.array([time_array, data_array])


def get_all_aq_data(station_id, start_time, end_time):
    data_matrix = [[], [], [], [], []]
    time_array = []
    data_rows = [2, 3, 4, 5, 6]
    temp_value = -1
    cursor.execute("SELECT * FROM KDD.bj_17_18_aq" +
                   " WHERE utctime >= '" + start_time + "' AND utctime <= '" + end_time + "'" +
                   " AND stationid LIKE '" + station_id + "'")
    result = cursor.fetchall()
    for row in result:
        time_array.append(row[1])
        for row_index in data_rows:
            if float(row[row_index]) < -900:
                value = temp_value
            else:
                temp_value = float(row[row_index])
            data_matrix[row_index].append(float(row[row_index]))
    return np.array([time_array, data_matrix])


def get_station_location(station_id):
    cursor.execute("SELECT longitude, latitude FROM KDD.bj_station_location WHERE id LIKE '" +
                   station_id + "'")
    result = cursor.fetchone()
    return np.array(result)


def get_nearest_grid(station_id, count):
    cursor.execute("SELECT longitude, latitude FROM KDD.bj_station_location WHERE id LIKE '" +
                   station_id + "'")
    result = cursor.fetchone()
    coordinate = result
    cursor.execute("SELECT * FROM KDD.bj_grid_location " +
                   "ORDER BY (abs(" + str(coordinate[0]) + " - longitude) + " +
                   "abs(" + str(coordinate[1]) + " - latitude))")
    result = cursor.fetchall()
    return result[0:count]


def plot_grid_meo(grid_name, longitude, latitude, start_time, end_time):
    data_matrix = []
    data_rows = [1, 2, 3, 4, 5, 6]
    data_name_array = ["temperature", "pressure", "humidity", "wind_direction", "wind_speed"]
    cursor.execute("select * from KDD.bj_historical_meo_grid " +
                   "where stationName like '" + grid_name + "' " +
                   "and utctime >= '" + start_time + "'and utctime <= '" + end_time + "'")
    result = cursor.fetchall()
    for row_index in data_rows:
        array = []
        for row in result:
            array.append(row[row_index])
        data_matrix.append(array)

    plt.figure()
    size = np.shape(data_matrix)[1]
    x = range(size)

    data_count = len(data_name_array)
    for i in range(len(data_name_array)):
        index = i + 1
        plt.subplot(data_count, 1, index)
        if index == 1:
            plt.title(grid_name + ", (" + str(longitude) + ", " + str(latitude) + ")")
        plt.plot(x, data_matrix[index])
        plt.grid()
        plt.ylabel(data_name_array[i])
    plt.xlabel("time")


start_time = "2017-10-01 14:00:00"
end_time = "2017-10-10 14:00:00"
station_id = "aotizhongxin_aq"
grid_count = 2

if len(sys.argv) > 1:
    try:
        start_time = sys.argv[1]
        end_time = sys.argv[2]
        station_id = sys.argv[3]
        grid_count = int(sys.argv[4])
    except:
        print("Command line argument no correct!")
        exit(1)

station_coordinate = get_station_location(station_id)
nearest = get_nearest_grid(station_id, grid_count)
grid_longitudes = []
grid_latitudes = []
labels = []
for one_near in nearest:
    plot_grid_meo(one_near[0], one_near[1], one_near[2], start_time, end_time)
    grid_longitudes.append(one_near[1])
    grid_latitudes.append(one_near[2])
    labels.append(one_near[0])

plt.figure()
plt.plot(station_coordinate[0], station_coordinate[1], 'o')
plt.plot(grid_longitudes, grid_latitudes, 'o')
for label, x, y in zip(labels, grid_longitudes, grid_latitudes):
    plt.annotate(
        label,
        xy=(x, y), xytext=(-10, 10),
        textcoords='offset points', ha='right', va='bottom',
        bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.3),
        arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
plt.xlabel("longitude")
plt.ylabel("latitude")

PM2_array = get_aq_data(station_id, start_time, end_time, 0)
PM10_array = get_aq_data(station_id, start_time, end_time, 1)
NO2_array = get_aq_data(station_id, start_time, end_time, 2)
CO_array = get_aq_data(station_id, start_time, end_time, 3)
O3_array = get_aq_data(station_id, start_time, end_time, 4)
SO2_array = get_aq_data(station_id, start_time, end_time, 5)
size = np.shape(PM2_array)[1]
# print("Datetime", "PM2.5", "PM10")
# for i in range(size):
#     print(PM2_array[0][i], PM2_array[1][i], PM10_array[1][i], sep=', ')

plt.figure()
x = range(size)
plt.subplot(4, 1, 1)
plt.plot(x, PM2_array[1], label='PM2.5')
plt.plot(x, PM10_array[1], label='PM10')
plt.grid()
plt.ylabel("PM2.5 & PM10")
plt.title(station_id + ", (" + str(station_coordinate[0]) + ", " + str(station_coordinate[1]) + ")")
plt.legend(loc='upper right')

plt.subplot(4, 1, 2)
plt.plot(x, NO2_array[1])
plt.grid()
plt.ylabel("NO2")

plt.subplot(4, 1, 3)
plt.plot(x, CO_array[1])
plt.grid()
plt.ylabel("CO")

plt.subplot(4, 1, 4)
plt.plot(x, O3_array[1], label='O3')
plt.plot(x, SO2_array[1], label='SO2')
plt.grid()
plt.ylabel("O3 & SO2")
plt.legend(loc='upper right', shadow=True)

plt.xlabel("time")

plt.show()
