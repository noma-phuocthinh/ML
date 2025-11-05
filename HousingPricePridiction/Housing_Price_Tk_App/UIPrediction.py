from tkinter import *
from tkinter import messagebox, ttk
from tkinter.font import Font
from tkinter import filedialog as fd
from DataSetViewer import DataSetViewer
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import metrics
from FileUtil import FileUtil
import os
import datetime
import glob


class UIPrediction:
    def __init__(self):
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

    def create_ui(self):
        self.root = Tk()
        self.root.title("House Pricing Prediction - Faculty of Information Systems")
        self.root.geometry("1280x800")

        main_panel = PanedWindow(self.root)
        main_panel["bg"] = "yellow"
        main_panel.pack(fill=BOTH, expand=True)

        # Top Panel
        top_panel = PanedWindow(main_panel, height=80)
        top_panel["bg"] = "lightblue"
        main_panel.add(top_panel)
        top_panel.pack(fill=X, side=TOP, expand=False)

        font = Font(family="tahoma", size=18, weight="bold")
        title_label = Label(top_panel, text='House Pricing Prediction', font=font)
        title_label["bg"] = "lightblue"
        title_label.pack(pady=20)

        # Center Panel
        center_panel = PanedWindow(main_panel)
        main_panel.add(center_panel)
        center_panel["bg"] = "lightgray"
        center_panel.pack(fill=BOTH, expand=True)

        # Choose Dataset Panel
        choose_dataset_panel = PanedWindow(center_panel, height=50)
        center_panel.add(choose_dataset_panel)
        choose_dataset_panel["bg"] = "orange"
        choose_dataset_panel.pack(fill=X, pady=5)

        dataset_label = Label(choose_dataset_panel, text="Select Dataset:")
        dataset_label.pack(side=LEFT, padx=5)

        self.selectedFileName = StringVar()
        self.selectedFileName.set("../Data/USA_Housing.csv")
        self.choose_dateset_entry = Entry(choose_dataset_panel, textvariable=self.selectedFileName, width=50)
        self.choose_dateset_entry.pack(side=LEFT, padx=5)

        self.choose_dataset_button = Button(choose_dataset_panel, text="1. Pick Dataset",
                                            width=15, command=self.do_pick_data)
        self.choose_dataset_button.pack(side=LEFT, padx=5)

        self.view_dataset_button = Button(choose_dataset_panel, text="2. View Dataset",
                                          width=15, command=self.do_view_dataset)
        self.view_dataset_button.pack(side=LEFT, padx=5)

        # Training Rate Panel
        training_rate_panel = PanedWindow(center_panel, height=50)
        center_panel.add(training_rate_panel)
        training_rate_panel.pack(fill=X, pady=5)

        training_rate_label = Label(training_rate_panel, text="Training Rate:")
        training_rate_label.pack(side=LEFT, padx=5)

        self.training_rate = IntVar()
        self.training_rate.set(80)
        self.training_rate_entry = Entry(training_rate_panel, textvariable=self.training_rate, width=10)
        self.training_rate_entry.pack(side=LEFT, padx=5)

        percent_label = Label(training_rate_panel, text="%")
        percent_label.pack(side=LEFT, padx=5)

        self.train_model_button = Button(training_rate_panel, text="3. Train Model",
                                         width=15, command=self.do_train)
        self.train_model_button.pack(side=LEFT, padx=5)

        self.evaluate_model_button = Button(training_rate_panel, text="4. Evaluate Model",
                                            width=15, command=self.do_evaluation)
        self.evaluate_model_button.pack(side=LEFT, padx=5)

        self.status = StringVar()
        self.status.set("Ready")
        self.train_model_result_label = Label(training_rate_panel, textvariable=self.status)
        self.train_model_result_label.pack(side=LEFT, padx=20)

        # Evaluate Panel
        evaluate_panel = PanedWindow(center_panel, height=400)
        evaluate_panel["bg"] = "lightcyan"
        center_panel.add(evaluate_panel)
        evaluate_panel.pack(fill=BOTH, expand=True, pady=5)

        # Table Evaluate Panel
        table_evaluate_panel = PanedWindow(evaluate_panel, height=400)
        evaluate_panel.add(table_evaluate_panel)
        table_evaluate_panel.pack(side=LEFT, fill=BOTH, expand=True)

        # Define columns for evaluation table
        columns = ('Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms',
                   'Avg. Area Number of Bedrooms', 'Area Population', 'Original Price', 'Prediction Price')

        self.tree = ttk.Treeview(table_evaluate_panel, columns=columns, show="headings", height=15)

        # Define headings
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor=CENTER)

        self.tree.pack(side=LEFT, fill=BOTH, expand=True)
        scrollbar = ttk.Scrollbar(table_evaluate_panel, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

        # Coefficient Panel
        coefficient_panel = PanedWindow(evaluate_panel, width=400)
        evaluate_panel.add(coefficient_panel)
        coefficient_panel.pack(side=RIGHT, fill=Y, expand=False)

        coefficient_detail_label = Label(coefficient_panel, text="Coefficient:", font=("Arial", 12, "bold"))
        coefficient_detail_label.pack(side=TOP, fill=X, pady=5)

        coefficient_detail_panel = PanedWindow(coefficient_panel)
        coefficient_panel.add(coefficient_detail_panel)
        coefficient_detail_panel.pack(side=TOP, fill=BOTH, expand=True)

        self.coefficient_detail_text = Text(coefficient_detail_panel, height=10, width=40)
        scroll_text = Scrollbar(coefficient_detail_panel)
        self.coefficient_detail_text.configure(yscrollcommand=scroll_text.set)
        self.coefficient_detail_text.pack(side=LEFT, fill=BOTH, expand=True)
        scroll_text.config(command=self.coefficient_detail_text.yview)
        scroll_text.pack(side=RIGHT, fill=Y)

        # Metrics Panel
        metric_panel = PanedWindow(coefficient_panel)
        coefficient_panel.add(metric_panel)
        metric_panel.pack(side=TOP, fill=X, pady=10)

        self.mae_value = DoubleVar()
        mae_label = Label(metric_panel, text="Mean Absolute Error (MAE):")
        mae_label.grid(row=0, column=0, sticky=W, padx=5, pady=2)
        mae_entry = Entry(metric_panel, width=20, textvariable=self.mae_value, state='readonly')
        mae_entry.grid(row=0, column=1, padx=5, pady=2)

        self.mse_value = DoubleVar()
        mse_label = Label(metric_panel, text="Mean Square Error (MSE):")
        mse_label.grid(row=1, column=0, sticky=W, padx=5, pady=2)
        mse_entry = Entry(metric_panel, width=20, textvariable=self.mse_value, state='readonly')
        mse_entry.grid(row=1, column=1, padx=5, pady=2)

        self.rmse_value = DoubleVar()
        rmse_label = Label(metric_panel, text="Root Mean Square Error (RMSE):")
        rmse_label.grid(row=2, column=0, sticky=W, padx=5, pady=2)
        rmse_entry = Entry(metric_panel, width=20, textvariable=self.rmse_value, state='readonly')
        rmse_entry.grid(row=2, column=1, padx=5, pady=2)

        savemodel_button = Button(metric_panel, text="5. Save Model", width=15, command=self.do_save_model)
        savemodel_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Load Model Panel - ĐÃ ĐƯỢC CẢI TIẾN
        loadmodel_panel = PanedWindow(center_panel, height=40)
        center_panel.add(loadmodel_panel)
        loadmodel_panel.pack(fill=X, pady=5)

        loadmodel_button = Button(loadmodel_panel, text="6. Load Model",
                                  width=15, command=self.do_load_model)
        loadmodel_button.pack(side=LEFT, padx=5)

        # Thêm OptionMenu để chọn model đã lưu
        self.selected_model = StringVar()
        self.update_saved_models_list()  # Cập nhật danh sách model
        if not self.saved_models:
            self.saved_models = ["No saved models"]
        self.selected_model.set(self.saved_models[0])

        self.model_option_menu = OptionMenu(loadmodel_panel, self.selected_model, *self.saved_models)
        self.model_option_menu.pack(side=LEFT, padx=5)

        # Input Prediction Panel
        input_prediction_panel = PanedWindow(center_panel)
        center_panel.add(input_prediction_panel)
        input_prediction_panel.pack(fill=X, pady=10)

        # Create input fields
        inputs = [
            ("Avg. Area Income:", "area_income_value"),
            ("Avg. Area House Age:", "area_house_age_value"),
            ("Avg. Area Number of Rooms:", "area_number_of_rooms_value"),
            ("Avg. Area Number of Bedrooms:", "area_number_of_bedrooms_value"),
            ("Area Population:", "area_population_value")
        ]

        for i, (label_text, var_name) in enumerate(inputs):
            label = Label(input_prediction_panel, text=label_text)
            label.grid(row=i, column=0, sticky=W, padx=10, pady=5)
            var = DoubleVar()
            setattr(self, var_name, var)
            entry = Entry(input_prediction_panel, textvariable=var, width=30)
            entry.grid(row=i, column=1, padx=10, pady=5)

        prediction_button = Button(input_prediction_panel, text="7. Prediction House Pricing",
                                   command=self.do_prediction)
        prediction_button.grid(row=5, column=0, columnspan=2, pady=10)

        prediction_price_label = Label(input_prediction_panel, text="Prediction Price:",
                                       font=("Arial", 12, "bold"))
        prediction_price_label.grid(row=6, column=0, sticky=W, padx=10, pady=5)

        self.prediction_price_value = DoubleVar()
        prediction_price_entry = Entry(input_prediction_panel, textvariable=self.prediction_price_value,
                                       width=30, font=("Arial", 12, "bold"), state='readonly')
        prediction_price_entry.grid(row=6, column=1, padx=10, pady=5)

        # Bottom Panel
        designedby_panel = PanedWindow(main_panel, height=30)
        designedby_panel["bg"] = "lightblue"
        main_panel.add(designedby_panel)
        designedby_panel.pack(fill=X, side=BOTTOM)

        designedby_label = Label(designedby_panel, text="Designed by: Tran Duy Thanh")
        designedby_label["bg"] = "lightblue"
        designedby_label.pack(pady=5)

    def show_ui(self):
        self.root.mainloop()

    def update_saved_models_list(self):
        """Cập nhật danh sách các model đã lưu trong thư mục models"""
        try:
            if os.path.exists(self.models_dir):
                # Tìm tất cả file .pkl trong thư mục models
                model_files = glob.glob(os.path.join(self.models_dir, "*.pkl"))
                self.saved_models = [os.path.basename(f) for f in model_files]
            else:
                self.saved_models = []
        except Exception as e:
            print(f"Error updating models list: {e}")
            self.saved_models = []

    def do_pick_data(self):
        filetypes = (("Dataset CSV", "*.csv"),
                     ("All Files", "*.*"))

        filename = fd.askopenfilename(
            title="Choose dataset",
            initialdir="../Data",
            filetypes=filetypes)
        if filename:
            self.selectedFileName.set(filename)
            messagebox.showinfo("Info", f"Dataset selected: {filename}")

    def do_view_dataset(self):
        if not self.selectedFileName.get():
            messagebox.showerror("Error", "Please select a dataset first!")
            return

        try:
            viewer = DataSetViewer()
            viewer.create_ui()
            viewer.show_data_listview(self.selectedFileName.get())
            viewer.show_ui()
        except Exception as e:
            messagebox.showerror("Error", f"Cannot view dataset: {str(e)}")

    def do_train(self):
        if not self.selectedFileName.get():
            messagebox.showerror("Error", "Please select a dataset first!")
            return

        try:
            ratio = self.training_rate.get() / 100
            if ratio <= 0 or ratio >= 1:
                messagebox.showerror("Error", "Training rate must be between 1 and 99!")
                return

            self.df = pd.read_csv(self.selectedFileName.get())
            self.X = self.df[['Avg. Area Income', 'Avg. Area House Age', 'Avg. Area Number of Rooms',
                              'Avg. Area Number of Bedrooms', 'Area Population']]
            self.y = self.df['Price']

            self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
                self.X, self.y, test_size=1 - ratio, random_state=101)

            self.lm = LinearRegression()
            self.lm.fit(self.X_train, self.y_train)

            self.status.set("Training finished successfully!")
            messagebox.showinfo("Info", "Training is finished successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Training failed: {str(e)}")

    def do_evaluation(self):
        if self.lm is None:
            messagebox.showerror("Error", "Please train the model first!")
            return

        try:
            # Clear previous data
            for item in self.tree.get_children():
                self.tree.delete(item)
            self.coefficient_detail_text.delete(1.0, END)

            # Calculate coefficients
            intercept_text = f"Intercept: {self.lm.intercept_:.2f}\n\n"
            self.coefficient_detail_text.insert(END, intercept_text)

            self.coeff_df = pd.DataFrame(self.lm.coef_, self.X.columns, columns=['Coefficient'])
            coeff_text = self.coeff_df.to_string()
            self.coefficient_detail_text.insert(END, coeff_text)

            # Make predictions
            predictions = self.lm.predict(self.X_test)
            y_test_array = np.asarray(self.y_test)

            # Display predictions in table
            for i in range(min(50, len(self.X_test))):  # Limit to 50 rows for performance
                values = [
                    f"{self.X_test.iloc[i][0]:.2f}",
                    f"{self.X_test.iloc[i][1]:.2f}",
                    f"{self.X_test.iloc[i][2]:.2f}",
                    f"{self.X_test.iloc[i][3]:.2f}",
                    f"{self.X_test.iloc[i][4]:.2f}",
                    f"{y_test_array[i]:.2f}",
                    f"{predictions[i]:.2f}"
                ]
                self.tree.insert('', END, values=values)

            # Calculate metrics
            mae = metrics.mean_absolute_error(self.y_test, predictions)
            mse = metrics.mean_squared_error(self.y_test, predictions)
            rmse = np.sqrt(mse)

            self.mae_value.set(mae)
            self.mse_value.set(mse)
            self.rmse_value.set(rmse)

            self.status.set("Evaluation finished successfully!")
            messagebox.showinfo("Info", "Evaluation is finished successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Evaluation failed: {str(e)}")

    def do_save_model(self):
        if self.lm is None:
            messagebox.showerror("Error", "No model to save! Please train the model first.")
            return

        try:
            # Xác nhận lưu model
            confirm = messagebox.askyesno("Confirm Save", "Are you sure you want to save the model?")
            if not confirm:
                return

            # Tạo tên file với ngày giờ hiện tại
            current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            model_filename = f"housing_model_{current_time}.pkl"
            model_path = os.path.join(self.models_dir, model_filename)

            # Đảm bảo thư mục tồn tại
            os.makedirs(self.models_dir, exist_ok=True)

            # Lưu model
            success = FileUtil.savemodel(self.lm, model_path)
            if success:
                messagebox.showinfo("Info", f"Model saved successfully as {model_filename}!")
                # Cập nhật danh sách model
                self.update_saved_models_list()
                # Cập nhật OptionMenu
                self.update_model_option_menu()
            else:
                messagebox.showerror("Error", "Failed to save model!")
        except Exception as e:
            messagebox.showerror("Error", f"Save failed: {str(e)}")

    def update_model_option_menu(self):
        """Cập nhật OptionMenu với danh sách model mới"""
        self.update_saved_models_list()

        # Xóa menu cũ
        self.model_option_menu['menu'].delete(0, 'end')

        # Thêm các lựa chọn mới
        if not self.saved_models:
            self.saved_models = ["No saved models"]

        for model in self.saved_models:
            self.model_option_menu['menu'].add_command(
                label=model,
                command=lambda value=model: self.selected_model.set(value)
            )

        self.selected_model.set(self.saved_models[0])

    def do_load_model(self):
        try:
            selected_model_name = self.selected_model.get()
            if selected_model_name == "No saved models":
                messagebox.showerror("Error", "No saved models available!")
                return

            model_path = os.path.join(self.models_dir, selected_model_name)

            if not os.path.exists(model_path):
                messagebox.showerror("Error", f"Model file {selected_model_name} not found!")
                return

            self.lm = FileUtil.loadmodel(model_path)
            if self.lm is not None:
                messagebox.showinfo("Info", f"Model {selected_model_name} loaded successfully!")
                self.status.set(f"Model {selected_model_name} loaded successfully!")
            else:
                messagebox.showerror("Error", "Failed to load model!")
        except Exception as e:
            messagebox.showerror("Error", f"Load failed: {str(e)}")

    def do_prediction(self):
        if self.lm is None:
            messagebox.showerror("Error", "No model available! Please train or load a model first.")
            return

        try:
            # Validate inputs
            required_fields = [
                self.area_income_value.get(),
                self.area_house_age_value.get(),
                self.area_number_of_rooms_value.get(),
                self.area_number_of_bedrooms_value.get(),
                self.area_population_value.get()
            ]

            if any(str(field) == '0.0' or str(field) == '' for field in required_fields):
                messagebox.showerror("Error", "Please fill in all fields!")
                return

            result = self.lm.predict([[
                self.area_income_value.get(),
                self.area_house_age_value.get(),
                self.area_number_of_rooms_value.get(),
                self.area_number_of_bedrooms_value.get(),
                self.area_population_value.get()
            ]])
            self.prediction_price_value.set(f"{result[0]:.2f}")

        except Exception as e:
            messagebox.showerror("Error", f"Prediction failed: {str(e)}")