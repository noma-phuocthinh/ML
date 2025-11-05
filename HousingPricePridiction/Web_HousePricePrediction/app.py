from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np
import os
import traceback

app = Flask(__name__)



def load_model():
    model_path = "D:/ML/HousingPricePridiction/models/housing_price_model.pkl"
    try:
        print(f"Đang load model từ: {model_path}")

        # Kiểm tra file có tồn tại không
        if not os.path.exists(model_path):
            print("❌ File model không tồn tại!")
            return None

        with open(model_path, 'rb') as file:
            model = pickle.load(file)
        print("✅ Model loaded successfully!")
        print(f"Model type: {type(model)}")
        return model
    except Exception as e:
        print(f"❌ Lỗi khi load model: {e}")
        traceback.print_exc()
        return None


trained_model = load_model()


@app.route("/")
def main():
    return render_template("index.html")


@app.route("/doprediction", methods=["POST"])
def doprediction():
    try:
        print("📨 Nhận request dự đoán...")
        print(f"Form data: {request.form}")

        # Lấy dữ liệu từ form
        area_income_value = float(request.form["area_income_value"])
        area_house_age_value = float(request.form["area_house_age_value"])
        area_number_of_rooms_value = float(request.form["area_number_of_rooms_value"])
        area_number_of_bedrooms_value = float(request.form["area_number_of_bedrooms_value"])
        area_population_value = float(request.form["area_population_value"])

        print(
            f"Input values: {area_income_value}, {area_house_age_value}, {area_number_of_rooms_value}, {area_number_of_bedrooms_value}, {area_population_value}")

        if trained_model is None:
            print("❌ Model is None")
            return jsonify({"error": "Model không thể load"}), 500

        # Tạo input cho model prediction
        input_features = np.array([[area_income_value,
                                    area_house_age_value,
                                    area_number_of_rooms_value,
                                    area_number_of_bedrooms_value,
                                    area_population_value]])

        print(f"Input features shape: {input_features.shape}")
        print(f"Input features: {input_features}")

        # Dự đoán giá nhà
        result = trained_model.predict(input_features)
        print(f"Raw prediction result: {result}")

        # Format kết quả
        predicted_price = f"{result[0]:,.2f}"
        print(f"Formatted price: {predicted_price}")

        return predicted_price

    except Exception as e:
        print(f"❌ Lỗi khi dự đoán: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)