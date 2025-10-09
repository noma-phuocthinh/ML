# frontend/frames/LogIn.py
import os, sys
import tkinter as tk
from pathlib import Path
from tkinter import Canvas, Entry, Button, PhotoImage, messagebox
import pymysql

# sys.path trước khi import backend
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from backend.controllers.LogInEx import LogInEx
from backend.controllers.function import LoginValidationError, UnregisteredAccountError, WrongPasswordError

class LogInFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.OUTPUT_PATH = Path(__file__).parent.parent
        self.ASSETS_PATH = self.OUTPUT_PATH / "assets" / "LogIn"

        # backend
        self.login_backend = LogInEx()

        self.setup_ui()

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def setup_ui(self):
        # 1) TẠO CANVAS TRƯỚC
        self.canvas = Canvas(
            self, bg="#FFFFFF", height=980, width=1380,
            bd=0, highlightthickness=0, relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # 2) RỒI MỚI TẠO CÁC ẢNH/NÚT/ENTRY ĐẶT TRÊN CANVAS
        self.background_image = PhotoImage(file=self.relative_to_assets("background.png"))
        self.dn_img_background = self.canvas.create_image(690.0, 490.0, image=self.background_image)

        # Username
        self.dn_username_image = PhotoImage(file=self.relative_to_assets("entry_username.png"))
        self.dn_username_bg = self.canvas.create_image(1031.0, 344.5, image=self.dn_username_image)
        self.dn_username = Entry(
            self.canvas, bd=0, bg="#FAFDE0", fg="#000716",
            font=("Young Serif", 16), highlightthickness=0
        )
        self.dn_username.place(x=893.0, y=325.0, width=276.0, height=37.0)

        # Password
        self.dn_password_image = PhotoImage(file=self.relative_to_assets("entry_password.png"))
        self.dn_password_bg = self.canvas.create_image(1031.0, 404.5, image=self.dn_password_image)
        self.dn_password = Entry(
            self.canvas, bd=0, bg="#FAFDE0", fg="#000716",
            font=("Young Serif", 16), highlightthickness=0, show="*"
        )
        self.dn_password.place(x=893.0, y=385.0, width=276.0, height=37.0)

        # Eye hide Button
        self.dn_eyehide_image = PhotoImage(file=self.relative_to_assets("btn_eyehide.png"))
        self.dn_btn_eyehide = Button(
            self.canvas,
            image=self.dn_eyehide_image,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.dn_btn_eyehide.place(x=1150.0, y=395.0, width=22.0, height=20.0)

        # LogIn button (đặt SAU khi đã có self.canvas)
        self.dn_login_image = PhotoImage(file=self.relative_to_assets("btn_login.png"))
        self.dn_btn_login = Button(
            self.canvas, image=self.dn_login_image, borderwidth=0,
            highlightthickness=0, command=self.on_login_click, relief="flat"
        )
        self.dn_btn_login.place(x=710.0, y=453.0, width=486.0, height=48.0)

        # Forgot password Button
        self.dn_forgotpassword_image = PhotoImage(file=self.relative_to_assets("btn_forgotpassword.png"))
        self.dn_btn_forgotpassword = Button(
            self.canvas, image=self.dn_forgotpassword_image,
            borderwidth=0, highlightthickness=0, relief="flat"
        )
        self.dn_btn_forgotpassword.place(x=878.0, y=549.0, width=149.0, height=18.0)

        # SignUp Button
        self.dn_signup_image = PhotoImage(file=self.relative_to_assets("btn_signup.png"))
        self.dn_btn_signup = Button(
            self.canvas, image=self.dn_signup_image, borderwidth=0,
            highlightthickness=0, command=lambda: self.controller.show_frame("SignUpFrame"),
            relief="flat"
        )
        self.dn_btn_signup.place(x=809.0, y=582.0, width=289.0, height=49.0)

    def on_login_click(self):
        identifier = self.dn_username.get().strip()
        password   = self.dn_password.get()
        try:
            user = self.login_backend.login(identifier, password)
            self.controller.current_user = user
            self.controller.show_frame("HomepageFrame")
        except LoginValidationError as e:
            messagebox.showerror("Thiếu thông tin", str(e))
        except UnregisteredAccountError as e:
            messagebox.showerror("Chưa đăng ký", str(e))
        except WrongPasswordError as e:
            messagebox.showerror("Đăng nhập thất bại", str(e))
        except pymysql.MySQLError as e:
            messagebox.showerror("Lỗi CSDL", str(e))
        except Exception as e:
            messagebox.showerror("Lỗi hệ thống", str(e))
