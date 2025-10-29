from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem, QMessageBox
from RetailProject.Models.Employee import Employee
from RetailProject.Connectors.Employee_Connector import Employee_Connector
from RetailProject.UI.EmployeeMainWindow import Ui_MainWindow


class EmployeeMainWindowEx(Ui_MainWindow):
    def __init__(self):
        self.empc = Employee_Connector()

    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.MainWindow = MainWindow
        self.displayEmployeeIntoTable()
        self.setupSignalAndSlot()

    def showWindow(self):
        self.MainWindow.show()

    def displayEmployeeIntoTable(self):
        self.employees = self.empc.getAllEmployee()
        # Remove existing data
        self.tableWidget_ListEmp.setRowCount(0)
        # Loading emp into table
        for employee in self.employees:
            # Get the last row (for appending):
            row = self.tableWidget_ListEmp.rowCount()
            # Insert a new row (at the last row):
            self.tableWidget_ListEmp.insertRow(row)

            item_id = QTableWidgetItem(str(employee.ID))
            self.tableWidget_ListEmp.setItem(row, 0, item_id)

            if employee.IsDeleted == 1:
                item_id.setBackground(Qt.GlobalColor.red)

            item_code = QTableWidgetItem(str(employee.EmployeeCode))
            self.tableWidget_ListEmp.setItem(row, 1, item_code)

            item_name = QTableWidgetItem(str(employee.Name))
            self.tableWidget_ListEmp.setItem(row, 2, item_name)

            item_phone = QTableWidgetItem(str(employee.Phone))
            self.tableWidget_ListEmp.setItem(row, 3, item_phone)

            item_email = QTableWidgetItem(str(employee.Email))
            self.tableWidget_ListEmp.setItem(row, 4, item_email)

    def setupSignalAndSlot(self):
        self.pushButton_New.clicked.connect(self.clearAll)
        self.tableWidget_ListEmp.itemSelectionChanged.connect(self.showDetailEmployee)
        self.pushButton_Save.clicked.connect(self.save_employee)
        self.pushButton_Update.clicked.connect(self.update_employee)
        self.pushButton_Delete.clicked.connect(self.delete_employee)

    def clearAll(self):
        self.lineEdit_EmpID.clear()
        self.lineEdit_EmpName.clear()
        self.lineEdit_EmpPhone.clear()
        self.lineEdit_Email.clear()
        self.lineEdit_EmpCode.clear()
        self.lineEdit_EmpPassword.clear()
        self.checkBox_IsDeleted.setChecked(False)
        self.lineEdit_EmpCode.setFocus()

    def showDetailEmployee(self):
        if self.tableWidget_ListEmp.currentRow() < 0:
            return

        row_index = self.tableWidget_ListEmp.currentRow()
        id = self.tableWidget_ListEmp.item(row_index, 0).text()
        emp = self.empc.getDetailEmployee(id)
        if emp:
            self.lineEdit_EmpID.setText(str(emp.ID))
            self.lineEdit_EmpCode.setText(str(emp.EmployeeCode))
            self.lineEdit_EmpName.setText(str(emp.Name))
            self.lineEdit_EmpPhone.setText(str(emp.Phone))
            self.lineEdit_Email.setText(str(emp.Email))
            self.lineEdit_EmpPassword.setText(str(emp.Password))
            self.checkBox_IsDeleted.setChecked(emp.IsDeleted == 1)

    def save_employee(self):
        # Validate required fields
        if not self.validate_inputs():
            return

        code = self.lineEdit_EmpCode.text()
        name = self.lineEdit_EmpName.text()
        phone = self.lineEdit_EmpPhone.text()
        email = self.lineEdit_Email.text()
        password = self.lineEdit_EmpPassword.text()
        is_deleted = 1 if self.checkBox_IsDeleted.isChecked() else 0

        emp = Employee(None, code, name, phone, email, password, is_deleted)
        result = self.empc.insertOneEmployee(emp)

        if result > 0:
            self.displayEmployeeIntoTable()
            self.clearAll()
            QMessageBox.information(self.MainWindow, "Success", "Employee saved successfully!")
        else:
            QMessageBox.warning(self.MainWindow, "Insert Failed", "Failed to insert new employee")

    def update_employee(self):
        if not self.lineEdit_EmpID.text():
            QMessageBox.warning(self.MainWindow, "Warning", "Please select an employee to update!")
            return

        if not self.validate_inputs():
            return

        emp_id = self.lineEdit_EmpID.text()
        code = self.lineEdit_EmpCode.text()
        name = self.lineEdit_EmpName.text()
        phone = self.lineEdit_EmpPhone.text()
        email = self.lineEdit_Email.text()
        password = self.lineEdit_EmpPassword.text()
        is_deleted = 1 if self.checkBox_IsDeleted.isChecked() else 0

        # Tạo employee object và gọi phương thức từ connector
        emp = Employee(emp_id, code, name, phone, email, password, is_deleted)

        try:
            result = self.empc.updateOneEmployee(emp)
            if result > 0:
                self.displayEmployeeIntoTable()
                self.clearAll()
                QMessageBox.information(self.MainWindow, "Success", "Employee updated successfully!")
            else:
                QMessageBox.warning(self.MainWindow, "Update Failed", "Failed to update employee")
        except Exception as e:
            QMessageBox.critical(self.MainWindow, "Error", f"Error updating employee: {str(e)}")

    def delete_employee(self):
        if not self.lineEdit_EmpID.text():
            QMessageBox.warning(self.MainWindow, "Warning", "Please select an employee to delete!")
            return

        reply = QMessageBox.question(self.MainWindow, "Confirm Delete",
                                     "Are you sure you want to delete this employee?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            emp_id = self.lineEdit_EmpID.text()

            try:
                result = self.empc.deleteOneEmployee(emp_id)
                if result > 0:
                    self.displayEmployeeIntoTable()
                    self.clearAll()
                    QMessageBox.information(self.MainWindow, "Success", "Employee deleted successfully!")
                else:
                    QMessageBox.warning(self.MainWindow, "Delete Failed", "Failed to delete employee")
            except Exception as e:
                QMessageBox.critical(self.MainWindow, "Error", f"Error deleting employee: {str(e)}")

    def validate_inputs(self):
        """Validate required inputs"""
        if not self.lineEdit_EmpCode.text().strip():
            QMessageBox.warning(self.MainWindow, "Validation Error", "Employee Code is required!")
            self.lineEdit_EmpCode.setFocus()
            return False

        if not self.lineEdit_EmpName.text().strip():
            QMessageBox.warning(self.MainWindow, "Validation Error", "Employee Name is required!")
            self.lineEdit_EmpName.setFocus()
            return False

        if not self.lineEdit_Email.text().strip():
            QMessageBox.warning(self.MainWindow, "Validation Error", "Email is required!")
            self.lineEdit_Email.setFocus()
            return False

        # Validate email format
        email = self.lineEdit_Email.text().strip()
        if not self.is_valid_email(email):
            QMessageBox.warning(self.MainWindow, "Validation Error", "Please enter a valid email address!")
            self.lineEdit_Email.setFocus()
            return False

        return True

    def is_valid_email(self, email):
        """Simple email validation"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None