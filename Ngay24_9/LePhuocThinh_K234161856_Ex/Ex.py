import pandas as pd

def find_top3_products(df):
    # Tính giá trị bán ra cho từng sản phẩm trong mỗi đơn hàng
    df['SalesValue'] = df['UnitPrice'] * df['Quantity'] * (1 - df['Discount'])

    # Nhóm theo ProductID và tính tổng giá trị bán ra
    product_sales = df.groupby('ProductID').agg({
        'SalesValue': 'sum',
        'UnitPrice': 'first',  # Lấy đơn giá đầu tiên để tham khảo
        'Quantity': 'sum'  # Tổng số lượng bán ra
    }).reset_index()

    # Sắp xếp theo giá trị bán ra giảm dần và lấy top 3
    top3_products = product_sales.nlargest(3, 'SalesValue')

    return top3_products

def find_top3_product_categories(df):
    # Tính giá trị bán ra
    df['SalesValue'] = df['UnitPrice'] * df['Quantity'] * (1 - df['Discount'])

    # Nhóm theo loại sản phẩm (giả sử ProductID 2 chữ số đầu là Category)
    df['Category'] = df['ProductID'] // 100  # Giả định category từ ProductID

    category_sales = df.groupby('Category').agg({
        'SalesValue': 'sum',
        'ProductID': 'nunique'  # Số lượng sản phẩm khác nhau trong category
    }).reset_index()

    # Sắp xếp và lấy top 3 categories
    top3_categories = category_sales.nlargest(3, 'SalesValue')

    return top3_categories

file_path = '../../dataset/SalesTransactions.csv'
# Đọc dữ liệu
df = pd.read_csv(file_path)

print("=== TOP 3 SẢN PHẨM CÓ GIÁ TRỊ BÁN RA CAO NHẤT ===")
top3_products = find_top3_products(df)
print(top3_products)

print("\n=== TOP 3 LOẠI SẢN PHẨM CÓ GIÁ TRỊ BÁN RA CAO NHẤT ===")
top3_categories = find_top3_product_categories(df)
print(top3_categories)

# Hiển thị kết quả chi tiết
print("\n=== CHI TIẾT TOP 3 SẢN PHẨM ===")
for idx, row in top3_products.iterrows():
    print(f"Top {idx + 1}:")
    print(f"  ProductID: {row['ProductID']}")
    print(f"  Tổng giá trị bán ra: ${row['SalesValue']:,.2f}")
    print(f"  Tổng số lượng: {row['Quantity']}")
    print(f"  Đơn giá trung bình: ${row['UnitPrice']:.2f}")
    print()