from backend.models.RecommendModel.RecommendModel import SearchNeighbor
from common.CommonFunc import getProjectRoot

# Tạo đối tượng SearchNeighbor
searcher = SearchNeighbor()

# Huấn luyện mô hình
params = {"n_neighbors": 1}
rootpath = getProjectRoot()
loadpath = rootpath/"data"/"processed"/"food_dataset.csv"
searcher.trainModel(loadpath, params)

# Lưu mô hình
savepath = rootpath/"backend"/"models"/"RecommendModel"
searcher.saveModel(savepath/"knn_model.pkl")