import os
import traceback
import pymysql

from dotenv import load_dotenv
from common.CommonFunc import getProjectRoot


class SQLConnector:
    def __init__(self):
        rootpath = getProjectRoot()
        load_dotenv(dotenv_path=rootpath/'.env')
        # DB config
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASSWORD')
        self.host = os.getenv('DB_HOST')
        self.port = int(os.getenv('DB_PORT'))
        self.database = os.getenv('DB_NAME')
        # AWS config
        self.AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
        self.AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.AWS_REGION = os.getenv("AWS_REGION")
        self.AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
        # connect
        self.connectsql()

    """Kết nối và truy vấn sql"""
    def connectsql(self):
        try:
            self.conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
            )
            return self.conn
        except :
            traceback.print_exc()
            return None

    def fetchAll(self, sql, var):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, var)
            result = cursor.fetchall()
            cursor.close()
            return result
        except:
            traceback.print_exc()
        return None
    def fetchOne(self, sql, var):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, var)
            result = cursor.fetchone()
            cursor.close()
            return result
        except:
            traceback.print_exc()
        return None
    def insertRow(self, sql, var):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, var)
            self.conn.commit()
            lastid = cursor.lastrowid
            cursor.close()
            return lastid

        except pymysql.MySQLError as err:
            print(f"Database error: {err}")
            return 0

    def deleteOrUpdateRow(self, sql, var):
        try:
            cursor = self.conn.cursor()
            cursor.execute(sql, var)
            self.conn.commit()
            affected_row = cursor.rowcount
            cursor.close()
            return affected_row

        except pymysql.MySQLError as err:
            print(f"Database error: {err}")
            return 0


