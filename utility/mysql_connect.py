import pymysql


def get_result(sql):
    database = pymysql.connect("localhost", "root", "094213", "KDD")
    cursor = database.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    database.close()
    return result


def commit_sql(sql):
    database = pymysql.connect("localhost", "root", "094213", "KDD")
    cursor = database.cursor()
    cursor.execute(sql)
    database.commit()
    cursor.close()
    database.close()


def batch_commit(sql_array):
    database = pymysql.connect("localhost", "root", "094213", "KDD")
    cursor = database.cursor()
    error = []
    for i in range(len(sql_array)):
        try:
            cursor.execute(sql_array[i])
            database.commit()
        except:
            error.append(str(i + 1))
    cursor.close()
    database.close()
    return error
