from Ngay8_10.connectors.connector import Connector
from Ngay8_10.models.employee import Employee


class EmployeeConnector(Connector):
    def login(self,email,pwd):
        sql = "SELECT * FROM employee " \
              "where Email=%s and Password=%s"
        val = (email, pwd)
        dataset=self.fetchone(sql, val)
        if dataset==None:
            return None
        emp=Employee(dataset[0],
                     dataset[1],
                     dataset[2],
                     dataset[3],
                     dataset[4],dataset[5],dataset[6])
        return emp

    def get_all_employee(self):
        sql = "SELECT * FROM employee"
        dataset = self.fetchall(sql,None)
        print(dataset)
        employees=[]
        for dataset in dataset:
            emp = Employee(dataset[0],
                           dataset[1],
                           dataset[2],
                           dataset[3],
                           dataset[4], dataset[5], dataset[6])
            employees.append(emp)
        return employees

    def get_detail_infor(self,id):
        sql = "SELECT * FROM employee " \
        "where ID=%s"
        val = (id, )
        dataset = self.fetchone(sql,val)
        if dataset==None:
            return None
        emp = Employee(dataset[0],
                       dataset[1],
                       dataset[2],
                       dataset[3],
                       dataset[4], dataset[5], dataset[6])
        return emp
