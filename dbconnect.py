import pymysql

db = pymysql.connect("localhost", "root", "", "advprog")

def insertuser(username, password):

    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO `users` (`username`, `password`) VALUES (%s, %s)"
            cursor.execute(sql)
            result = cursor.fetchone(username, password)
            print(result)
    finally:
        db.close()
