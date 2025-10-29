import sqlite3
import pandas as pd
try:
    sqliteConnection = sqlite3.connect('../databases/Chinook_Sqlite.sqlite')
    cursor = sqliteConnection.cursor()
    print("DB Init")

    query = "SELECT * FROM InvoiceLine LIMIT 5;"
    cursor.execute(query)

    # Lấy dữ liệu
    rows = cursor.fetchall()

    # Lấy tên cột từ cursor.description
    col_names = [desc[0] for desc in cursor.description]

    # Tạo DataFrame với tên cột
    df = pd.DataFrame(rows, columns=col_names)
    print(df)
    cursor.close()
except sqlite3.Error as error:
    print("Error occured", error)
finally:
    if sqliteConnection:
        sqliteConnection.close()
        print("sqlite connection closed")
