import pymysql

db = pymysql.connect("http://192.168.47.1:3306/", "root", "%r(kHRxcp>Zw5we2b_nD", "advprog")

def insertuser(username, password):

    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO `users` (`username`, `password`) VALUES (%s, %s)"
            cursor.execute(sql)
            result = cursor.fetchone(username, password)
            print(result)
    finally:
        db.close()
