import pandas as pd
import numpy as np
import lightgbm as lgb
from sklearn.model_selection import train_test_split

# 1. Tạo dữ liệu mẫu với nhiều truy vấn (quan trọng trong Listwise)
np.random.seed(42)
data = []

# Tạo dữ liệu cho 3 truy vấn khác nhau, mỗi truy vấn có 4 tài liệu
queries = ['Q1', 'Q2', 'Q3']
for query_id in queries:
    for doc_id in range(4):  # 4 tài liệu cho mỗi truy vấn
        data.append({
            'query_id': query_id,
            'doc_id': f'{query_id}_Doc_{doc_id}',
            'feature_1': np.random.uniform(0.5, 1.0),
            'feature_2': np.random.randint(10, 100),
            'feature_3': np.random.uniform(0, 1),
            # Tạo nhãn liên quan dựa trên các đặc trưng (giả lập)
            'relevance_label': int(np.random.choice([0, 1, 2], p=[0.3, 0.5, 0.2]))
        })

df = pd.DataFrame(data)
print("Dữ liệu gốc (có cấu trúc theo danh sách - listwise):")
print(df.head(8)) # Hiển thị 2 truy vấn đầu tiên

# 2. Chuẩn bị dữ liệu theo định dạng Listwise cho LightGBM
# LightGBM yêu cầu chỉ định độ dài của mỗi danh sách (truy vấn)
query_groups = df.groupby('query_id').size().values
print(f"\nSố tài liệu cho mỗi truy vấn: {query_groups}")

# Đặc trưng và nhãn
features = ['feature_1', 'feature_2', 'feature_3']
X = df[features]
y = df['relevance_label']

# 3. Tạo Dataset cho LightGBM với thông tin nhóm (query)
lgb_train = lgb.Dataset(
    X,
    y,
    group=query_groups,  # Tham số QUAN TRỌNG: chỉ định độ dài mỗi danh sách
    free_raw_data=False
)

# 4. Thiết lập tham số cho mô hình Listwise (sử dụng Lambdarank)
params = {
    'objective': 'lambdarank',  # Mục tiêu xếp hạng dựa trên Listwise
    'metric': 'ndcg',           # Chỉ số đánh giá: NDCG
    'ndcg_eval_at': [3],        # Tính NDCG@3
    'learning_rate': 0.05,
    'verbose': -1
}

# 5. Huấn luyện mô hình
model = lgb.train(
    params,
    lgb_train,
    num_boost_round=100
)

print("\nMô hình Listwise (LambdaRank) đã được huấn luyện!")

# 6. Dự đoán và minh họa kết quả xếp hạng cho một truy vấn mới
# Giả sử có một truy vấn mới Q4 với 3 tài liệu
new_query_data = pd.DataFrame({
    'doc_id': ['Q4_Doc_A', 'Q4_Doc_B', 'Q4_Doc_C'],
    'feature_1': [0.95, 0.75, 0.85],
    'feature_2': [95, 45, 75],
    'feature_3': [0.9, 0.6, 0.8]
})

# Dự đoán điểm số (không phải nhãn) cho các tài liệu
X_new = new_query_data[features]
predicted_scores = model.predict(X_new)

new_query_data['predicted_score'] = predicted_scores
new_query_data['predicted_rank'] = new_query_data['predicted_score'].rank(ascending=False).astype(int)

print("\nKết quả xếp hạng cho truy vấn mới Q4:")
print(new_query_data.sort_values('predicted_rank'))

# 7. Đánh giá chất lượng xếp hạng (giả lập nhãn thật để tính NDCG)
# Giả sử nhãn liên quan thật sự của các tài liệu
true_relevance = np.array([2, 0, 1]) # Nhãn thật: A rất liên quan, B không liên quan, C bình thường

# Tính NDCG thực tế
from sklearn.metrics import ndcg_score
ndcg_value = ndcg_score([true_relevance], [predicted_scores])
print(f"\nChất lượng xếp hạng (NDCG): {ndcg_value:.4f}")

# Phân tích kết quả
print("\nPhân tích:")
if ndcg_value > 0.8:
    print("Mô hình tạo ra thứ hạng rất tốt, phù hợp với nhãn liên quan thực tế.")
elif ndcg_value > 0.5:
    print("Mô hình tạo ra thứ hạng khá tốt.")
else:
    print("Thứ hạng cần được cải thiện.")