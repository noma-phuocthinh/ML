import mysql.connector
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns


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


def gom_cum_khach_hang_kmeans(conn, n_clusters=4):
    """
    Gom cụm khách hàng về mức độ quan tâm Film và Inventory sử dụng K-Means
    """
    try:
        # Truy vấn để lấy các thuộc tính cho phân cụm
        sql = """
        SELECT 
            c.customer_id AS customer_id,
            CONCAT(c.first_name, ' ', c.last_name) AS customer_name,

            -- Thuộc tính về tần suất thuê
            COUNT(r.rental_id) AS total_rentals,
            COUNT(DISTINCT f.film_id) AS unique_films_rented,
            COUNT(DISTINCT i.inventory_id) AS unique_inventories_used,

            -- Thuộc tính về đa dạng thể loại
            COUNT(DISTINCT fc.category_id) AS categories_explored,

            -- Thuộc tính về thời gian hoạt động
            DATEDIFF(MAX(r.rental_date), MIN(r.rental_date)) AS rental_period_days,

            -- Thuộc tính về độ mới của phim (release year)
            AVG(f.release_year) AS avg_film_release_year,

            -- Thuộc tính về giá thuê
            AVG(f.rental_rate) AS avg_rental_rate,
            SUM(p.amount) AS total_spent,

            -- Thuộc tính về rating phim (chuyển đổi thành số)
            AVG(CASE 
                WHEN f.rating = 'G' THEN 1
                WHEN f.rating = 'PG' THEN 2
                WHEN f.rating = 'PG-13' THEN 3
                WHEN f.rating = 'R' THEN 4
                WHEN f.rating = 'NC-17' THEN 5
                ELSE 0
            END) AS avg_film_rating_numeric,

            -- Thuộc tính về độ dài phim
            AVG(f.length) AS avg_film_length,

            -- Tần suất thuê gần đây (số ngày kể từ lần thuê cuối)
            DATEDIFF('2006-02-14', MAX(r.rental_date)) AS days_since_last_rental

        FROM customer c
        INNER JOIN rental r ON c.customer_id = r.customer_id
        INNER JOIN inventory i ON r.inventory_id = i.inventory_id
        INNER JOIN film f ON i.film_id = f.film_id
        INNER JOIN film_category fc ON f.film_id = fc.film_id
        INNER JOIN payment p ON r.rental_id = p.rental_id
        GROUP BY c.customer_id
        HAVING total_rentals > 0
        ORDER BY total_rentals DESC
        """

        df = queryDataset(conn, sql)

        if df.empty:
            print("Không có dữ liệu để phân cụm")
            return None

        # Chuẩn bị dữ liệu cho K-Means
        features = [
            'total_rentals', 'unique_films_rented', 'unique_inventories_used',
            'categories_explored', 'avg_film_release_year', 'avg_rental_rate',
            'total_spent', 'avg_film_rating_numeric', 'avg_film_length',
            'days_since_last_rental'
        ]

        X = df[features].fillna(0)

        # Chuẩn hóa dữ liệu
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Thực hiện K-Means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(X_scaled)

        # Thêm nhóm cụm vào dataframe
        df['cluster'] = clusters

        # Tính silhouette score để đánh giá chất lượng cụm
        silhouette_avg = silhouette_score(X_scaled, clusters)
        print(f"Silhouette Score: {silhouette_avg:.3f}")

        # Phân tích đặc điểm từng cụm
        cluster_analysis = df.groupby('cluster')[features].mean()

        # Đặt tên cho các cụm dựa trên đặc điểm
        cluster_names = {}
        for cluster_id in range(n_clusters):
            cluster_data = cluster_analysis.loc[cluster_id]

            # Phân loại dựa trên đặc điểm nổi bật
            if cluster_data['total_rentals'] > cluster_analysis['total_rentals'].mean():
                if cluster_data['days_since_last_rental'] < cluster_analysis['days_since_last_rental'].mean():
                    cluster_names[cluster_id] = "Khách hàng tích cực"
                else:
                    cluster_names[cluster_id] = "Khách hàng trung thành cũ"
            else:
                if cluster_data['avg_rental_rate'] > cluster_analysis['avg_rental_rate'].mean():
                    cluster_names[cluster_id] = "Khách hàng cao cấp"
                else:
                    cluster_names[cluster_id] = "Khách hàng thỉnh thoảng"

        df['cluster_name'] = df['cluster'].map(cluster_names)

        # Hiển thị kết quả
        print("\n" + "=" * 80)
        print("KẾT QUẢ PHÂN CỤM KHÁCH HÀNG")
        print("=" * 80)

        print(f"\nTổng số khách hàng được phân cụm: {len(df)}")
        print(f"Số lượng cụm: {n_clusters}")

        print("\nPHÂN BỐ KHÁCH HÀNG THEO CỤM:")
        cluster_distribution = df['cluster_name'].value_counts()
        print(cluster_distribution)

        print("\nĐẶC ĐIỂM CÁC CỤM:")
        for cluster_id in range(n_clusters):
            cluster_df = df[df['cluster'] == cluster_id]
            print(f"\n--- {cluster_names[cluster_id]} (Cụm {cluster_id}) - {len(cluster_df)} khách hàng ---")
            print(f"  - Tổng số lượt thuê trung bình: {cluster_df['total_rentals'].mean():.1f}")
            print(f"  - Số phim độc nhất trung bình: {cluster_df['unique_films_rented'].mean():.1f}")
            print(f"  - Tổng chi tiêu trung bình: ${cluster_df['total_spent'].mean():.2f}")
            print(f"  - Số ngày từ lần thuê cuối: {cluster_df['days_since_last_rental'].mean():.1f} ngày")

        # Trực quan hóa kết quả
        visualize_clusters(df, features)

        return df

    except Exception as e:
        print("Lỗi khi thực hiện phân cụm:", e)
        return None


