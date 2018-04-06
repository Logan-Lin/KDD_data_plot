import sys

import matplotlib.pyplot as plt
import numpy as np
import pymysql as pm
import data_fetch

start_time = "2017-04-01 00:00:00"
end_time = "2017-05-01 23:00:00"
station_id = "beibuxinqu_aq"
grid_count = 1

database = pm.connect("localhost", "root", "094213", "KDD")
cursor = database.cursor()


def get_aq_data(station_id, start_time, end_time):
    print("Fetching", station_id, "air quality data from MySQL...")
    data_matrix = []
    data_rows = [1, 2, 3, 4, 5, 6, 7]
    temp_value = -1
    cursor.execute("SELECT * FROM KDD.bj_17_18_aq" +
                   " WHERE utctime >= '" + start_time + "' AND utctime <= '" + end_time + "'" +
                   " AND stationid LIKE '" + station_id + "'")
    result = cursor.fetchall()
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
    print("Fetching", grid_name, "grid meteorology data from MySQL...")
    data_matrix = []
    data_rows = [1, 2, 3, 4, 5, 6]
    data_name_array = ["temperature", "pressure", "humidity", "wind_direction", "wind_speed"]
    cursor.execute("SELECT * FROM KDD.bj_historical_meo_grid " +
                   "WHERE stationName LIKE '" + grid_name + "' " +
                   "AND utctime >= '" + start_time + "'AND utctime <= '" + end_time + "'")
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
        plt.plot(x, data_matrix[index], label=data_name_array[i])
        plt.grid()
        plt.legend(loc='upper right', shadow=False)
    plt.xlabel("time")


def plot_aq_data(station_id, longitude, latitude, start_time, end_time):
    aq_matrix = get_aq_data(station_id, start_time, end_time)
    size = np.shape(aq_matrix)[1]

    plt.figure()
    x = range(size)

    aq_name = ["PM2.5", "PM10", "NO2", "CO", "SO2", "O3"]
    aq_count = len(aq_name)
    for i in range(aq_count):
        plt.subplot(aq_count, 1, i + 1)
        if i == 0:
            plt.title(station_id + ", (" + str(longitude) + ", " + str(latitude) + ")")
        plt.plot(x, aq_matrix[i + 1], label=aq_name[i])
        plt.grid()
        plt.legend(loc='upper right', shadow=False)

    plt.xlabel("time")


# If command line arguments were inputted, use information from these instead
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
plot_aq_data(station_id, station_coordinate[0], station_coordinate[1], start_time, end_time)
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

print("Plotting data...")
plt.show()
