from backend.models.RecommendModel.RecommendPreprocessing import FoodPreprocessing
from common.CommonFunc import getProjectRoot

rootpath = getProjectRoot()
foodpre = FoodPreprocessing()
foodcleaned = foodpre.runPipeline(load_path=rootpath/"data"/"raw"/"food_dataset.csv", save_path=rootpath/"data"/"processed"/"food_dataset.csv")
