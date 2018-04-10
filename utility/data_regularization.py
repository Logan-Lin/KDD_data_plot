def normalization(value, min_value, max_value):
    return (value - min_value) / (max_value - min_value)


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
