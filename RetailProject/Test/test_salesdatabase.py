from RetailProject.Connectors.Connector import Connector

conn = Connector(database='salesdatabase')
conn.connect()
sql = 'select * from customer'
df = conn.queryDataset(sql)

if df is not None:
    print(df)
    print(df.columns)
else:
    print("Không lấy được dữ liệu")

conn.disConnect()  # Sửa thành disConnect() với chữ D viết hoa