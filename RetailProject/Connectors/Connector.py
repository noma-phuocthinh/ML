import mysql.connector
import traceback
import pandas as pd
import pymysql


class Connector:
    def __init__(self,server="localhost", port=3306, database="k23416_retail", username="root", password="@Obama123"):
        self.server=server
        self.port=port
        self.database=database
        self.username=username
        self.password=password
        self.connect()
    def connect(self):
        try:
            self.conn = pymysql.connect(
                host=self.server,
                port=self.port,
                database=self.database,
                user=self.username,
                password=self.password)
            return self.conn
        except:
            self.conn=None
            traceback.print_exc()
        return None

    def disConnect(self):
        if self.conn != None:
            self.conn.close()

    def queryDataset(self, sql):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql)
            df = pd.DataFrame(cursor.fetchall())
            if not df.empty:
                # SỬA DÒNG NÀY:
                # df.columns=cursor.column_names  # DÒNG CŨ BỊ LỖI
                df.columns = [desc[0] for desc in cursor.description]  # DÒNG MỚI ĐÃ SỬA
            return df
        except:
            traceback.print_exc()
        return None

    def getTablesName(self):
        cursor = self.conn.cursor()
        cursor.execute("Show tables;")
        results=cursor.fetchall()
        tablesName=[]
        for item in results:
            tablesName.append([tableName for tableName in item][0])
        return tablesName

    def fetchOne(self, sql, var = None):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, var)
            dataset = cursor.fetchone()
            cursor.close()
            return dataset
        except:
            traceback.print_exc()
        return None

    def fetchAll(self, sql, var = None):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, var)
            dataset = cursor.fetchall()
            cursor.close()
            return dataset
        except:
            traceback.print_exc()
        return None

    def insertOne(self, sql, var = None):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, var)
            self.conn.commit()
            affected_row = cursor.rowcount
            cursor.close()
            return affected_row
        except:
            traceback.print_exc()

    def executeUpdate(self, sql, var=None):
        """Thực thi các câu lệnh UPDATE, DELETE và trả về số hàng bị ảnh hưởng"""
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, var)
            self.conn.commit()
            affected_row = cursor.rowcount
            cursor.close()
            return affected_row
        except Exception as e:
            self.conn.rollback()
            traceback.print_exc()
            return 0

