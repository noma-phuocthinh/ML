from PyQt6.QtWidgets import QMessageBox
from Ngay8_10.uis.LoginMainWindow import Ui_MainWindow
from Ngay8_10.connectors.employee_connector import EmployeeConnector  # Thêm import


class LoginMainWindowEx(Ui_MainWindow):
    def __init__(self):
        super().__init__()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.setupSignalAndSlot()  # Sửa: Gọi hàm, không gán

    def showWindow(self):
        self.MainWindow.show()

    def setupSignalAndSlot(self):  # Sửa lỗi chính tả: Signal thay vì Singal
        self.pushButtonLogin.clicked.connect(self.process_login)  # Sửa: clicked thay vì click()

    def process_login(self):
        email = self.lineEditEmail.text()
        pwd = self.lineEditPassWord.text()

        ec = EmployeeConnector()
        ec.connect()
        em = ec.login(email, pwd)  # Sửa: dùng email và pwd từ lineEdit

        if em is None:
            msg = QMessageBox()
            msg.setText("Đăng nhập thất bại")
            msg.setWindowTitle("Không đăng nhập được")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        else:
            msg = QMessageBox()
            msg.setText("Đăng nhập thành công")  # Sửa lỗi chính tả
            msg.setWindowTitle("Đăng nhập được")
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)

        msg.exec()