from csv_process import csv_write
from data_export import current_data_fetch
from utility import date_tools
import time as t
import sys
from utility import location
import threading


class MyThread(threading.Thread):
    def __init__(self, station_id):
        threading.Thread.__init__(self)
        self.station_id = station_id
    def run(self):
        tic = t.time()
        fetch_period_train_sets(self.station_id, start, end)
        toc = t.time()
        print(toc - tic)


aq_row = ["PM2.5", "PM10", "NO2", "CO", "O3", "SO2"]
head_row = ["aq_station", "time", "weekday", "workday", "holiday"] + aq_row + \
           ["temperature", "pressure", "humidity", "wind_direction", "wind_speed"]
for i in range(34):
    head_row.append("near_aq_factor_" + str(i))
    head_row = head_row + aq_row


def fetch_period_train_sets(station_id, start_time, end_time):
    csv_write.write_csv(head_row, "../output/" + station_id + ".csv")
    for time_string in date_tools.get_time_string(start_time, end_time):
        try:
            data_row = current_data_fetch.fetch_train_set(station_id, time_string)
            csv_write.write_csv(data_row, "../output/" + station_id + ".csv")
            print("Finished fetching", station_id, time_string, "data")
        except:
            print("Data loss at", time_string)


start, end = "2017-03-01 00:00:00", "2017-03-01 23:00:00"
start_index = int(input("Input start index: "))
end_index = int(input("Input end index: "))
# start_index, end_index = 17, 24
for station in location.get_all_station("")[start_index:end_index+1]:
    station_id = station[0]
    thread = MyThread(station_id)
    thread.run()
