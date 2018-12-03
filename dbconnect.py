import pymysql

db = pymysql.connect("localhost", "root", "", "advprog")



try:
    with db.cursor() as cursor:
        sql = "INSERT INTO `users` (`username`, `password`) VALUES (%s, %s)"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)
finally:
    db.close()
