from PyQt6.QtWidgets import QApplication, QMainWindow

from RetailProject.UI.LoginMainWindowEx import LoginWindowEx

app = QApplication([])
loginWindow = LoginWindowEx()
loginWindow.setupUi(QMainWindow())
app.exec()