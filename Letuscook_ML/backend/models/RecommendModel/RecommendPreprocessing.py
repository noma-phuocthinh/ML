import os
import pandas as pd
import re

class FoodPreprocessing:
    """Tiền xử lý dữ liệu food"""
    def __init__(self):
        pass

    def loadRawData(self, path: str):
        print("Đang bắt đầu xử lý dữ liệu ...")
        raw_data = pd.read_csv(path)
        print(f"Đã load raw data ở {path} thành công!")
        return raw_data

    def filterColumns(self, raw_data: pd.DataFrame):
        """
        Lọc các cột dữ liệu sử dụng
        """
        feature_columns = [
            'RecipeId','Name', 'DatePublished','Images','Calories', 'ProteinContent','FatContent',
            'CarbohydrateContent', 'RecipeIngredientParts','RecipeInstructions'
        ]
        print("Đã lựa chọn feature cho hệ thống:", feature_columns)
        return raw_data[feature_columns]

    def dropDuplicates(self, df: pd.DataFrame):
        """
        Xử lý trùng lặp. Ở đây không tính các cột RecipeId, DatePublished vì nó chỉ là những cột định danh
        """
        _ = [
            'Name', 'Images','Calories', 'ProteinContent','FatContent',
            'CarbohydrateContent', 'RecipeIngredientParts','RecipeInstructions'
        ]
        return df.drop_duplicates(subset=_, keep = 'first')

    def validImages(self, text):
        """
        Phát hiện đường link hợp lệ
        :return: list or None
        """
        if not isinstance(text, str):
            return None
        urls = re.findall(r'(https?://[^\s]+)', text)
        return urls if urls else None

    def cleanText(self, text):
        """
        Làm sạch dữ liệu text - loại bỏ ký tự lạ [@#$%^&*!`~]
        """
        text = re.sub(r'[@#$%^&*!`~]', '', text)
        text = text.lower()
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        return text

    def convertTextToList(self, text):
        # Loại bỏ chữ 'c' (viết hoa hoặc viết thường) và dấu ngoặc
        input_str = re.sub(r"^[cC]\s*\(|\)$", "", text)

        # Tìm tất cả các từ giữa dấu nháy đơn hoặc nháy kép, bao gồm cả các từ không có nháy
        words = re.findall(r"'([^']*)'|\"([^\"]*)\"|(\S+)", input_str)

        # Tạo danh sách từ các phần tử đã tách, bỏ qua các phần tử rỗng hoặc dấu phẩy
        result = [word[0] or word[1] or word[2] for word in words if
                  (word[0] or word[1] or word[2]) and word[0] != ',' and word[1] != ',' and word[2] != ',']
        return result

    def filterByNutrition(self, df, max_values=None):
        """
        Lọc ngưỡng dinh dưỡng phù hợp
        :param max_values: Ngưỡng dinh dưỡng
        """
        if max_values is None:
            max_values = [2000, 200, 100, 325]
        _ = ['Calories', 'ProteinContent', 'FatContent', 'CarbohydrateContent']
        for column, maximum in zip(_, max_values):
            df = df[df[column] < maximum]
        return df

    def removeNull(self, df):
        c = df.isnull().sum().sum()
        if c > 0:
            print(f"Phát hiện {c} giá trị null → xoá toàn bộ dòng chứa null.")
            df = df.dropna()
        return df

    def saveCleanedData(self,df, path: str):
        """
        :param path: địa chỉ lưu file
        """
        # Nếu chưa có thư mục thì tự tạo
        os.makedirs(os.path.dirname(path), exist_ok=True)
        df.to_csv(path, index=False)
        print(f"Đã lưu cleaned data tại: {path}")

    def runPipeline(self, load_path: str, max_values=None, save_path: str = None):
        """Thực hiện toàn bộ pipeline: load data, xử lý, và lưu kết quả"""
        raw_data = self.loadRawData(load_path)
        processed_data = self.filterColumns(raw_data)
        processed_data = self.dropDuplicates(processed_data)
        print("Đã xử lý xong dữ liệu trùng lặp")
        processed_data = self.removeNull(processed_data)
        if processed_data is None:
            print("Lỗi: Dữ liệu bị None sau bước xử lý null.")
            return

        processed_data = self.filterByNutrition(processed_data, max_values)
        processed_data['Name'] = processed_data['Name'].apply(self.cleanText)
        processed_data['RecipeInstructions'] = processed_data['RecipeInstructions'].apply(self.convertTextToList)
        processed_data['RecipeIngredientParts'] = processed_data['RecipeIngredientParts'].apply(self.convertTextToList)
        processed_data["Images"] = processed_data['Images'].apply(self.validImages)
        print("Đã xử lý xong, bắt đầu lưu dữ liệu")
        if save_path:
            self.saveCleanedData(processed_data, save_path)
        return processed_data