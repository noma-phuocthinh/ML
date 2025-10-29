import traceback

import mysql.connector

from RetailProject.Models.Customer import Customer

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
# Câu 1: Đăng nhập cho customer
def login_customer(email, password):
    cursor = conn.cursor()
    sql = ("select * from customer "
           "where Email='") + email + "' and Password='" + password +"'"
    cus = None
    cursor.execute(sql)
    result = cursor.fetchone()
    if result:
        cus = Customer(result[0], result[1], result[2], result[3], result[4], result[5])
        # cus.ID, cus.Name, cus.Phone, cus.Email, cus.Password, cus.IsDeleted = result
    cursor.close()
    return cus
cus = login_customer("obama@gmail.com", "123")
if cus == None:
    print("Login failed!")
else:
    print("Login succeeded!")
    print(cus)