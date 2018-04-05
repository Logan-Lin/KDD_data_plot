import numpy as np
import matplotlib.pyplot as plt
import pymysql as pm

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


start_time = "2017-04-01 14:00:00"
end_time = "2017-05-01 14:00:00"
station_id = "aotizhongxin_aq"
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

x = range(size)
plt.subplot(4, 1, 1)
plt.plot(x, PM2_array[1], x, PM10_array[1])
plt.grid()
plt.ylabel("PM2.5 & PM10")
plt.title("AQ Display")

plt.subplot(4, 1, 2)
plt.plot(x, NO2_array[1])
plt.grid()
plt.ylabel("NO2")

plt.subplot(4, 1, 3)
plt.plot(x, CO_array[1])
plt.grid()
plt.ylabel("CO")

plt.subplot(4, 1, 4)
plt.plot(x, O3_array[1], x, SO2_array[1])
plt.grid()
plt.ylabel("O3 & SO2")

plt.xlabel("time")
plt.show()
