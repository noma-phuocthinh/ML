from PyQt6.QtWidgets import QMessageBox, QMainWindow
from RetailProject.Connectors.Employee_Connector import Employee_Connector
from RetailProject.UI import EmployeeMainWindowEx
from RetailProject.UI.LoginMainWindow import Ui_MainWindow
from RetailProject.UI.EmployeeMainWindowEx import EmployeeMainWindowEx

class LoginWindowEx(Ui_MainWindow):
    def __init__(self):
        pass
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.showWindow()
        self.setupSignalandSlots()

    def showWindow(self):
        self.MainWindow.show()
    def setupSignalandSlots(self):
        self.pushButtonLogin.clicked.connect(self.processLogin)
    def processLogin(self):
        email = self.lineEditEmail.text()
        password = self.lineEditPassword.text()
        empc = Employee_Connector()
        empc.connect()
        emp = empc.login(email, password)
        if emp is None:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setText("Employee Connector Login Failed")
            msg.setWindowTitle("Login Falied")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        else:
            print("akjsdfjsgjdgi")
            self.gui_emp = EmployeeMainWindowEx()
            self.gui_emp.setupUi(QMainWindow())
            self.gui_emp.showWindow()
            self.MainWindow.close()
