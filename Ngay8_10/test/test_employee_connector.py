from Ngay8_10.connectors.employee_connector import EmployeeConnector

ec = EmployeeConnector()
ec.connect()
em =ec.login("putin@gmail.com","123")
if em==None:
    print("Login Failed")
else:
    print("Login Succesful")
    print(em)
