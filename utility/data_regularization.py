def normalization(value, min_value=None, max_value=None, start=0, end=1):
    if value is None or value < -100:
        return None
    if min_value is None or max_value is None:
        return value
    return ((value - min_value) / (max_value - min_value)) * (end - start) + start


def get_temp_scope(raw_string):
    temp_string = raw_string.split("  ")[1][:-1]
    return temp_string.split("~")


def get_onehot(value, start, end):
    one_hot_array = []
    for n in range(start, end + 1):
        if n is value:
            one_hot_array.append("1")
        else:
            one_hot_array.append("0")
    return "".join(one_hot_array)
