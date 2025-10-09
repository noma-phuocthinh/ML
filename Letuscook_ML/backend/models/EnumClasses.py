# Class này để thiết kế danh sách Enum cần thiết
from enum import Enum

class Meal(Enum):
    """Định nghĩa các bữa ăn trong ngày"""
    BREAKFAST = "Breakfast"
    LUNCH = "Lunch"
    DINNER = "Dinner"
    NONE = "None"

    def __str__(self):
        return self.value

