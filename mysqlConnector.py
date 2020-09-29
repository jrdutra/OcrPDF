import mysql.connector

class MysqlConnector:

    def __init__(self, _host, _user, _pass, _dataBase):
        self.mydb = mysql.connector.connect(
                host = _host,
                user = _user,
                password = _pass,
                database = _dataBase
        )
    
    def record(self, _path, _text):
        mycursor = self.mydb.cursor()

        sql = "INSERT INTO record (path, text) VALUES (%s, %s)"
        val = (_path, _text)
        
        mycursor.execute(sql, val)
        self.mydb.commit()