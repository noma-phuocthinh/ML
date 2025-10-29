import mysql.connector
import pandas as pd
import numpy as np
import os
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


def chuyen_csv_sang_excel(duong_dan_csv, duong_dan_excel=None):
    """
    Chuyển đổi file CSV sang file Excel

    Parameters:
    - duong_dan_csv: Đường dẫn đến file CSV cần chuyển đổi
    - duong_dan_excel: Đường dẫn đến file Excel đầu ra (nếu None sẽ tự động tạo)

    Returns:
    - True nếu thành công, False nếu thất bại
    """
    try:
        # Kiểm tra file CSV có tồn tại không
        if not os.path.exists(duong_dan_csv):
            print(f"Lỗi: File CSV không tồn tại - {duong_dan_csv}")
            return False

        # Đọc file CSV
        print(f"Đang đọc file CSV: {duong_dan_csv}")
        df = pd.read_csv(duong_dan_csv)
        print(f"Đọc thành công: {len(df)} dòng, {len(df.columns)} cột")

        # Tạo đường dẫn Excel nếu không được cung cấp
        if duong_dan_excel is None:
            duong_dan_excel = duong_dan_csv.replace('.csv', '.xlsx')

        # Đảm bảo thư mục đích tồn tại
        os.makedirs(os.path.dirname(duong_dan_excel) if os.path.dirname(duong_dan_excel) else '.', exist_ok=True)

        # Ghi ra file Excel
        print(f"Đang ghi file Excel: {duong_dan_excel}")
        with pd.ExcelWriter(duong_dan_excel, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='Data', index=False)

            # Tạo sheet thống kê
            thong_ke_data = {
                'Thong_Ke': ['Tổng số bản ghi', 'Số cột dữ liệu', 'Ngày xuất báo cáo'],
                'Gia_Tri': [len(df), len(df.columns), pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')]
            }
            pd.DataFrame(thong_ke_data).to_excel(writer, sheet_name='ThongKe', index=False)

        print(f"✅ Chuyển đổi thành công!")
        print(f"📂 CSV: {duong_dan_csv}")
        print(f"📂 Excel: {duong_dan_excel}")
        print(f"📊 Số dòng: {len(df)}")
        print(f"📋 Số cột: {len(df.columns)}")

        return True

    except Exception as e:
        print(f"❌ Lỗi khi chuyển đổi: {e}")
        return False


def luu_dataframe_excel(df, ten_file, thu_muc='.'):
    """
    Lưu DataFrame trực tiếp ra file Excel với nhiều sheet

    Parameters:
    - df: DataFrame cần lưu
    - ten_file: Tên file (không cần đuôi .xlsx)
    - thu_muc: Thư mục lưu file
    """
    try:
        duong_dan = os.path.join(thu_muc, f"{ten_file}.xlsx")

        # Đảm bảo thư mục tồn tại
        os.makedirs(thu_muc, exist_ok=True)

        with pd.ExcelWriter(duong_dan, engine='openpyxl') as writer:
            # Sheet dữ liệu chính
            df.to_excel(writer, sheet_name='DuLieu', index=False)

            # Sheet thống kê
            thong_ke = {
                'Thong_Ke': ['Tổng số bản ghi', 'Số cột', 'Ngày tạo'],
                'Gia_Tri': [len(df), len(df.columns), pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')]
            }
            pd.DataFrame(thong_ke).to_excel(writer, sheet_name='ThongKe', index=False)

            # Sheet thông tin cột
            column_info = {
                'Ten_Cot': df.columns.tolist(),
                'Kieu_Du_Lieu': [str(dtype) for dtype in df.dtypes],
                'So_Gia_Tri_Non_Null': [df[col].count() for col in df.columns]
            }
            pd.DataFrame(column_info).to_excel(writer, sheet_name='ThongTinCot', index=False)

        print(f"✅ Đã lưu DataFrame ra file: {duong_dan}")
        print(f"📊 Số dòng: {len(df)}, Số cột: {len(df.columns)}")

        return duong_dan

    except Exception as e:
        print(f"❌ Lỗi khi lưu Excel: {e}")
        return None


def phan_loai_khach_hang_theo_phim(conn):
    """
    Phân loại khách hàng theo tên phim - những khách hàng nào đã thuê phim nào
    """
    try:
        sql = """
        SELECT 
            f.title AS Ten_Phim,
            c.customer_id AS Ma_Khach_Hang,
            CONCAT(c.first_name, ' ', c.last_name) AS Ten_Khach_Hang,
            c.email AS Email,
            COUNT(r.rental_id) AS So_Lan_Thue,
            MAX(r.rental_date) AS Lan_Thue_Gan_Nhat
        FROM film f
        INNER JOIN inventory i ON f.film_id = i.film_id
        INNER JOIN rental r ON i.inventory_id = r.inventory_id
        INNER JOIN customer c ON r.customer_id = c.customer_id
        GROUP BY f.film_id, c.customer_id
        ORDER BY f.title, c.customer_id
        """

        df = queryDataset(conn, sql)

        # Lưu trực tiếp ra Excel thay vì CSV
        if df is not None and not df.empty:
            luu_dataframe_excel(df, 'phan_loai_khach_hang_theo_phim', 'output')

        return df

    except Exception as e:
        print("Lỗi khi phân loại khách hàng theo phim:", e)
        return None


def phan_loai_khach_hang_theo_category(conn):
    """
    Phân loại khách hàng theo category - những khách hàng nào đã thuê phim thuộc category nào
    Loại bỏ dữ liệu trùng lặp (mỗi khách hàng chỉ xuất hiện 1 lần trong 1 category)
    """
    try:
        sql = """
        SELECT DISTINCT
            cat.name AS Ten_Category,
            c.customer_id AS Ma_Khach_Hang,
            CONCAT(c.first_name, ' ', c.last_name) AS Ten_Khach_Hang,
            c.email AS Email,
            COUNT(r.rental_id) AS So_Luot_Thue_Trong_Category,
            MAX(r.rental_date) AS Lan_Thue_Gan_Nhat
        FROM category cat
        INNER JOIN film_category fc ON cat.category_id = fc.category_id
        INNER JOIN film f ON fc.film_id = f.film_id
        INNER JOIN inventory i ON f.film_id = i.film_id
        INNER JOIN rental r ON i.inventory_id = r.inventory_id
        INNER JOIN customer c ON r.customer_id = c.customer_id
        GROUP BY cat.category_id, c.customer_id
        ORDER BY cat.name, c.customer_id
        """

        df = queryDataset(conn, sql)

        # Lưu trực tiếp ra Excel thay vì CSV
        if df is not None and not df.empty:
            luu_dataframe_excel(df, 'phan_loai_khach_hang_theo_category', 'output')

        return df

    except Exception as e:
        print("Lỗi khi phân loại khách hàng theo category:", e)
        return None


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

        # Lưu kết quả phân cụm ra Excel
        if df is not None and not df.empty:
            luu_dataframe_excel(df, 'ket_qua_phan_cum_khach_hang', 'output')

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

        # Tạo thư mục output nếu chưa tồn tại
        os.makedirs('output', exist_ok=True)

        plt.savefig('output/phan_cum_khach_hang.png', dpi=300, bbox_inches='tight')
        plt.show()

        print("Đã lưu biểu đồ trực quan ra file: output/phan_cum_khach_hang.png")

    except Exception as e:
        print("Lỗi khi trực quan hóa:", e)


def chuyen_nhieu_csv_sang_excel(danh_sach_duong_dan):
    """
    Chuyển đổi nhiều file CSV sang Excel cùng lúc
    """
    thanh_cong = 0
    that_bai = 0

    for duong_dan_csv in danh_sach_duong_dan:
        print(f"\n{'=' * 50}")
        print(f"Xử lý file: {duong_dan_csv}")

        if chuyen_csv_sang_excel(duong_dan_csv):
            thanh_cong += 1
        else:
            that_bai += 1

    print(f"\n{'=' * 50}")
    print("🎯 TỔNG KẾT CHUYỂN ĐỔI:")
    print(f"✅ Thành công: {thanh_cong} file")
    print(f"❌ Thất bại: {that_bai} file")

    return thanh_cong, that_bai


# Kết nối và thực hiện phân cụm
conn = getConnect('localhost', 3306, 'sakila', 'root', '@Obama123')

if conn is not None:
    try:
        # Tạo thư mục output
        os.makedirs('output', exist_ok=True)

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

        print("\n" + "=" * 80)
        print("PHÂN LOẠI KHÁCH HÀNG THEO PHIM")
        print("=" * 80)

        # Phân loại khách hàng theo phim
        df_phan_loai_phim = phan_loai_khach_hang_theo_phim(conn)
        if df_phan_loai_phim is not None:
            print(f"Tổng số bản ghi phân loại theo phim: {len(df_phan_loai_phim)}")

        print("\n" + "=" * 80)
        print("PHÂN LOẠI KHÁCH HÀNG THEO CATEGORY")
        print("=" * 80)

        # Phân loại khách hàng theo category
        df_phan_loai_category = phan_loai_khach_hang_theo_category(conn)
        if df_phan_loai_category is not None:
            print(f"Tổng số bản ghi phân loại theo category: {len(df_phan_loai_category)}")

    except Exception as e:
        print("Lỗi khi thực hiện truy vấn:", e)
    finally:
        closeConnection(conn)
else:
    print("Không thể kết nối đến database")

# Ví dụ sử dụng hàm chuyển đổi CSV sang Excel
if __name__ == "__main__":
    # Nếu có file CSV cũ muốn chuyển đổi
    duong_dan_csv_cu = r"D:\ML\Ngay29_10\Sakila\ket_qua_phan_cum_khach_hang.csv"

    if os.path.exists(duong_dan_csv_cu):
        print("\n" + "=" * 80)
        print("CHUYỂN ĐỔI FILE CSV CŨ SANG EXCEL")
        print("=" * 80)
        chuyen_csv_sang_excel(duong_dan_csv_cu)