import traceback

import mysql.connector

server = "localhost"
port = 3306
database = "k23416_retail"
username = "root"
password = "@Obama123"
try:
    conn = mysql.connector.connect(
        host=server,
        port=port,
        database=database,
        user=username,
        password=password,
    )

    print("Successfully connected to MySQL ")
except:
    traceback.print_exc()
print("Continue")
print("--CRUD--")
# Câu 1: Đăng nhập cho customer
def login_customer(email, password):
    cursor = conn.cursor()
    sql = ("select * from customer "
           "where Email='") + email + "' and Password='" + password +"'"
    print(sql)
    cursor.execute(sql)
    result = cursor.fetchone()
    if result:
        print(result)
    else:
        print("Login failed!")
    cursor.close()
    return result
login_customer("obama@gmail.com", "123")

#Câu 2. Đăng nhập employee
def login_employee(email, password):
    cursor = conn.cursor()
    sql = ("select * from employee "
           "where Email=%s and Password=%s")
    val = (email, password) # 1 cái thì có dấu phẩy, 2 cái trở lên thì không cần
    cursor.execute(sql, val)
    result = cursor.fetchone()
    if result:
        print(result)
    else:
        print("Login failed!")
    cursor.close()
    return result
login_employee("ngocmy@gmail.com", "123")