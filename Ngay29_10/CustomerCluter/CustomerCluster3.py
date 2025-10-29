from flask import Flask
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.cluster import KMeans
import numpy as np
from tabulate import tabulate

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
cluster = 6
colors = ["red", "green", "blue", "purple", "black", "pink", "orange", "yellow", "brown", "gray"]

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
                "Clusters of Customers - Age X Spending Score (k=6)",
                "Age",
                "Spending Score",
                colors)

# In thống kê các cụm
print("\nThống kê số lượng khách hàng trong mỗi cụm:")
print(df2['cluster'].value_counts().sort_index())

print("\nThống kê mô tả theo cụm:")
print(df2.groupby('cluster')[['Age', 'Spending Score']].describe())


# HÀM MỚI: Visualize 3D KMeans
def visualize3DKmeans(df, columns, hover_data, cluster):
    fig = px.scatter_3d(
        df,
        x=columns[0],
        y=columns[1],
        z='Annual Income',
        color='cluster',
        hover_data=hover_data,
        category_orders={"cluster": range(0, cluster)},
    )
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))
    fig.show()
    return fig


# HÀM MỚI: Xuất file HTML 3D
def export3DToHTML(df, columns, hover_data, cluster, filename='3d_cluster_visualization.html'):
    fig = visualize3DKmeans(df, columns, hover_data, cluster)
    fig.write_html(filename)
    print(f"Đã xuất file 3D thành công: {filename}")


# HÀM MỚI: Xuất file CSV với kết quả phân cụm
def exportClustersToCSV(df, filename='customer_clusters_results.csv'):
    df.to_csv(filename, index=False, encoding='utf-8-sig')
    print(f"Đã xuất file CSV thành công: {filename}")


# HÀM MỚI: Xuất bảng chi tiết khách hàng theo cụm ra CONSOLE
def display_cluster_tables_console(df):
    """
    Hiển thị bảng chi tiết khách hàng theo cụm ra console dạng bảng
    """
    print("\n" + "=" * 100)
    print("BẢNG CHI TIẾT KHÁCH HÀNG THEO CỤM")
    print("=" * 100)

    for cluster_id in sorted(df['cluster'].unique()):
        cluster_data = df[df['cluster'] == cluster_id].copy()
        cluster_data = cluster_data.sort_values('CustomerId')

        # Chuẩn bị dữ liệu cho bảng
        table_data = []
        for idx, row in cluster_data.iterrows():
            table_data.append([
                row['CustomerId'],
                row['Age'],
                f"{row['Annual Income']:.1f}",
                row['Spending Score'],
                f"Cluster {cluster_id}"
            ])

        # Thống kê cụm
        avg_age = cluster_data['Age'].mean()
        avg_income = cluster_data['Annual Income'].mean()
        avg_spending = cluster_data['Spending Score'].mean()

        print(f"\n🎯 CỤM {cluster_id} - {len(cluster_data)} KHÁCH HÀNG")
        print(
            f"📊 Thống kê: Tuổi TB: {avg_age:.1f} | Thu nhập TB: {avg_income:.1f} | Điểm chi tiêu TB: {avg_spending:.1f}")
        print("-" * 80)

        # Hiển thị bảng
        headers = ["Customer ID", "Age", "Annual Income", "Spending Score", "Cluster"]
        print(tabulate(table_data, headers=headers, tablefmt="grid", numalign="center"))
        print(f"\nTổng số: {len(cluster_data)} khách hàng")
        print("=" * 80)


