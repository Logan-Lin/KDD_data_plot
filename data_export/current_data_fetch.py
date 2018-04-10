from data_export import airquality
from data_export import meo
from utility import data_regularization as dr
from utility import location
from utility import date_tools


def fetch_train_set(station_id, time):
    nearest_grids = location.get_nearest_grid(station_id, 1)
    grid_name = nearest_grids[0][0]

    nearest_stations = location.get_all_station(station_id)
    meo_result = meo.get_meo_flat_data(grid_name, time)
    aq_result = airquality.get_flat_aq_data(station_id, time)

    aq_data_row = []
    aq_rows = [2, 3, 4, 5, 6, 7]
    min_max_aq = [[2, 1574], [5, 3280], [1, 300], [0.1, 15], [1, 504], [1, 307]]
    aq_index = 0
    for aq_row_index in aq_rows:
        aq_data_row.append(dr.normalization(aq_result[aq_row_index], min_max_aq[aq_index][0], min_max_aq[aq_index][1]))
        aq_index = aq_index + 1

    meo_data_row = []
    meo_rows = [2, 3, 4, 5, 6]
    min_max_meo = [[-25.5, 36.87], [826.39, 1040.62], [0, 100], [0, 360], [0, 68.82]]
    meo_index = 0
    for meo_row_index in meo_rows:
        meo_data_row.append(dr.normalization(meo_result[meo_row_index],
                                             min_max_meo[meo_index][0], min_max_meo[meo_index][1]))
        meo_index = meo_index + 1

    nearest_aq_row = []
    for nearest_station in nearest_stations:
        nearest_aq_result = airquality.get_flat_aq_data(nearest_station[0], time)
        aq_index = 0
        nearest_aq_row.append(location.cal_affect_factor(nearest_station[0], station_id, time))
        for aq_row_index in aq_rows:
            nearest_aq_row.append(dr.normalization(nearest_aq_result[aq_row_index],
                                                   min_max_aq[aq_index][0], min_max_aq[aq_index][1]))
            aq_index = aq_index + 1

    weekday, workday, holiday = date_tools.get_weekday_onehot(time)
    sum_row = [station_id, time, weekday, workday, holiday] + aq_data_row + meo_data_row + nearest_aq_row
    return sum_row
