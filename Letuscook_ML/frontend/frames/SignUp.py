# frontend/frames/SignUp.py
import os, sys
import tkinter as tk
from pathlib import Path
from tkinter import Canvas, Entry, Button, PhotoImage, filedialog, messagebox
import pymysql

from backend.controllers.SignUpEx import SignUpBackendEx

# === Thêm project root TRƯỚC khi import backend ===
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# === Import backend ===
# Lưu ý: đảm bảo file ở backend/signup_backend_pymysql.py (hoặc đổi import cho đúng vị trí bạn đặt)
from backend.controllers.function import DuplicateFieldError, SignupValidationError

class SignUpFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.OUTPUT_PATH = Path(__file__).parent.parent
        # Thiết lập đường dẫn assets
        self.ASSETS_PATH = self.OUTPUT_PATH / "assets" / "SignUp"

        # --- backend ---
        self.backend = SignUpBackendEx()
        self.photo_path = None

        self.setup_ui()
        self.setup_events()

    def relative_to_assets(self, path: str) -> Path:
        return self.ASSETS_PATH / Path(path)

    def setup_ui(self):
        self.canvas = Canvas(
            self,
            bg="#FFFFFF",
            height=980,
            width=1380,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        # Background
        self.background_image = PhotoImage(file=self.relative_to_assets("background.png"))
        self.dk_img_background = self.canvas.create_image(690.0, 490.0, image=self.background_image)

        # Fullname Entry
        self.dk_fullname_image = PhotoImage(file=self.relative_to_assets("entry_fullname.png"))
        self.dk_fullname_bg = self.canvas.create_image(1050.5, 213.5, image=self.dk_fullname_image)
        self.dk_entry_fullname = Entry(
            self.canvas,
            bd=0,
            bg="#FAFDE0",
            fg="#000716",
            font=("Young Serif", 16),
            highlightthickness=0
        )
        self.dk_entry_fullname.place(x=880.0, y=194.0, width=341.0, height=37.0)

        # Email Entry
        self.dk_email_image = PhotoImage(file=self.relative_to_assets("entry_email.png"))
        self.dk_email_bg = self.canvas.create_image(1050.5, 274.0, image=self.dk_email_image)
        self.dk_entry_email = Entry(
            self.canvas,
            bd=0,
            bg="#FAFDE0",
            fg="#000716",
            font=("Young Serif", 16),
            highlightthickness=0
        )
        self.dk_entry_email.place(x=880.0, y=255.0, width=341.0, height=36.0)

        # Username Entry
        self.dk_username_image = PhotoImage(file=self.relative_to_assets("entry_username.png"))
        self.dk_username_bg = self.canvas.create_image(1050.5, 334.5, image=self.dk_username_image)
        self.dk_entry_username = Entry(
            self.canvas,
            bd=0,
            bg="#FAFDE0",
            fg="#000716",
            font=("Young Serif", 16),
            highlightthickness=0
        )
        self.dk_entry_username.place(x=880.0, y=315.0, width=341.0, height=37.0)

        # Password Entry (ẩn)
        self.dk_password_image = PhotoImage(file=self.relative_to_assets("entry_password.png"))
        self.dk_password_bg = self.canvas.create_image(1050.5, 394.5, image=self.dk_password_image)
        self.dk_entry_password = Entry(
            self.canvas,
            bd=0,
            bg="#FAFDE0",
            fg="#000716",
            font=("Young Serif", 16),
            highlightthickness=0,
            show="*"
        )
        self.dk_entry_password.place(x=880.0, y=375.0, width=341.0, height=37.0)

        # Confirm password Entry (ẩn)
        self.dk_cfpassword_image = PhotoImage(file=self.relative_to_assets("entry_cfpassword.png"))
        self.dk_cfpassword_bg = self.canvas.create_image(1050.5, 454.5, image=self.dk_cfpassword_image)
        self.dk_entry_cfpassword = Entry(
            self.canvas,
            bd=0,
            bg="#FAFDE0",
            fg="#000716",
            font=("Young Serif", 16),
            highlightthickness=0,
            show="*"
        )
        self.dk_entry_cfpassword.place(x=880.0, y=435.0, width=341.0, height=37.0)

        # Phone number Entry
        self.dk_phonenumber_image = PhotoImage(file=self.relative_to_assets("entry_phonenumber.png"))
        self.dk_phonenumber_bg = self.canvas.create_image(1051.0, 515.0, image=self.dk_phonenumber_image)
        self.dk_entry_phonenumber = Entry(
            self.canvas,
            bd=0,
            bg="#FAFDE0",
            fg="#000716",
            font=("Young Serif", 16),
            highlightthickness=0
        )
        self.dk_entry_phonenumber.place(x=881.0, y=496.0, width=340.0, height=36.0)

        # Bio Entry
        self.dk_bio_image = PhotoImage(file=self.relative_to_assets("entry_bio.png"))
        self.dk_bio_bg = self.canvas.create_image(1051.0, 575.5, image=self.dk_bio_image)
        self.dk_entry_bio = Entry(
            self.canvas,
            bd=0,
            bg="#FAFDE0",
            fg="#000716",
            font=("Young Serif", 16),
            highlightthickness=0
        )
        self.dk_entry_bio.place(x=881.0, y=556.0, width=340.0, height=37.0)

        # Eye hide Button
        self.dk_eyehide_image = PhotoImage(file=self.relative_to_assets("btn_eyehide.png"))
        self.dk_btn_eyehide1 = Button(
            self.canvas,
            image=self.dk_eyehide_image,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.dk_btn_eyehide1.place(x=1197.0, y=384.0, width=24.0, height=22.0)

        self.dk_btn_eyehide2 = Button(
            self.canvas,
            image=self.dk_eyehide_image,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.dk_btn_eyehide2.place(x=1197.0, y=444.0, width=24.0, height=22.0)

        # Upload Photo Button
        self.dk_uploadphoto_image = PhotoImage(file=self.relative_to_assets("btn_uploadphoto.png"))
        self.dk_btn_uploadphoto = Button(
            self.canvas,
            image=self.dk_uploadphoto_image,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.dk_btn_uploadphoto.place(x=858.0, y=613.0, width=385.0, height=45.0)

        # Sign Up Button
        self.dk_signup_image = PhotoImage(file=self.relative_to_assets("btn_signup.png"))
        self.dk_btn_signup = Button(
            self.canvas,
            image=self.dk_signup_image,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.dk_btn_signup.place(x=680.0, y=711.0, width=487.0, height=48.0)

        # Already Account Button
        self.dk_alreadyaccount_image = PhotoImage(file=self.relative_to_assets("btn_alreadyaccount.png"))
        self.dk_btn_alreadyaccount = Button(
            self.canvas,
            image=self.dk_alreadyaccount_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("LogInFrame"),
            relief="flat"
        )
        self.dk_btn_alreadyaccount.place(x=812.0, y=775.0, width=222.0, height=24.0)

    def setup_events(self):
        self.photo_path = None
        self.dk_btn_uploadphoto.configure(command=self.on_upload_photo)
        self.dk_btn_signup.configure(command=self.on_signup)

    # ====== Handlers ======
    def on_upload_photo(self):
        path = filedialog.askopenfilename(
            title="Chọn ảnh đại diện",
            filetypes=[("Images", "*.png *.jpg *.jpeg *.webp"), ("All files", "*.*")]
        )
        if path:
            self.photo_path = path
            messagebox.showinfo("Ảnh", f"Đã chọn: {os.path.basename(path)}")

    def on_signup(self):
        full_name = self.dk_entry_fullname.get().strip()
        email = self.dk_entry_email.get().strip()
        username = self.dk_entry_username.get().strip()
        password = self.dk_entry_password.get()
        confirm_password = self.dk_entry_cfpassword.get()
        phone_number = self.dk_entry_phonenumber.get().strip()
        bio = self.dk_entry_bio.get().strip()

        try:
            ok, user_id = self.backend.register(
                full_name=full_name,
                email=email,
                username=username,
                password=password,
                confirm_password=confirm_password,
                phone_number=phone_number,
                bio=bio,
                photo_path=self.photo_path
            )
            if ok:
                self.controller.show_frame("LogInFrame")
        except SignupValidationError as e:
            messagebox.showerror("Đăng ký thất bại", str(e))
        except pymysql.MySQLError as e:
            messagebox.showerror("Lỗi cơ sở dữ liệu", str(e))


