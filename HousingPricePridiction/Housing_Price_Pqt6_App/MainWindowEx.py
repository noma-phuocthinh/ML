import sys
import os
import pandas as pd
import numpy as np
from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import (QMainWindow, QMessageBox, QFileDialog,
                             QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import QAbstractTableModel, Qt
import pickle
import datetime
import glob
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics

from MainWindow import Ui_MainWindow


class PandasModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self._data = data

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        return len(self._data.columns)

    def data(self, index, role=Qt.ItemDataRole.DisplayRole):
        if index.isValid() and role == Qt.ItemDataRole.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(f"{value:.2f}") if isinstance(value, (int, float)) else str(value)
        return None

    def headerData(self, section, orientation, role=Qt.ItemDataRole.DisplayRole):
        if orientation == Qt.Orientation.Horizontal and role == Qt.ItemDataRole.DisplayRole:
            return str(self._data.columns[section])
        if orientation == Qt.Orientation.Vertical and role == Qt.ItemDataRole.DisplayRole:
            return str(self._data.index[section])
        return None


class DataSetViewer(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dataset viewer - House Pricing Prediction")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QtWidgets.QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QtWidgets.QVBoxLayout(self.central_widget)

        self.table = QtWidgets.QTableView()
        layout.addWidget(self.table)

    def show_data_listview(self, fileName):
        try:
            df = pd.read_csv(fileName)
            model = PandasModel(df.iloc[:, :-1])  # Exclude Address column
            self.table.setModel(model)
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Cannot load dataset: {str(e)}")


class FileUtil:
    @staticmethod
    def savemodel(model, filename):
        try:
            with open(filename, 'wb') as file:
                pickle.dump(model, file)
            return True
        except Exception as e:
            print(f"An exception occurred: {e}")
            return False

    @staticmethod
    def loadmodel(filename):
        try:
            with open(filename, 'rb') as file:
                model = pickle.load(file)
            return model
        except Exception as e:
            print(f"An exception occurred: {e}")
            return None


class MainWindowEx(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Initialize variables
        self.fileName = ""
        self.lm = None
        self.df = None
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.coeff_df = None
        self.models_dir = "../models"
        self.saved_models = []

        # Update models list
        self.update_saved_models_list()
        self.update_model_option_menu()

        # Connect signals
        self.connect_signals()

        # Set initial dataset path
        self.choose_dateset_entry.setText("../Data/USA_Housing.csv")

    def connect_signals(self):
        self.choose_dataset_button.clicked.connect(self.do_pick_data)
        self.view_dataset_button.clicked.connect(self.do_view_dataset)
        self.train_model_button.clicked.connect(self.do_train)
        self.evaluate_model_button.clicked.connect(self.do_evaluation)
        self.savemodel_button.clicked.connect(self.do_save_model)
        self.loadmodel_button.clicked.connect(self.do_load_model)
        self.prediction_button.clicked.connect(self.do_prediction)

    def update_saved_models_list(self):
        """Cập nhật danh sách các model đã lưu trong thư mục models"""
        try:
            if os.path.exists(self.models_dir):
                model_files = glob.glob(os.path.join(self.models_dir, "*.pkl"))
                self.saved_models = [os.path.basename(f) for f in model_files]
            else:
                self.saved_models = []
        except Exception as e:
            print(f"Error updating models list: {e}")
            self.saved_models = []

    def update_model_option_menu(self):
        """Cập nhật ComboBox với danh sách model mới"""
        self.model_option_menu.clear()
        if not self.saved_models:
            self.model_option_menu.addItem("No saved models")
        else:
            self.model_option_menu.addItems(self.saved_models)

    def do_pick_data(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self,
            "Choose dataset",
            "../Data",
            "Dataset CSV (*.csv);;All Files (*.*)"
        )
        if filepath:
            self.choose_dateset_entry.setText(filepath)
            QMessageBox.information(self, "Info", f"Dataset selected: {filepath}")

    def do_view_dataset(self):
        filename = self.choose_dateset_entry.text()
        if not filename:
            QMessageBox.critical(self, "Error", "Please select a dataset first!")
            return

        try:
            self.viewer = DataSetViewer()
            self.viewer.show_data_listview(filename)
            self.viewer.show()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Cannot view dataset: {str(e)}")

    def do_train(self):
        filename = self.choose_dateset_entry.text()
        if not filename:
            QMessageBox.critical(self, "Error", "Please select a dataset first!")
            return

        try:
            ratio = int(self.training_rate_entry.text()) / 100
            if ratio <= 0 or ratio >= 1:
                QMessageBox.critical(self, "Error", "Training rate must be between 1 and 99!")
                return

            self.df = pd.read_csv(filename)
            self.X = self.df[['Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms',
                              'Avg. Area Number of Bedrooms', 'Area Population']]
            self.y = self.df['Price']

            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
                self.X, self.y, test_size=1 - ratio, random_state=101)

            self.lm = LinearRegression()
            self.lm.fit(self.X_train, self.y_train)

            self.train_model_result_label.setText("Training finished successfully!")
            QMessageBox.information(self, "Info", "Training is finished successfully!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Training failed: {str(e)}")

    def do_evaluation(self):
        if self.lm is None:
            QMessageBox.critical(self, "Error", "Please train the model first!")
            return

        try:
            # Clear previous data from table
            model = self.tree.model()
            if model:
                model.deleteLater()

            # Clear coefficient text
            self.coefficient_detail_text.clear()

            # Calculate coefficients
            intercept_text = f"Intercept: {self.lm.intercept_:.2f}\n\n"
            self.coefficient_detail_text.setPlainText(intercept_text)

            self.coeff_df = pd.DataFrame(self.lm.coef_, self.X.columns, columns=['Coefficient'])
            coeff_text = self.coeff_df.to_string()
            self.coefficient_detail_text.append(coeff_text)

            # Make predictions
            predictions = self.lm.predict(self.X_test)
            y_test_array = np.asarray(self.y_test)

            # Create evaluation dataframe for table
            eval_data = []
            for i in range(min(50, len(self.X_test))):
                row = {
                    'Avg. Area Income': f"{self.X_test.iloc[i][0]:.2f}",
                    'Avg. Area House Age': f"{self.X_test.iloc[i][1]:.2f}",
                    'Avg. Area Number of Rooms': f"{self.X_test.iloc[i][2]:.2f}",
                    'Avg. Area Number of Bedrooms': f"{self.X_test.iloc[i][3]:.2f}",
                    'Area Population': f"{self.X_test.iloc[i][4]:.2f}",
                    'Original Price': f"{y_test_array[i]:.2f}",
                    'Prediction Price': f"{predictions[i]:.2f}"
                }
                eval_data.append(row)

            eval_df = pd.DataFrame(eval_data)
            table_model = PandasModel(eval_df)
            self.tree.setModel(table_model)
            self.tree.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)

            # Calculate metrics
            mae = metrics.mean_absolute_error(self.y_test, predictions)
            mse = metrics.mean_squared_error(self.y_test, predictions)
            rmse = np.sqrt(mse)

            self.mae_entry.setText(f"{mae:.2f}")
            self.mse_entry.setText(f"{mse:.2f}")
            self.rmse_entry.setText(f"{rmse:.2f}")

            self.train_model_result_label.setText("Evaluation finished successfully!")
            QMessageBox.information(self, "Info", "Evaluation is finished successfully!")

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Evaluation failed: {str(e)}")

    def do_save_model(self):
        if self.lm is None:
            QMessageBox.critical(self, "Error", "No model to save! Please train the model first.")
            return

        try:
            confirm = QMessageBox.question(
                self,
                "Confirm Save",
                "Are you sure you want to save the model?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirm != QMessageBox.StandardButton.Yes:
                return

            # Create filename with current timestamp
            current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            model_filename = f"housing_model_{current_time}.pkl"
            model_path = os.path.join(self.models_dir, model_filename)

            # Ensure directory exists
            os.makedirs(self.models_dir, exist_ok=True)

            # Save model
            success = FileUtil.savemodel(self.lm, model_path)
            if success:
                QMessageBox.information(self, "Info", f"Model saved successfully as {model_filename}!")
                # Update models list
                self.update_saved_models_list()
                self.update_model_option_menu()
            else:
                QMessageBox.critical(self, "Error", "Failed to save model!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Save failed: {str(e)}")

    def do_load_model(self):
        try:
            selected_model_name = self.model_option_menu.currentText()
            if selected_model_name == "No saved models":
                QMessageBox.critical(self, "Error", "No saved models available!")
                return

            model_path = os.path.join(self.models_dir, selected_model_name)

            if not os.path.exists(model_path):
                QMessageBox.critical(self, "Error", f"Model file {selected_model_name} not found!")
                return

            self.lm = FileUtil.loadmodel(model_path)
            if self.lm is not None:
                QMessageBox.information(self, "Info", f"Model {selected_model_name} loaded successfully!")
                self.train_model_result_label.setText(f"Model {selected_model_name} loaded successfully!")
            else:
                QMessageBox.critical(self, "Error", "Failed to load model!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Load failed: {str(e)}")

    def do_prediction(self):
        if self.lm is None:
            QMessageBox.critical(self, "Error", "No model available! Please train or load a model first.")
            return

        try:
            # Get input values
            area_income = float(self.area_income_entry.text())
            area_house_age = float(self.area_house_age_entry.text())
            area_number_of_rooms = float(self.area_number_of_rooms_entry.text())
            area_number_of_bedrooms = float(self.area_number_of_bedrooms_entry.text())
            area_population = float(self.area_population_entry.text())

            # Validate inputs
            if (area_income == 0.0 or area_house_age == 0.0 or
                    area_number_of_rooms == 0.0 or area_number_of_bedrooms == 0.0 or
                    area_population == 0.0):
                QMessageBox.critical(self, "Error", "Please fill in all fields with non-zero values!")
                return

            result = self.lm.predict([[
                area_income,
                area_house_age,
                area_number_of_rooms,
                area_number_of_bedrooms,
                area_population
            ]])
            self.prediction_price_entry.setText(f"{result[0]:.2f}")

        except ValueError:
            QMessageBox.critical(self, "Error", "Please enter valid numeric values in all fields!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Prediction failed: {str(e)}")