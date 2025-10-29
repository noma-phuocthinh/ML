import mysql.connector


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

print("Thành công")

#Đăng nhập vào hệ thống
def log_customer(email, pwd):
    cursor = conn.cursor()
    sql = "SELECT * FROM customer " \
          "where Email='" + email + "' and Password='" + pwd + "'"
    cursor.execute(sql)

    dataset = cursor.fetchone()
    if dataset is not None:
        print(dataset)
    else:
        print("Đăng nhập không thành công")

    cursor.close()

log_customer("daodao@gmail.com", "123")

def login_employee(email, pwd):
    cursor = conn.cursor()
    sql = "SELECT * FROM employee WHERE Email=%s AND Password=%s"
    val = (email, pwd)
    cursor.execute(sql, val)
    dataset = cursor.fetchone()
    if dataset is not None:
        print(dataset)
    else:
        print("Đăng nhập không thành công")
    cursor.close()

login_employee("putin@gmail.com", "123")
