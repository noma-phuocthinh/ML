from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox, QMainWindow, QTableWidget, QTableWidgetItem
from Ngay8_10.uis.EmployeeMainWindow import Ui_MainWindow


class EmployeeMainWindowEx(Ui_MainWindow):
    def __init__(self):
        super().__init__()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.displayEmployeesIntoTable()
        self.setupSignalAndSlot()

    def showWindow(self):
        self.MainWindow.show()

    def displayEmployeesIntoTable(self):
        self.employees = self.ec.get_all_employee()
        self.tableWidget.setRowCount(0)
        for emp in self.employees:
            row = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row)
            item_id =QTableWidgetItem(str(emp.ID))
            self.tableWidget.setItem(row,0,item_id)

            if emp.IsDeleted == 1:
                item_id.setBackground(Qt.GlobalColor.red)

            item_code = QTableWidgetItem(str(emp.Code))
            self.tableWidget.setItem(row, 1, item_code)

            item_name = QTableWidgetItem(str(emp.Name))
            self.tableWidget.setItem(row, 2, item_name)

            item_phone = QTableWidgetItem(str(emp.Phone))
            self.tableWidget.setItem(row, 3, item_phone)

            item_email = QTableWidgetItem(str(emp.Email))
            self.tableWidget.setItem(row, 4, item_email)

    def setupSignalAndSlot(self):
        self.pushButtonNew.clicked.connect(self.clear_all)
        self.tableWidget.itemSelectionChanged.connect(self.show_detail)

    def clear_all(self):
        self.lineEditID.clear()
        self.lineEditName.clear()
        self.lineEditCode.clear()
        self.lineEditEmail.clear()
        self.lineEditPassword.clear()
        self.lineEditPhone.clear()

    def show_detail(self):
        row_index = self.tableWidget.currentIndex()
        print("you clicked at", row_index)
        id = self.tableWidget.setItem(row_index.row(),0).text
        print("Employee ID",id)
        emp = self.ec.get_detail_infor(id)
        if emp!=None:
            self.lineEditID.setText(str(emp.ID))