# HÀM MỚI: Xuất bảng HTML chi tiết khách hàng theo cụm
def display_cluster_tables_web(df, cluster_id=None):
    """
    Tạo bảng HTML chi tiết khách hàng theo cụm
    """
    if cluster_id is not None:
        cluster_data = df[df['cluster'] == cluster_id].copy()
    else:
        cluster_data = df.copy()

    cluster_data = cluster_data.sort_values('CustomerId')

    # Tạo bảng HTML
    html_table = """
    <table border="1" style="border-collapse: collapse; width: 100%; margin: 10px 0;">
        <thead>
            <tr style="background-color: #4CAF50; color: white;">
                <th style="padding: 8px; text-align: center;">Customer ID</th>
                <th style="padding: 8px; text-align: center;">Age</th>
                <th style="padding: 8px; text-align: center;">Annual Income</th>
                <th style="padding: 8px; text-align: center;">Spending Score</th>
                <th style="padding: 8px; text-align: center;">Cluster</th>
            </tr>
        </thead>
        <tbody>
    """

    for idx, row in cluster_data.iterrows():
        html_table += f"""
            <tr>
                <td style="padding: 8px; text-align: center;">{row['CustomerId']}</td>
                <td style="padding: 8px; text-align: center;">{row['Age']}</td>
                <td style="padding: 8px; text-align: center;">{row['Annual Income']:.1f}</td>
                <td style="padding: 8px; text-align: center;">{row['Spending Score']}</td>
                <td style="padding: 8px; text-align: center; font-weight: bold;">Cluster {row['cluster']}</td>
            </tr>
        """

    html_table += """
        </tbody>
    </table>
    """

    return html_table


# CẬP NHẬT Route Flask để hiển thị bảng
@app.route('/')
def index():
    return """
    <html>
    <head>
        <title>Customer Clustering Results</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .cluster { margin: 20px 0; padding: 15px; border: 2px solid #ddd; border-radius: 10px; }
            .cluster-0 { border-color: #ff4444; background-color: #ffebee; }
            .cluster-1 { border-color: #44ff44; background-color: #e8f5e8; }
            .cluster-2 { border-color: #4444ff; background-color: #e3f2fd; }
            .cluster-3 { border-color: #ff44ff; background-color: #f3e5f5; }
            .cluster-4 { border-color: #000000; background-color: #f5f5f5; }
            .cluster-5 { border-color: #ff69b4; background-color: #fff0f6; }
            .stats { font-weight: bold; color: #333; margin: 15px 0; padding: 10px; background: #e9ecef; border-radius: 5px; }
            .back-link { display: block; margin: 10px 0; color: #007bff; text-decoration: none; }
            .back-link:hover { text-decoration: underline; }
            table { width: 100%; margin: 10px 0; }
            th { background-color: #4CAF50; color: white; padding: 10px; }
            td { padding: 8px; text-align: center; border-bottom: 1px solid #ddd; }
            tr:nth-child(even) { background-color: #f2f2f2; }
            tr:hover { background-color: #e9ecef; }
        </style>
    </head>
    <body>
        <h1>🎯 Kết Quả Phân Cụm Khách Hàng (K=6)</h1>
        <a href="/clusters" class="back-link">📊 Xem bảng chi tiết tất cả các cụm</a><br>
        <a href="/cluster/0" class="back-link">🔴 Cụm 0</a> | 
        <a href="/cluster/1" class="back-link">🟢 Cụm 1</a> | 
        <a href="/cluster/2" class="back-link">🔵 Cụm 2</a> | 
        <a href="/cluster/3" class="back-link">🟣 Cụm 3</a> | 
        <a href="/cluster/4" class="back-link">⚫ Cụm 4</a> | 
        <a href="/cluster/5" class="back-link">🎀 Cụm 5</a>
    </body>
    </html>
    """


@app.route('/clusters')
def display_all_clusters_tables():
    """Hiển thị tất cả các cụm dạng bảng trên web"""
    html_content = """
    <html>
    <head>
        <title>All Clusters - Tables</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 20px; }
            .cluster-section { margin: 30px 0; padding: 20px; border: 2px solid #ddd; border-radius: 10px; }
            .stats { font-weight: bold; color: #333; margin: 15px 0; padding: 10px; background: #e9ecef; border-radius: 5px; }
            .back-link { display: block; margin: 10px 0; color: #007bff; text-decoration: none; }
            table { width: 100%; margin: 10px 0; border-collapse: collapse; }
            th { background-color: #4CAF50; color: white; padding: 12px; text-align: center; }
            td { padding: 10px; text-align: center; border-bottom: 1px solid #ddd; }
            tr:nth-child(even) { background-color: #f2f2f2; }
            tr:hover { background-color: #e9ecef; }
        </style>
    </head>
    <body>
        <h1>📊 Bảng Chi Tiết Tất Cả Các Cụm Khách Hàng</h1>
        <a href="/" class="back-link">← Quay lại trang chủ</a>
    """

    for cluster_id in sorted(df2['cluster'].unique()):
        cluster_data = df2[df2['cluster'] == cluster_id]
        avg_age = cluster_data['Age'].mean()
        avg_income = cluster_data['Annual Income'].mean()
        avg_spending = cluster_data['Spending Score'].mean()

        html_content += f"""
        <div class="cluster-section">
            <h2>🔹 Cụm {cluster_id} - {len(cluster_data)} Khách Hàng</h2>
            <div class="stats">
                📊 Thống kê: Tuổi trung bình: {avg_age:.1f} | Thu nhập trung bình: {avg_income:.1f} | Điểm chi tiêu trung bình: {avg_spending:.1f}
            </div>
            {display_cluster_tables_web(df2, cluster_id)}
        </div>
        """

    html_content += "</body></html>"
    return html_content


