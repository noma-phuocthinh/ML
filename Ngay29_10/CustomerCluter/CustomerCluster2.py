from flask import Flask
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.cluster import KMeans
import numpy as np

app = Flask(__name__)


def getConnect(server, port, database, username, password):
    try:
        conn = mysql.connector.connect(
            host=server,
            port=port,
            database=database,
            user=username,
            password=password
        )
        return conn
    except Exception as e:
        print("Error = ", e)
        return None


def closeConnection(conn):
    if conn is not None:
        conn.close()


def queryDataset(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    df = pd.DataFrame(cursor.fetchall())

    # Lấy tên cột
    if cursor.description:
        column_names = [i[0] for i in cursor.description]
        df.columns = column_names

    return df


# Kết nối và thực hiện truy vấn
conn = getConnect('localhost', 3306, 'salesdatabase', 'root', '@Obama123')

if conn is not None:
    try:
        sql1 = "select * from customer"
        df1 = queryDataset(conn, sql1)
        print(df1)

        sql2 = """select distinct customer.CustomerId, Age, Annual_Income, Spending_Score 
                  from customer, customer_spend_score 
                  where customer.CustomerId = customer_spend_score.CustomerID"""

        df2 = queryDataset(conn, sql2)
        df2.columns = ['CustomerId', 'Age', 'Annual Income', 'Spending Score']

        print(df2)
        print(df2.head())
        print(df2.describe())

    except Exception as e:
        print("Lỗi khi thực hiện truy vấn:", e)
    finally:
        closeConnection(conn)
else:
    print("Không thể kết nối đến database")


def showHistogram(df, columns):
    plt.figure(1, figsize=(10, 12))
    n = 0
    for column in columns:
        n += 1
        plt.subplot(3, 1, n)
        plt.subplots_adjust(hspace=0.5, wspace=0.5)

        # Sử dụng histplot thay cho distplot (đã deprecated)
        sns.histplot(df[column], bins=32, kde=True)
        plt.title(f'Histogram of {column}')

    plt.tight_layout()
    plt.show()


# Gọi hàm với các cột cần vẽ histogram (bỏ qua CustomerId)
showHistogram(df2, df2.columns[1:])


def elbowMethod(df, columnsForElbow):
    X = df.loc[:, columnsForElbow].values
    inertia = []
    for n in range(1, 11):
        model = KMeans(
            n_clusters=n,
            init='k-means++',
            max_iter=500,
            random_state=42
        )
        model.fit(X)
        inertia.append(model.inertia_)

    plt.figure(1, figsize=(15, 6))
    plt.plot(np.arange(1, 11), inertia, 'o')
    plt.plot(np.arange(1, 11), inertia, '-', alpha=0.5)
    plt.xlabel('Number of Clusters')
    plt.ylabel('Cluster sum of squared distances')
    plt.title('Elbow Method for Optimal Number of Clusters')
    plt.show()


columns = ['Age', 'Spending Score']
# Gọi hàm elbow method
elbowMethod(df2, columns)


def runKMeans(X, cluster):
    model = KMeans(n_clusters=cluster, init='k-means++', max_iter=500, random_state=42)
    model.fit(X)
    labels = model.labels_
    centroids = model.cluster_centers_
    y_kmeans = model.fit_predict(X)
    return y_kmeans, centroids, labels


X = df2.loc[:, columns].values
cluster = 5  # ĐÃ THAY ĐỔI TỪ 4 THÀNH 5
colors = ["red", "green", "blue", "purple", "black", "pink", "orange"]  # Đảm bảo có đủ 5 màu

y_kmeans, centroids, labels = runKMeans(X, cluster)
print("Cluster assignments:", y_kmeans)
print("Centroids:", centroids)
print("Labels:", labels)
df2["cluster"] = labels


def visualizeKMeans(X, y_kmeans, cluster, title, xlabel, ylabel, colors):
    plt.figure(figsize=(10, 10))
    for i in range(cluster):
        plt.scatter(X[y_kmeans == i, 0], X[y_kmeans == i, 1], s=100, c=colors[i], label='Cluster %i' % (i + 1))
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.legend()
    plt.show()


visualizeKMeans(X,
                y_kmeans,
                cluster,
                "Clusters of Customers - Age X Spending Score (k=5)",  # Đã cập nhật tiêu đề
                "Age",
                "Spending Score",
                colors)

# In thống kê các cụm
print("\nThống kê số lượng khách hàng trong mỗi cụm:")
print(df2['cluster'].value_counts().sort_index())

print("\nThống kê mô tả theo cụm:")
print(df2.groupby('cluster')[['Age', 'Spending Score']].describe())