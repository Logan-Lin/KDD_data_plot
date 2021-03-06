import sys

import matplotlib.pyplot as plt
import numpy as np
from database_process import mysql_connect
from utility import location
from data_export import airquality

start_time = "2017-04-18 00:00:00"
end_time = "2017-04-18 23:00:00"
aq_array = ["beibuxinqu_aq", "dongsi_aq"]
grid_count = 1


def get_station_location(station_id):
    result = mysql_connect.get_result("SELECT longitude, latitude FROM KDD.bj_station_location WHERE id LIKE '" +
                                      station_id + "'")
    return result[0]


def plot_grid_meo(grid_name, longitude, latitude, start_time, end_time):
    print("Fetching", grid_name, "grid meteorology data from MySQL...")
    data_matrix = []
    data_rows = [1, 2, 3, 4, 5, 6]
    data_name_array = ["temperature", "pressure", "humidity", "wind_direction", "wind_speed"]
    result = mysql_connect.get_result("SELECT * FROM KDD.bj_historical_meo_grid " +
                                      "WHERE stationName LIKE '" + grid_name + "' " +
                                      "AND utctime >= '" + start_time + "'AND utctime <= '" + end_time + "'")
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
    aq_matrix = airquality.get_aq_data(station_id, start_time, end_time)
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


def draw_labels(labels, x, y):
    for label, x, y in zip(labels, x, y):
        plt.annotate(
            label,
            xy=(x, y), xytext=(-10, 10),
            textcoords='offset points', ha='right', va='bottom',
            bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.3),
            arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))


def plot_aq_nearest_meo(station_id_array, start_time, end_time, grid_count):
    station_longitudes = []
    station_latitudes = []
    grid_longitudes = []
    grid_latitudes = []
    labels = []

    refined_nearest = set()
    for station_id in station_id_array:
        station_coordinate = get_station_location(station_id)
        station_longitudes.append(station_coordinate[0])
        station_latitudes.append(station_coordinate[1])
        plot_aq_data(station_id, station_coordinate[0], station_coordinate[1], start_time, end_time)
        nearest = location.get_nearest_grid(station_id, grid_count)
        for one_near in nearest:
            refined_nearest.add(one_near)
    for one_near in refined_nearest:
        plot_grid_meo(one_near[0], one_near[1], one_near[2], start_time, end_time)
        grid_longitudes.append(one_near[1])
        grid_latitudes.append(one_near[2])
        labels.append(one_near[0])
    if len(station_id_array) == 1 and grid_count == 0:
        return
    plt.figure()
    plt.plot(station_longitudes, station_latitudes, 'o')
    plt.plot(grid_longitudes, grid_latitudes, 'o')
    draw_labels(labels, grid_longitudes, grid_latitudes)
    draw_labels(station_id_array, station_longitudes, station_latitudes)
    plt.xlabel("longitude")
    plt.ylabel("latitude")


# If command line arguments were inputted, use information from these instead
if len(sys.argv) > 1:
    try:
        start_time = sys.argv[1]
        end_time = sys.argv[2]
        grid_count = int(sys.argv[3])
        aq_array = sys.argv[4:]
    except:
        print("Command line argument no correct!")
        exit(1)

plot_aq_nearest_meo(aq_array, start_time, end_time, grid_count)

print("Plotting data...")
# plt.savefig(start_time + ".png", dpi=300)
plt.show()
