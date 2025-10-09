import pickle
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.pipeline import Pipeline


class SearchNeighbor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.neigh = None
        self.pipeline = None
        self.df = None

    def loadCleanedData(self, path: str):
        """Tải dữ liệu đã làm sạch từ file CSV."""
        try:
            self.df = pd.read_csv(path)
            print(f"Đã tải dữ liệu từ {path} thành công!")
        except Exception as e:
            raise ValueError(f"Lỗi khi tải dữ liệu: {e}")
        return self.df
    def filterFeatureForModel(self):
        feature_columns = [
            'RecipeId','Calories', 'ProteinContent', 'FatContent',
            'CarbohydrateContent'
        ]
        print("Đã lựa chọn feature cho models", feature_columns)
        self.df = self.df[feature_columns]
        return self.df

    def _fitNeighbors(self, df: pd.DataFrame):
        """Huấn luyện mô hình Nearest Neighbors."""
        if df is None or df.empty:
            raise ValueError("Dữ liệu không hợp lệ hoặc trống.")

        feature_cols = ['Calories', 'ProteinContent', 'FatContent', 'CarbohydrateContent']
        if not all(col in df.columns for col in feature_cols):
            raise ValueError(f"Dữ liệu thiếu các cột cần thiết: {feature_cols}")

        # Chuẩn hóa 4 feature numeric
        prep_data = self.scaler.fit_transform(df[feature_cols].to_numpy())

        # Huấn luyện KNN
        self.neigh = NearestNeighbors(metric='euclidean', algorithm='brute')
        self.neigh.fit(prep_data)

    def _buildPipeline(self, params: dict):
        """Xây dựng pipeline với mô hình nearest neighbors."""
        transformer = FunctionTransformer(
            self.neigh.kneighbors,
            kw_args=params
        )
        self.pipeline = Pipeline([
            ('std_scaler', self.scaler),
            ('NN', transformer)
        ])

    def trainModel(self, path: str, params: dict):
        """Huấn luyện mô hình và tạo pipeline."""
        if path is None:
            raise ValueError("Cần truyền đường dẫn dữ liệu.")
        self.df = self.loadCleanedData(path)
        self.df = self.filterFeatureForModel()
        self._fitNeighbors(self.df)
        self._buildPipeline(params)
        print("Mô hình đã được huấn luyện và pipeline đã được tạo.")

    def saveModel(self, path: str):
        """Lưu mô hình đã huấn luyện."""
        if self.pipeline is None:
            raise ValueError("Mô hình chưa được huấn luyện.")
        with open(path, "wb") as f:
            pickle.dump({
                "scaler": self.scaler,
                "neigh": self.neigh,
                "pipeline": self.pipeline,
                "features": ['Calories', 'ProteinContent', 'FatContent', 'CarbohydrateContent']
            }, f)

        print(f"Mô hình đã được lưu tại {path}.")

    def loadModel(self, path: str):
        """Tải mô hình đã lưu."""
        try:
            with open(path, "rb") as f:
                data = pickle.load(f)
                self.scaler = data["scaler"]
                self.neigh = data["neigh"]
                self.pipeline = data["pipeline"]
            print(f"Mô hình đã được tải từ {path}.")
            return self
        except Exception as e:
            raise ValueError(f"Lỗi khi tải mô hình: {e}")