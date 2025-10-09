from Ngay8_10.connectors.connector import Connector

class EmployeeConnector(Connector):
    def login(self, email, pwd):
        sql = "SELECT * FROM employee WHERE Email=%s AND Password=%s"
        val = (email, pwd)
        # Dùng fetchone vì login chỉ cần 1 bản ghi
        result = self.fetchone(sql, val)
        return result