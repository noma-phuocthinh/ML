from backend.models.EnumClasses import Meal
from backend.models.RecommendModel.RecommenFunc import RecommendFood
from backend.models.User import HealthyProfile

healthya = HealthyProfile(28, "female", 60, 155, 1.6, 4, )
healthya.days = 180
healthya.goal_weight = 50
re = RecommendFood(healthya)
print(re.recommendFood(Meal.BREAKFAST))