def visualize_clusters(df, features):
    """
    Trực quan hóa kết quả phân cụm
    """
    try:
        plt.figure(figsize=(15, 10))

        # Biểu đồ 1: Phân bố cụm
        plt.subplot(2, 2, 1)
        df['cluster_name'].value_counts().plot(kind='bar', color='skyblue')
        plt.title('Phân bố khách hàng theo cụm')
        plt.xticks(rotation=45)
        plt.ylabel('Số lượng khách hàng')

        # Biểu đồ 2: Tổng số lượt thuê vs Tổng chi tiêu
        plt.subplot(2, 2, 2)
        scatter = plt.scatter(df['total_rentals'], df['total_spent'],
                              c=df['cluster'], cmap='viridis', alpha=0.6)
        plt.xlabel('Tổng số lượt thuê')
        plt.ylabel('Tổng chi tiêu ($)')
        plt.title('Phân cụm theo lượt thuê và chi tiêu')
        plt.colorbar(scatter, label='Cụm')

        # Biểu đồ 3: Số phim độc nhất vs Số thể loại
        plt.subplot(2, 2, 3)
        scatter = plt.scatter(df['unique_films_rented'], df['categories_explored'],
                              c=df['cluster'], cmap='viridis', alpha=0.6)
        plt.xlabel('Số phim độc nhất đã thuê')
        plt.ylabel('Số thể loại đã khám phá')
        plt.title('Phân cụm theo đa dạng phim và thể loại')
        plt.colorbar(scatter, label='Cụm')

        # Biểu đồ 4: Độ dài phim trung bình vs Rating trung bình
        plt.subplot(2, 2, 4)
        scatter = plt.scatter(df['avg_film_length'], df['avg_film_rating_numeric'],
                              c=df['cluster'], cmap='viridis', alpha=0.6)
        plt.xlabel('Độ dài phim trung bình (phút)')
        plt.ylabel('Rating phim trung bình')
        plt.title('Phân cụm theo đặc điểm phim ưa thích')
        plt.colorbar(scatter, label='Cụm')

        plt.tight_layout()
        plt.savefig('phan_cum_khach_hang.png', dpi=300, bbox_inches='tight')
        plt.show()

        # Lưu kết quả ra file CSV
        df.to_csv('ket_qua_phan_cum_khach_hang.csv', index=False)
        print(f"\nĐã lưu kết quả phân cụm ra file: ket_qua_phan_cum_khach_hang.csv")
        print("Đã lưu biểu đồ trực quan ra file: phan_cum_khach_hang.png")

    except Exception as e:
        print("Lỗi khi trực quan hóa:", e)


# Kết nối và thực hiện phân cụm
conn = getConnect('localhost', 3306, 'sakila', 'root', '@Obama123')

if conn is not None:
    try:
        print("=" * 80)
        print("PHÂN CỤM KHÁCH HÀNG SỬ DỤNG K-MEANS")
        print("=" * 80)

        # Thực hiện phân cụm với 4 cụm
        df_clusters = gom_cum_khach_hang_kmeans(conn, n_clusters=4)

        if df_clusters is not None:
            print("\n" + "=" * 80)
            print("DANH SÁCH KHÁCH HÀNG THEO CỤM")
            print("=" * 80)

            # Hiển thị 15 khách hàng đầu tiên với thông tin cụm
            display_columns = ['customer_id', 'customer_name', 'cluster_name',
                               'total_rentals', 'unique_films_rented', 'total_spent']
            print(df_clusters[display_columns].head(15))

    except Exception as e:
        print("Lỗi khi thực hiện phân cụm:", e)
    finally:
        closeConnection(conn)
else:
    print("Không thể kết nối đến database")