@app.route('/cluster/<int:cluster_id>')
def display_single_cluster_table(cluster_id):
    """Hiển thị 1 cụm cụ thể dạng bảng trên web"""
    cluster_data = df2[df2['cluster'] == cluster_id]

    if cluster_data.empty:
        return f"<h1>Không tìm thấy cụm {cluster_id}</h1><a href='/clusters'>Quay lại</a>"

    avg_age = cluster_data['Age'].mean()
    avg_income = cluster_data['Annual Income'].mean()
    avg_spending = cluster_data['Spending Score'].mean()

    html_content = f"""
    <html>
    <head>
        <title>Cluster {cluster_id} - Table</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .cluster-section {{ margin: 20px 0; padding: 20px; border: 2px solid {colors[cluster_id]}; border-radius: 10px; background-color: #f8f9fa; }}
            .stats {{ font-weight: bold; color: #333; margin: 15px 0; padding: 15px; background: #e9ecef; border-radius: 5px; }}
            .back-link {{ display: block; margin: 10px 0; color: #007bff; text-decoration: none; }}
            table {{ width: 100%; margin: 10px 0; border-collapse: collapse; }}
            th {{ background-color: #4CAF50; color: white; padding: 12px; text-align: center; }}
            td {{ padding: 10px; text-align: center; border-bottom: 1px solid #ddd; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
            tr:hover {{ background-color: #e9ecef; }}
        </style>
    </head>
    <body>
        <h1>🔹 Cụm {cluster_id} - {len(cluster_data)} Khách Hàng</h1>
        <a href="/clusters" class="back-link">← Quay lại danh sách cụm</a>
        <a href="/" class="back-link">← Quay lại trang chủ</a>

        <div class="stats">
            📊 Thống kê cụm:<br>
            • Tuổi trung bình: {avg_age:.1f}<br>
            • Thu nhập trung bình: {avg_income:.1f}<br>
            • Điểm chi tiêu trung bình: {avg_spending:.1f}
        </div>

        <div class="cluster-section">
            <h3>📋 Bảng danh sách khách hàng:</h3>
            {display_cluster_tables_web(df2, cluster_id)}
        </div>
    </body>
    </html>
    """
    return html_content


# Sử dụng các hàm mới
hover_data = df2.columns.tolist()

# Hiển thị biểu đồ 3D
visualize3DKmeans(df2, columns, hover_data, cluster)

# Xuất file HTML 3D
export3DToHTML(df2, columns, hover_data, cluster, 'customer_clusters_3d.html')

# Xuất file CSV với kết quả phân cụm
exportClustersToCSV(df2, 'customer_clusters_results.csv')

# HIỂN THỊ BẢNG CHI TIẾT RA CONSOLE
display_cluster_tables_console(df2)

# In thông báo hoàn thành
print("\n" + "=" * 50)
print("HOÀN THÀNH PHÂN CỤM VỚI K=6")
print("=" * 50)
print(f"Tổng số cụm: {cluster}")
print(f"Tổng số khách hàng: {len(df2)}")
print(f"Phân bố các cụm:")
for i in range(cluster):
    count = len(df2[df2['cluster'] == i])
    percentage = (count / len(df2)) * 100
    print(f"  Cluster {i}: {count} khách hàng ({percentage:.1f}%)")

# CHẠY FLASK APP VỚI PORT 60963
if __name__ == '__main__':
    print("\n🌐 Khởi chạy Flask Web Server...")
    print("📱 Truy cập: http://127.0.0.1:60963/")
    print("⏹️  Nhấn Ctrl+C để dừng server")
    app.run(debug=True, host='127.0.0.1', port=60963)