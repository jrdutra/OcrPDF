import mysql.connector

class MysqlConnector:

    def __init__(self, _host, _user, _pass, _dataBase):
        try:
            self.mydb = mysql.connector.connect(
                    host = _host,
                    user = _user,
                    password = _pass,
                    database = _dataBase
            )
        except mysql.connector.Error as err:
            print("MYSQL conection error: : {}".format(err))
        finally:
            print("Can't conect to mysql database...")
    
    def record(self, _path, _text):
        mycursor = self.mydb.cursor()

        sql = "INSERT INTO record (path, text) VALUES (%s, %s)"
        val = (_path, _text)
        try:
            mycursor.execute(sql, val)
            self.mydb.commit()
            mycursor.close()
        except mysql.connector.Error as err:
            print("  MYSQL insert error: : {}".format(err))
        