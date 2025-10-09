import io
import pathlib

import py_mini_racer

from common.CommonFunc import getProjectRoot


class HallModelService:
    FILES = ["baseline.js", "dailyparams.js", "bodychange.js",
             "bodymodel.js", "intervention.js", "wrapper.js"]

    def __init__(self):
        """
        :param base_path: Đường dẫn tới folder chứa FILES
        """
        self.rootpath = getProjectRoot()
        self.base_path = self.rootpath/"backend"/"models"/"HallModelService"/"src"
        self.ctx = py_mini_racer.MiniRacer()
        for f in self.FILES:
            with io.open(str(self.base_path) + "/"+ f, "r", encoding="utf-8") as jsfile:
                self.ctx.eval(jsfile.read())
    def calculateCalories(self, sex: str, age: int, current_weight: float, height: float, pal : float, goal_weight: float, days: float):
        """
        Tính lượng calo cần thiết mỗi này
        :param sex: giới tính = "male" or "female"
        :param age: tuổi
        :param current_weight: cân nặng tại t = 0
        :param height: chiều cao
        :param pal: mức độ hoạt động
        :param goal_weight: cân nặng tại thời điểm t = days
        :param days: số ngày để đạt được goal_weight
        :return: calories per day
        """
        isMale = sex.lower() == "male"
        return self.ctx.call("calorieAPI", isMale, age, height, current_weight, goal_weight, pal, days)
