import pymysql

db = pymysql.connect("localhost", "root", "", "advprog")

def insertuser(username, password):

        with db.cursor() as cursor:
            sql = "INSERT INTO `users` (`username`, `password`) VALUES ('"+ username +  "', '" + password + "')"
            cursor.execute(sql)
