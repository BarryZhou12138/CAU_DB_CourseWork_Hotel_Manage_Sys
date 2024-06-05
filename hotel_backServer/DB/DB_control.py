import pymysql

class DB_connect:

    def __init__(self, username, password, port):
        self.connect = pymysql.connect(
            host = 'localhost',
            port = port,
            user = username,
            password = password,
            charset = 'utf8mb4',
            autocommit=True
        )
        self.connect.select_db("hotel_DB")
        self.cursor = self.connect.cursor()
    
    def insert(self, tableName, data):
        sql = 'insert into %s values %s'%(tableName, data)
        print(sql)
        self.cursor.execute(sql)
        self.connect.commit()

    def search(self, tableName, whereSQL):
        sql = 'select * from  %s where %s;'%(tableName, whereSQL)
        print(sql)
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result

    def delete(self, tableName,whereSQL):
        sql = 'delete from  %s where %s;'%(tableName, whereSQL)
        print(sql)
        self.cursor.execute(sql)
        self.connect.commit()

    def update(self, tableName, setSQL, whereSQL, ):
        sql = 'update %s set %s where %s;'%(tableName, setSQL, whereSQL)
        print(sql)
        self.cursor.execute(sql)
        self.connect.commit()

    def direct_execute(self, SQL_String):
        print(SQL_String)
        self.cursor.execute(SQL_String)
        return  self.cursor.fetchall()
    
    def commit(self):
        self.connect.commit()
    


