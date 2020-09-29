import mysql.connector

class MysqlConnector:

    def __init__(self, _host, _user, _pass, _dataBase):
        self.mydb = mysql.connector.connect(
                host = _host,
                user = _user,
                password = _pass,
                database = _dataBase
        )