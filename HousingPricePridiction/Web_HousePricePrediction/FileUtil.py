import pickle
import os


class FileUtil:
    @staticmethod
    def Loadmodel(model_path):
        """
        Load trained model từ file pickle
        """
        try:
            print(f"Đang load model từ: {model_path}")

            if not os.path.exists(model_path):
                print("❌ File model không tồn tại!")
                return None

            with open(model_path, 'rb') as file:
                model = pickle.load(file)
            print("✅ Model loaded successfully!")
            return model
        except Exception as e:
            print(f"❌ Lỗi khi load model: {e}")
            return None