from datetime import datetime, timedelta


def normalization(value, min_value, max_value):
    return (value - min_value) / (max_value - min_value)


def per_delta(start, end, delta):
    curr = start
    while curr <= end:
        yield curr
        curr += delta


def get_time_string(start_time_s, end_time_s):
    time_string_array = []
    format_string = "%Y-%m-%d %H:%M:%S"
    start_time = datetime.strptime(start_time_s, format_string)
    end_time = datetime.strptime(end_time_s, format_string)
    for time in per_delta(start_time, end_time, timedelta(hours=1)):
        time_string_array.append(time.strftime(format_string))
    return time_string_array
