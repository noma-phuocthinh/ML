# Gồm 2 class:
# User: quản lý khai báo thông tin chung người dùng
# HealthyProfile: quản lý thông tin liên quan để sức khoẻ người dùng
from typing import Optional

import numpy as np


class HealthyProfile:
    """Thông tin chi tiết của người dùng"""
    def __init__(self,
        age: int,
        sex: str,
        weight: float,
        height: float,
        activity_level: str,
        family_history_with_overweight: str = None,
        favc: str = None,
        fcvc: float = None,
        ncp: float = None,
        caec: str = None,
        smoke: str = None,
        ch2o: float = None,
        scc: str = None,
        faf: float = None,
        tue: float = None,
        calc: str = None,
        mtrans: str = None,
        obesity_level: str = None,
        # Có nên cấu trúc thành Enum?
    ):
        # Hồ sơ sức khoẻ ban đầu --> Dùng để dự đoán tình trạng béo phì
        self.age = age
        self.sex = sex
        self.weight = weight
        self.height = height
        self.activity_level = activity_level
        self.family_history_with_overweight = family_history_with_overweight
        self.favc = favc
        self.fcvc = fcvc
        self.ncp = ncp
        self.caec = caec
        self.smoke = smoke
        self.ch2o = ch2o
        self.scc = scc
        self.faf = faf
        self.tue = tue
        self.calc = calc
        self.mstrans = mtrans
        self.obesity_level = obesity_level

        # Input người dùng về lộ trình kiểm soát cân nặng
        self.current_weight = weight # Cân nặng tại thời điểm hiện tại của user
        self.goal_weight = weight # Cân nặng mong muốn của user
        self.days = None # Số ngày để đạt được mục tiêu
        self.calories = None # Lượng calo cần thiết mỗi ngày theo mô hình Hall

    def defineMarcoMatrix(self, current_weight: float, goal_weight: float):
        """
        Ước lượng tỷ lệ protein, fat, carb với từng mục tiêu cân nặng
        :param current_weight: cân nặng tại t = 0
        :param goal_weight: cân nặng tại t = days
        :return: protein_ratio, fat_ratio, carb_ratio
        """
        if current_weight > goal_weight:
            return 0.3, 0.3, 0.4
        elif current_weight < goal_weight:
            return 0.25, 0.3, 0.45
        else:
            return 0.3, 0.3, 0.4
    def getCalories(self, service = None):
        """
        Tính lượng calo cần thiết mỗi ngày để đạt được goal_weight sau days ngày
        :param service: HallModelService
        :return: calories per day
        """
        if service:
            self.calories = service.calculateCalories(self.sex, self.age, self.current_weight, self.height, self.activity_level, self.goal_weight, self.days)
            return self.calories
        return 0

    def calculateMacro(self):
        """
        Ước lượng  protein, fat, carbs (gram/ngày)
        :return: protein, fat, carbs
        """
        if self.calories:
            protein_ratio, fat_ratio, carb_ratio = self.defineMarcoMatrix(self.current_weight, self.goal_weight)
            protein = (self.calories * protein_ratio) / 4
            fat = (self.calories * fat_ratio) / 9
            carbs = (self.calories * carb_ratio) / 4
            return protein, fat, carbs
        return 0, 0, 0
    @staticmethod
    def getVector(calories, protein, fat, carbs):
        """Vector đầu vào cho mô hình """
        return  np.array([calories, protein, fat, carbs], dtype=float)
    def __repr__(self):
        pass
class User:
    """ Thông tin chung của người dùng"""
    def __init__(self,
        user_id: int,
        username: str,
        email: str,
        password_hash: str,
        password_salt: str,
        full_name: str,
        phone_number: str,
        bio: Optional[str] = None,
        photo_url: Optional[str] = None,
        is_admin: int = None,
        ):
        self.user_id = user_id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.password_salt = password_salt
        self.full_name = full_name
        self.phone_number = phone_number
        self.bio = bio
        self.photo_url = photo_url
        self.is_admin = is_admin

    def __repr__(self):
        pass