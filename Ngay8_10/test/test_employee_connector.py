from Ngay8_10.connectors.employee_connector import EmployeeConnector

ec = EmployeeConnector()
ec.connect()
em = ec.login("obama@gmail.com","123")

if em == None:
    print("Login failed?")
else:
    print("Login successful")
    print(em)
#tdxt
print("List of Emps")
ds = ec.get_all_employee()
print(ds)
for emp in ds:
    print(emp)

id=3
emp= ec.get_detail_employee(id)

if emp == None:
    print("Khoong thay cac nhan vien")
else:
    print(emp)