import mysql.connector
from Ngay8_10.models.customer import Customer

server="localhost"
port=3306
database="k23416_retail"
username="root"
password="@Obama123"

conn = mysql.connector.connect(
                host=server,
                port=port,
                database=database,
                user=username,
                password=password)
#Đăng nhập vào hệ thống
def log_customer(email, pwd):
    cursor = conn.cursor()
    sql = "SELECT * FROM customer " \
          "where Email='" + email + "' and Password='" + pwd + "'"
    cust =None
    cursor.execute(sql)
    dataset = cursor.fetchone()

    if dataset is not None:
        cust = Customer()
        cust.ID,cust.Name,cust.Phone,cust.Email,cust.Password
    cursor.close()
    return cust


cust = log_customer("daodao@gmail.com", "123")
if cust == None:
    print("Đăng nhập thất bại")
else:
    print("Đăng nhập thành công")