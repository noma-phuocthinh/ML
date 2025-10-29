import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

# Tạo dữ liệu giả lập
np.random.seed(42)
num_samples = 1000

# Giả sử mỗi mẫu có 4 đặc trưng
data = {
    'feature1': np.random.rand(num_samples) * 10,  # Đặc trưng 1
    'feature2': np.random.rand(num_samples) * 5,   # Đặc trưng 2
    'feature3': np.random.rand(num_samples) * 8,   # Đặc trưng 3
    'feature4': np.random.rand(num_samples) * 12   # Đặc trưng 4
}

df = pd.DataFrame(data)

# Tạo nhãn liên quan (giả lập) dựa trên các đặc trưng với nhiễu
# Giả sử nhãn liên quan là giá trị thực từ 0 đến 5
df['relevance'] = (0.5 * df['feature1'] + 0.3 * df['feature2'] + 0.2 * df['feature3'] + 0.1 * df['feature4']) / 10
df['relevance'] += np.random.normal(0, 0.1, num_samples)  # Thêm nhiễu
df['relevance'] = np.clip(df['relevance'], 0, 5)  # Giới hạn trong [0, 5]

# Chia tập dữ liệu
X = df[['feature1', 'feature2', 'feature3', 'feature4']]
y = df['relevance']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Huấn luyện mô hình Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Đánh giá mô hình
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)
print(f"R² trên tập huấn luyện: {train_score:.4f}")
print(f"R² trên tập kiểm tra: {test_score:.4f}")

# Giả sử chúng ta có một truy vấn mới với 3 tài liệu cần xếp hạng
new_docs = pd.DataFrame({
    'feature1': [8.5, 7.0, 9.2],
    'feature2': [4.2, 3.8, 4.5],
    'feature3': [6.7, 5.5, 7.8],
    'feature4': [10.0, 9.5, 11.2]
})

# Dự đoán điểm liên quan cho các tài liệu mới
predicted_scores = model.predict(new_docs)
print("Điểm dự đoán cho các tài liệu mới:", predicted_scores)

# Xếp hạng các tài liệu theo điểm dự đoán giảm dần
ranking_order = np.argsort(-predicted_scores)  # argsort giảm dần
print("Thứ hạng của các tài liệu (theo chỉ số):", ranking_order)
print("Thứ hạng của các tài liệu (theo điểm):", predicted_scores[ranking_order])