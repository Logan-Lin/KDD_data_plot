import csv
import pymysql

database = pymysql.connect("localhost", "root", "094213", "KDD")
cursor = database.cursor()
# cursor.execute("DELETE FROM KDD.ld_17_18_forecast_aq")
cursor.execute("DELETE FROM KDD.ld_historical_meo_grid")
database.commit()

csv_file = open('data/London_historical_meo_grid.csv')
reader = csv.reader(csv_file, delimiter=',')
count = 0
nullable_indexes = [4, 5, 6, 7, 8]
for row in reader:
    count = count + 1
    if count == 1:
        continue
    if len(row[0]) <= 0:
        break
    try:
        value_list = []
        for index in nullable_indexes:
            if len(row[index]) <= 0:
                row[index] = str(-999)
            value_list.append(row[index])
        # row[1] = row[1].replace("/", "-")
        values = ",".join(value_list)
        cursor.execute("INSERT INTO KDD.ld_historical_meo_grid " +
                       "(stationName, utctime, temperature, pressure, humidity, wind_direction, wind_speed) VALUE " +
                       "('" + row[0] + "','" + row[3] + "'," + values + ")")
    except:
        print(count)
        break
database.commit()
print(count)
