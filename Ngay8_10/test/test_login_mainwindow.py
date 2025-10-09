from PyQt6.QtWidgets import QApplication, QMainWindow

from Ngay8_10.uis.LoginMainWindowEx import LoginMainWindowEx

app = QApplication([])
loginWindow = LoginMainWindowEx()
loginWindow.setupUi(QMainWindow())
loginWindow.showWindow()
app.exec()