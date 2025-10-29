import matplotlib.pyplot as plt
import numpy as np

# Dữ liệu
x = np.array([[73.5, 75., 76.5, 79., 81.5, 82.5, 84., 85., 86.5, 87.5, 89., 90., 91.5]]).T
y = np.array([[1.49, 1.5, 1.51, 1.54, 1.58, 1.59, 1.60, 1.62, 1.63, 1.64, 1.66, 1.67, 1.68]]).T


# Hàm tính hồi quy
def calculateLibB(x, y):
    xbar = np.mean(x)
    ybar = np.mean(y)
    xzbar = np.mean(x ** 2)
    xyear = np.mean(x * y)

    b1 = (xbar * ybar - xyear) / (xbar ** 2 - xzbar)
    b0 = ybar - b1 * xbar
    return b1, b0


# Hàm vẽ đồ thị
def showGraph(x, y, y_predicted, title="", xlabel="", ylabel=""):
    plt.figure(figsize=(14, 8))
    plt.plot(x, y, 'r-o', label="price")
    plt.plot(x, y_predicted, 'b-x', label="predicted value")

    x_min = np.min(x)
    x_max = np.max(x)
    y_min = np.min(y)
    y_max = np.max(y)

    ybar = np.mean(y)

    plt.axhline(ybar, linestyle='--', linewidth=4, label="mean")
    plt.axis([x_min * 0.95, x_max * 1.05, y_min * 0.95, y_max * 1.05])
    plt.xlabel(xlabel, fontsize=16)
    plt.ylabel(ylabel, fontsize=16)
    plt.text(x_min, ybar * 1.01, s="mean", fontsize=16)
    plt.legend(fontsize=15)
    plt.title(title, fontsize=20)
    plt.show()


# Tính toán và hiển thị
b1, b0 = calculateLibB(x, y)
print(f"b1: {b1}")
print(f"b0: {b0}")

y_predicted = b0 + b1 * x

showGraph(x, y, y_predicted,
          title='Giá nhà theo diện tích',
          xlabel='Diện tích (m2)',
          ylabel='Giá nhà (tỷ VND)')