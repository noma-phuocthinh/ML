import pandas as pd

def find_orders_within_range(df, minValue, maxValue):
    order_tolals = df.groupby('OrderID').apply(lambda x: (x['UnitPrice']*x['Quantity']*(1-x['Discount'])).sum())

    orders_within_range = order_tolals[(order_tolals >= minValue)&(order_tolals <=maxValue)]

    unique_orders = df[df['OrderID'].isin(orders_within_range.index)]['OrderID'].drop_duplicates().tolist()

    return unique_orders

df = pd.read_csv('D:/ML/dataset/SalesTransactions.csv')

minValue = float(input('Enter the minimum price: '))
maxValue = float(input('Enter the maximum price: '))

result = find_orders_within_range(df, minValue, maxValue)

print('Danh sách các hóa đơn trong phạm vi từ', minValue, 'đến', maxValue, 'là', result)