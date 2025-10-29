import sqlite3
import pandas as pd


def get_customers_with_min_invoices(n, db_path='../../databases/Chinook_Sqlite.sqlite'):
    """
    Lấy danh sách khách hàng có số lượng invoice tham gia >= N
    """
    try:
        conn = sqlite3.connect(db_path)
        query = '''
            SELECT 
                c.CustomerId, 
                c.FirstName, 
                c.LastName, 
                c.Email,
                c.Country,
                COUNT(i.InvoiceId) AS InvoiceCount,
                SUM(i.Total) AS TotalSpent
            FROM Customer c
            JOIN Invoice i ON c.CustomerId = i.CustomerId
            GROUP BY c.CustomerId, c.FirstName, c.LastName, c.Email, c.Country
            HAVING COUNT(i.InvoiceId) >= ?
            ORDER BY InvoiceCount DESC, TotalSpent DESC;
        '''
        df = pd.read_sql_query(query, conn, params=(n,))
        return df

    except sqlite3.Error as e:
        print("Database error:", e)
        return pd.DataFrame()  # Trả về DataFrame rỗng nếu có lỗi
    finally:
        if 'conn' in locals() and conn:
            conn.close()


# Phần code chính
try:
    sqliteConnection = sqlite3.connect('../../databases/Chinook_Sqlite.sqlite')
    cursor = sqliteConnection.cursor()
    print('DB Init')

    # Query 1: Lấy 5 dòng đầu từ InvoiceLine
    query1 = 'SELECT * FROM InvoiceLine LIMIT 5;'
    cursor.execute(query1)
    column_names = [description[0] for description in cursor.description]
    df_invoice_line = pd.DataFrame(cursor.fetchall(), columns=column_names)

    print("=== 5 DÒNG ĐẦU TỪ BẢNG InvoiceLine ===")
    print(df_invoice_line)
    print("\n" + "=" * 50 + "\n")

    cursor.close()

except sqlite3.Error as error:
    print('Error while connecting to sqlite', error)

finally:
    if sqliteConnection:
        sqliteConnection.close()
        print('sqlite connection closed')

# Gọi hàm mới để lấy khách hàng có ít nhất 5 invoice
print("=== KHÁCH HÀNG CÓ ÍT NHẤT 5 INVOICE ===")
df_customers = get_customers_with_min_invoices(5)

if not df_customers.empty:
    print(f"Tìm thấy {len(df_customers)} khách hàng có từ 5 invoice trở lên:")
    print(df_customers.to_string(index=False))

    # Hiển thị thống kê
    print("\n=== THỐNG KÊ ===")
    print(f"Tổng số khách hàng: {len(df_customers)}")
    print(f"Số invoice trung bình: {df_customers['InvoiceCount'].mean():.1f}")
    print(f"Số invoice cao nhất: {df_customers['InvoiceCount'].max()}")
    print(f"Số invoice thấp nhất: {df_customers['InvoiceCount'].min()}")
    print(f"Tổng chi tiêu: ${df_customers['TotalSpent'].sum():.2f}")
else:
    print("Không tìm thấy khách hàng nào thỏa điều kiện")

# Test với các giá trị N khác nhau
print("\n" + "=" * 50)
print("=== TEST VỚI CÁC GIÁ TRỊ N KHÁC NHAU ===")

for n in [3, 7, 10]:
    df_test = get_customers_with_min_invoices(n)
    if not df_test.empty:
        print(f"\nKhách hàng có ít nhất {n} invoice ({len(df_test)} khách hàng):")
        print(f"- Số invoice trung bình: {df_test['InvoiceCount'].mean():.1f}")
        print(f"- Tổng chi tiêu: ${df_test['TotalSpent'].sum():.2f}")
    else:
        print(f"\nKhông có khách hàng nào có ít nhất {n} invoice")