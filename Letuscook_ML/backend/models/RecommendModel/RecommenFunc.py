import numpy as np
import pandas as pd
from typing import Optional, List

from backend.models.EnumClasses import Meal
from backend.models.HallModelService.HallModelService import HallModelService
from backend.models.RecommendModel.RecommendModel import SearchNeighbor
from backend.models.User import HealthyProfile
from common.CommonFunc import getProjectRoot



class RecommendFood:
    def __init__(self, user: Optional["HealthyProfile"] = None):
        # Load model
        self.rootpath = getProjectRoot()
        model = SearchNeighbor()
        self.model = model.loadModel(self.rootpath/"backend"/"models"/"RecommendModel"/"knn_model.pkl")
        self.healthyprofile = user
        self.food_dataset = pd.read_csv(self.rootpath/"data"/"processed"/"food_dataset.csv")

    def setMealRatios(self, choice: Meal):
        ratios = {
            Meal.BREAKFAST: (0.5, 0.25, 0.25),
            Meal.LUNCH: (0.25, 0.5, 0.25),
            Meal.DINNER: (0.25, 0.25, 0.5),
            Meal.NONE: (1 / 3, 1 / 3, 1 / 3)
        }
        return ratios.get(choice, (1 / 3, 1 / 3, 1 / 3))

    def recommendFood(self, meal_choice: Meal):
        """Hàm gợi ý thực phẩm dựa trên vector người dùng và tỷ lệ bữa ăn"""
        service = HallModelService()
        calories = self.healthyprofile.getCalories(service=service)

        protein, fat, carbs = self.healthyprofile.calculateMacro()
        userVector = np.array(self.healthyprofile.getVector(calories, protein, fat, carbs))

        breakfast_ratio, lunch_ratio, dinner_ratio = self.setMealRatios(meal_choice)

        # Tính vector 2D đúng format
        breakfast_vector = (userVector * breakfast_ratio).reshape(1, -1)
        lunch_vector = (userVector * lunch_ratio).reshape(1, -1)
        dinner_vector = (userVector * dinner_ratio).reshape(1, -1)

        # Debug shape
        print("Shape:", breakfast_vector.shape, "Expected:", self.model.neigh.n_features_in_)

        # Tìm nearest neighbors
        _, breakfast_idx = self.model.neigh.kneighbors(breakfast_vector, n_neighbors=1)
        _, lunch_idx = self.model.neigh.kneighbors(lunch_vector, n_neighbors=1)
        _, dinner_idx = self.model.neigh.kneighbors(dinner_vector, n_neighbors=1)

        # Flatten chỉ số
        breakfast_idx = breakfast_idx[0][0]
        lunch_idx = lunch_idx[0][0]
        dinner_idx = dinner_idx[0][0]

        # Lấy thông tin món ăn
        recommended_food = [
            self.food_dataset.iloc[breakfast_idx].to_dict(),
            self.food_dataset.iloc[lunch_idx].to_dict(),
            self.food_dataset.iloc[dinner_idx].to_dict()
        ]
        return recommended_food