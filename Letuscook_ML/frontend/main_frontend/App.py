import tkinter as tk

from frontend.frames.ChangeUserInformation import ChangeUserInformationFrame
from frontend.frames.ChangeUserPassword import ChangeUserPasswordFrame
from frontend.frames.Homepage import HomepageFrame
from frontend.frames.LogIn import LogInFrame
from frontend.frames.PickingPackRecommend import PickingPackRecommendFrame
from frontend.frames.Setting import SettingFrame
from frontend.frames.ShowPredict import ShowPredictFrame
from frontend.frames.SignUp import SignUpFrame


class AppController:
    def __init__(self, window):
        self.window = window
        self.frames = {}
        self.current_frame = None

    def register_frame(self, name, frame):
        self.frames[name] = frame

    def show_frame(self, name):
        # Ẩn frame hiện tại
        if self.current_frame:
            self.current_frame.grid_remove()

        # Hiển thị frame mới
        frame = self.frames.get(name)
        if frame:
            frame.grid(row=0, column=0, sticky="nsew")
            self.current_frame = frame
            self.window.update_idletasks()  # Cập nhật giao diện


class Main(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.controller = AppController(self)

        # Cấu hình cửa sổ chính
        self.geometry("1380x980")
        self.title("Application")
        self.resizable(False, False)

        # Định vị cửa sổ giữa màn hình
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - 1380) // 2
        y = (screen_height - 980) // 2
        self.geometry(f"1380x980+{x}+{y}")

        # Tạo container chứa tất cả các frame
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Khởi tạo và lưu trữ tất cả các frame
        for F in (LogInFrame, SignUpFrame, HomepageFrame, ShowPredictFrame, PickingPackRecommendFrame, SettingFrame, ChangeUserInformationFrame, ChangeUserPasswordFrame):
            frame_name = F.__name__
            frame = F(parent=container, controller=self.controller)
            self.controller.register_frame(frame_name, frame)
            # TẤT CẢ CÁC FRAME ĐỀU ĐƯỢC TẠO NHƯNG ẨN ĐI
            frame.grid(row=0, column=0, sticky="nsew")
            frame.grid_remove()  # Ẩn frame ngay sau khi tạo

        # Hiển thị LogInFrame làm trang đầu tiên
        self.controller.show_frame("LogInFrame")


if __name__ == "__main__":
    app = Main()
    app.mainloop()