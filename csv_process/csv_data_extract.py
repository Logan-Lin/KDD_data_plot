import csv
import pymysql

database = pymysql.connect("localhost", "root", "094213", "KDD")
cursor = database.cursor()
cursor.execute("DELETE FROM KDD.bj_17_18_aq where utctime < '2018-01-31 16:00:00'")
database.commit()

csv_file = open('data/beijing_17_18_aq.csv')
reader = csv.reader(csv_file, delimiter=',')
count = 0
unnull_indexes = [0, 1]
nullable_indexes = [2, 3, 4, 5, 6, 7]
for row in reader:
    count = count + 1
    if count == 1:
        continue
    if len(row[unnull_indexes[0]]) <= 0:
        break
    try:
        value_list = []
        indexes_list = []
        for index in nullable_indexes:
            if len(row[index]) <= 0:
                row[index] = str(-999)
            value_list.append(row[index])
        for index in unnull_indexes:
            indexes_list.append(row[index])
        # row[1] = row[1].replace("/", "-")
        values = ",".join(value_list)
        indexes = "','".join(indexes_list)
        sql = "INSERT INTO KDD.bj_17_18_aq VALUE " + \
              "('" + indexes + "'," + values + ")"
        cursor.execute(sql)
    except:
        print(count, "\n", sql, "\n")
        # break
database.commit()
print(count)
