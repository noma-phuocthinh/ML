import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from itertools import combinations

# 1. Dữ liệu gốc cho một truy vấn (Pointwise format)
data_original = pd.DataFrame({
    'query_id': ['Q1', 'Q1', 'Q1'],
    'doc_id': ['Doc_A', 'Doc_B', 'Doc_C'],
    'feature_1': [0.9, 0.5, 0.7],  # Ví dụ: độ khớp từ khóa
    'feature_2': [80, 30, 50],     # Ví dụ: điểm uy tín trang
    'relevance_label': [2, 0, 1]   # Nhãn liên quan: 2 (cao), 1(TB), 0(thấp)
})

print("Dữ liệu gốc (Pointwise):")
print(data_original)

# 2. Chuyển đổi dữ liệu sang dạng Pairwise
pairs = []
features = ['feature_1', 'feature_2']

# Duyệt qua tất cả các cặp tài liệu có thể
for (idx1, row1), (idx2, row2) in combinations(data_original.iterrows(), 2):
    if row1['relevance_label'] > row2['relevance_label']:
        # Tài liệu 1 liên quan hơn tài liệu 2
        doc_winner = row1
        doc_loser = row2
        label = 1  # Winner nên được xếp cao hơn Loser
    elif row1['relevance_label'] < row2['relevance_label']:
        # Tài liệu 2 liên quan hơn tài liệu 1
        doc_winner = row2
        doc_loser = row1
        label = 1
    else:
        # Hai tài liệu có độ liên quan ngang nhau, bỏ qua hoặc gán nhãn 0.5
        continue

    # Tạo feature vector cho cặp: thường là hiệu số các đặc trưng
    feature_vector = doc_winner[features].values - doc_loser[features].values

    pairs.append({
        'query_id': row1['query_id'],
        'doc_winner': doc_winner['doc_id'],
        'doc_loser': doc_loser['doc_id'],
        'feature_diff': feature_vector,
        'label': label
    })

# Tạo DataFrame cho dữ liệu Pairwise
df_pairs = pd.DataFrame(pairs)
print("\nDữ liệu sau khi chuyển đổi sang Pairwise:")
print(df_pairs[['doc_winner', 'doc_loser', 'label']])

# 3. Chuẩn bị dữ liệu huấn luyện
X = np.vstack(df_pairs['feature_diff'].values)  # Ma trận đặc trưng
y = df_pairs['label'].values                    # Vector nhãn

# 4. Huấn luyện mô hình phân loại nhị phân (Binary Classification)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X, y)

print(f"\nMô hình đã được huấn luyện trên {len(X)} cặp dữ liệu.")

# 5. Dự đoán cho một cặp mới
# Giả sử ta muốn so sánh 2 tài liệu mới: Doc_X và Doc_Y
feature_doc_x = np.array([0.85, 70])  # Đặc trưng của Doc_X
feature_doc_y = np.array([0.60, 45])  # Đặc trưng của Doc_Y

# Tạo vector đặc trưng cho cặp (X, Y)
feature_diff_new = feature_doc_x - feature_doc_y

# Dự đoán xác suất: P(Doc_X liên quan hơn Doc_Y)
probability_xy = model.predict_proba([feature_diff_new])[0][1]

print(f"\nDự đoán cho cặp (Doc_X, Doc_Y):")
print(f"Xác suất Doc_X liên quan hơn Doc_Y: {probability_xy:.4f}")

if probability_xy > 0.5:
    print("Kết luận: Doc_X NÊN được xếp cao hơn Doc_Y")
else:
    print("Kết luận: Doc_Y NÊN được xếp cao hơn Doc_X")