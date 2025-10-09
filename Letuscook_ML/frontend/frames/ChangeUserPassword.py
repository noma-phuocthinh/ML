import tkinter as tk
from pathlib import Path
from tkinter import Canvas, Entry, Text, Button, PhotoImage

from frontend.resources.Effect import auto_update_date


class ChangeUserPasswordFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.OUTPUT_PATH = Path(__file__).parent.parent
        # Thiết lập đường dẫn assets
        self.ASSETS_PATH = self.OUTPUT_PATH / "assets" / "ChangeUserPassword"
        self.setup_ui()
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
        self.canvas.place(x = 0, y = 0)

        # Background
        self.background_image = PhotoImage(file=self.relative_to_assets("background.png"))
        self.cup_img_background = self.canvas.create_image(690.0, 490.0, image=self.background_image)

        # Date text
        self.cup_text_date = self.canvas.create_text(
            506.0,
            45.0,
            anchor="nw",
            text="",
            fill="#FFFFFF",
            justify="center",
            font=("Young Serif Regular", 25)
        )

        # Gọi update_date lần đầu
        auto_update_date(self.canvas, self.cup_text_date)

        # Username Entry
        self.cup_entry_image = PhotoImage(file=self.relative_to_assets("entry_background.png"))
        self.cup_username_bg = self.canvas.create_image(816.0, 249.5, image=self.cup_entry_image)
        self.cup_entry_username = Entry(
            self.canvas,
            bd=0,
            bg="#FAFDE0",
            fg="#000716",
            font=("Young Serif", 16),
            highlightthickness=0
        )
        self.cup_entry_username.place(x=679.0, y=230.0, width=274.0, height=37.0)

        # Current Password Entry
        self.cup_phone_bg = self.canvas.create_image(816.0, 310.5, image=self.cup_entry_image)
        self.cup_entry_phone = Entry(
            self.canvas,
            bd=0,
            bg="#FAFDE0",
            fg="#000716",
            font=("Young Serif", 16),
            show="*",
            highlightthickness=0
        )
        self.cup_entry_phone.place(x=679.0, y=291.0, width=274.0, height=37.0)

        # New Password Entry
        self.cup_email_bg = self.canvas.create_image(816.0, 370.5, image=self.cup_entry_image)
        self.cup_entry_email = Entry(
            self.canvas,
            bd=0,
            bg="#FAFDE0",
            fg="#000716",
            font=("Young Serif", 16),
            show="*",
            highlightthickness=0
        )
        self.cup_entry_email.place(x=679.0, y=351.0, width=274.0, height=37.0)

        # Confirm Password Entry
        self.cup_bio_bg = self.canvas.create_image(816.0, 430.5, image=self.cup_entry_image)
        self.cup_entry_bio = Entry(
            self.canvas,
            bd=0,
            bg="#FAFDE0",
            fg="#000716",
            font=("Young Serif", 16),
            show="*",
            highlightthickness=0
        )
        self.cup_entry_bio.place(x=679.0, y=411.0, width=274.0, height=37.0)

        # Email Entry
        self.cup_bio_bg = self.canvas.create_image(816.0, 490.5, image=self.cup_entry_image)
        self.cup_entry_bio = Entry(
            self.canvas,
            bd=0,
            bg="#FAFDE0",
            fg="#000716",
            font=("Young Serif", 16),
            highlightthickness=0
        )
        self.cup_entry_bio.place(x=679.0, y=471.0, width=274.0, height=37.0)

        # Back Button
        self.cup_back_image = PhotoImage(file=self.relative_to_assets("btn_back.png"))
        self.cup_btn_back = Button(
            self.canvas,
            image=self.cup_back_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("SettingFrame"),
            relief="flat"
        )
        self.cup_btn_back.place(x=41.0, y=32.0, width=36.0, height=37.0)

        # Log out Button
        self.cup_logout_image = PhotoImage(file=self.relative_to_assets("btn_logout.png"))
        self.cup_btn_logout = Button(
            self.canvas,
            image=self.cup_logout_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("LogInFrame"),
            relief="flat"
        )
        self.cup_btn_logout.place(x=1122.0, y=60.0, width=193.0, height=50.0)

        # Eye hide Button
        self.cup_eyehide_image = PhotoImage(file=self.relative_to_assets("btn_eyehide.png"))
        self.cup_btn_eyehide1 = Button(
            self.canvas,
            image=self.cup_eyehide_image,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.cup_btn_eyehide1.place(x=933.0, y=300.0, width=22.0, height=20.0)

        self.cup_btn_eyehide2 = Button(
            self.canvas,
            image=self.cup_eyehide_image,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.cup_btn_eyehide2.place(x=933.0, y=361.0, width=22.0, height=20.0)

        self.cup_btn_eyehide3 = Button(
            self.canvas,
            image=self.cup_eyehide_image,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.cup_btn_eyehide3.place(x=933.0, y=421.0, width=22.0, height=20.0)

        # Save Button
        self.cup_save_image = PhotoImage(file=self.relative_to_assets("btn_save.png"))
        self.cup_btn_save = Button(
            self.canvas,
            image=self.cup_save_image,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.cup_btn_save.place(x=447.0, y=565.0, width=486.0, height=49.0)

        # Homepage Button
        self.cup_homepage_image = PhotoImage(file=self.relative_to_assets("btn_homepage.png"))
        self.cup_btn_homepage = Button(
            self.canvas,
            image=self.cup_homepage_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("HomepageFrame"),
            relief="flat"
        )
        self.cup_btn_homepage.place(x=125.0, y=803.0, width=225.0, height=65.0)

        # Write Journal Button
        self.cup_writejournal_image = PhotoImage(file=self.relative_to_assets("btn_writejournal.png"))
        self.cup_btn_writejournal = Button(
            self.canvas,
            image=self.cup_writejournal_image,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.cup_btn_writejournal.place(x=388.0, y=803.0, width=225.0, height=65.0)

        # Recommend Button
        self.cup_recommend_image = PhotoImage(file=self.relative_to_assets("btn_recommend.png"))
        self.cup_btn_recommend = Button(
            self.canvas,
            image=self.cup_recommend_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("ObesityRiskPredictionFrame"),
            relief="flat"
        )
        self.cup_btn_recommend.place(x=768.0, y=803.0, width=225.0, height=65.0)

        # Setting Button
        self.cup_setting_image = PhotoImage(file=self.relative_to_assets("btn_setting.png"))
        self.cup_btn_setting = Button(
            self.canvas,
            image=self.cup_setting_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("SettingFrame"),
            relief="flat"
        )
        self.cup_btn_setting.place(x=1031.0, y=803.0, width=225.0, height=65.0)




