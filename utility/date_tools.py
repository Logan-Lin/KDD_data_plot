from datetime import datetime, timedelta
from utility import data_regularization as dr
import pytz

format_string = "%Y-%m-%d %H:%M:%S"
timezone = pytz.timezone("Asia/Hong_Kong")
holiday_start_ends = [["2017-01-01", "2017-01-02"],
                      ["2017-01-27", "2017-02-02"],
                      ["2017-04-02", "2017-04-04"],
                      ["2017-04-29", "2017-05-01"],
                      ["2017-05-28", "2017-05-30"],
                      ["2017-10-01", "2017-10-08"],
                      ["2018-01-01", "2018-01-01"],
                      ["2018-02-15", "2018-02-21"],
                      ["2018-04-05", "2018-04-07"],
                      ["2018-04-29", "2018-05-01"]]
holiday_array = []


def per_delta(start, end, delta):
    curr = start
    while curr <= end:
        yield curr
        curr += delta


def get_time_string(start_time_s, end_time_s, time_delta=timedelta(hours=1)):
    time_string_array = []
    start_time = datetime.strptime(start_time_s, format_string)
    end_time = datetime.strptime(end_time_s, format_string)
    for time in per_delta(start_time, end_time, time_delta):
        time_string_array.append(time.strftime(format_string))
    return time_string_array


def get_weekday_onehot(date_string):
    date_object = datetime.strptime(date_string, format_string)
    workday_bool = "0"  # weekend
    if date_object.weekday() in range(0, 5):
        workday_bool = "1"  # workday
    holiday_bool = "0"
    if date_object.date() in holiday_array:
        holiday_bool = "1"  # is holiday
    return dr.get_onehot(date_object.weekday(), 0, 6), workday_bool, holiday_bool


for i in range(len(holiday_start_ends)):
    for j in range(2):
        holiday_start_ends[i][j] += " 00:00:00"
    holiday_array += get_time_string(holiday_start_ends[i][0], holiday_start_ends[i][1], timedelta(days=1))
for i in range(len(holiday_array)):
    holiday_array[i] = datetime.strptime(holiday_array[i], format_string).date()
