from RetailProject.Connectors.Employee_Connector import Employee_Connector
from RetailProject.Models.Employee import Employee

empc = Employee_Connector()
emp = empc.login("putin@gmail.com", "123")
if emp is None:
    print("Employee Connector Login Failed")
else:
    print("Employee Connector Login Succeeded")
    print(emp)

# Test get all employee
print("List of Emps:")
ds = empc.getAllEmployee()
for emp in ds:
    print(emp)

id = 2
emp = empc.getDetailEmployee(id)
if emp is None:
    print("Không có nhân viên nào có mã = ", id)
else:
    print("Employee:\n", emp)
print("-"*50)
# Test new employee
emp = Employee(None, "EMP3", "Linda", "0981232568", "linda@gmail.com", "123", "0")
print("Thêm 1 dòng: ", emp)
result = empc.insertOneEmployee(emp)
if result <= 0:
    print("Không insert được")
else:
    print('Chúc mừng!')