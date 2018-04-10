from utility import mysql_connect
import math
from data_export import meo


def get_nearest_grid(station_id, count):
    coordinate = get_station_location(station_id)
    result = mysql_connect.get_result("SELECT * FROM KDD.bj_grid_location " +
                                      "ORDER BY (abs(" + str(coordinate[0]) + " - longitude) + " +
                                      "abs(" + str(coordinate[1]) + " - latitude))")
    return result[0:count]


def get_nearest_station(station_id, count):
    coordinate = get_station_location(station_id)
    nearest_result = mysql_connect.get_result("SELECT * FROM KDD.bj_station_location " +
                                              "ORDER BY (abs(" + str(coordinate[0]) + " - longitude) + " +
                                              "abs(" + str(coordinate[1]) + " - latitude))")
    return nearest_result[1:count + 1]


def get_station_location(station_id):
    result = mysql_connect.get_result(
        "SELECT longitude, latitude FROM KDD.bj_station_location WHERE id LIKE '" +
        station_id + "'")
    coordinate = result[0]
    return coordinate


def cal_distance(coordinate1, coordinate2):
    return math.sqrt(math.pow((coordinate1[0] - coordinate2[0]), 2) +
                     math.pow((coordinate1[1] - coordinate2[1]), 2))


def get_grid_number(grid_id):
    return grid_id.split("_")[2]


def cal_angle(main, verse):
    temp_angle = math.acos((verse[1] - main[1]) / cal_distance(main, verse))
    if main[0] - verse[0] < 0:
        temp_angle = 2 * math.pi - temp_angle
    return temp_angle


def get_all_station(except_id):
    result = mysql_connect.get_result("SELECT * FROM KDD.bj_station_location " +
                                      "WHERE id NOT LIKE '" + except_id + "'")
    return result


def cal_affect_factor(main_id, verse_id, time):
    main_coordinate = get_station_location(main_id)
    verse_coordinate = get_station_location(verse_id)
    distance = cal_distance(main_coordinate, verse_coordinate)
    try:
        meo_data = meo.get_meo_flat_data(get_nearest_grid(main_id, 1)[0][0], time)
        wind_direction = meo_data[5] / 360 * 2 * math.pi
        wind_speed = meo_data[6]
        angle = abs(cal_angle(main_coordinate, verse_coordinate) - wind_direction)
        result = math.cos(angle * wind_speed) / distance
    except:
        result = 0
    return result
