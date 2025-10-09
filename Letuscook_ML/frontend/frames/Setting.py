import tkinter as tk
from pathlib import Path
from tkinter import Canvas, Entry, Text, Button, PhotoImage

from frontend.resources.Effect import auto_update_date


class SettingFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.OUTPUT_PATH = Path(__file__).parent.parent
        # Thiết lập đường dẫn assets
        self.ASSETS_PATH = self.OUTPUT_PATH / "assets" / "Setting"
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
        self.s_img_background = self.canvas.create_image(690.0, 490.0, image=self.background_image)

        # Date text
        self.s_text_date = self.canvas.create_text(
            506.0,
            45.0,
            anchor="nw",
            text="",
            fill="#FFFFFF",
            justify="center",
            font=("Young Serif Regular", 25)
        )

        # Gọi update_date lần đầu
        auto_update_date(self.canvas, self.s_text_date)

        # Back Button
        self.s_back_image = PhotoImage(file=self.relative_to_assets("btn_back.png"))
        self.s_btn_back = Button(
            self.canvas,
            image=self.s_back_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("HomepageFrame"),
            relief="flat"
        )
        self.s_btn_back.place(x=41.0, y=32.0, width=36.0, height=37.0)

        # Log out Button
        self.s_logout_image = PhotoImage(file=self.relative_to_assets("btn_logout.png"))
        self.s_btn_logout = Button(
            self.canvas,
            image=self.s_logout_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("LogInFrame"),
            relief="flat"
        )
        self.s_btn_logout.place(x=1122.0, y=60.0, width=193.0, height=50.0)

        # Change User Information Button
        self.s_changeinformation_image = PhotoImage(file=self.relative_to_assets("btn_changeinformation.png"))
        self.s_btn_changeinformation = Button(
            self.canvas,
            image=self.s_changeinformation_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("ChangeUserInformationFrame"),
            relief="flat"
        )
        self.s_btn_changeinformation.place(x=207.0, y=608.0, width=441.0, height=63.0)

        # Change User Password Button
        self.s_changepassword_image = PhotoImage(file=self.relative_to_assets("btn_changepassword.png"))
        self.s_btn_changepassword = Button(
            self.canvas,
            image=self.s_changepassword_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("ChangeUserPasswordFrame"),
            relief="flat"
        )
        self.s_btn_changepassword.place(x=732.0, y=608.0, width=441.0, height=63.0)

        # Homepage Button
        self.s_homepage_image = PhotoImage(file=self.relative_to_assets("btn_homepage.png"))
        self.s_btn_homepage = Button(
            self.canvas,
            image=self.s_homepage_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("HomepageFrame"),
            relief="flat"
        )
        self.s_btn_homepage.place(x=125.0, y=803.0, width=225.0, height=65.0)

        # Write Journal Button
        self.s_writejournal_image = PhotoImage(file=self.relative_to_assets("btn_writejournal.png"))
        self.s_btn_writejournal = Button(
            self.canvas,
            image=self.s_writejournal_image,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.s_btn_writejournal.place(x=388.0, y=803.0, width=225.0, height=65.0)

        # Recommend Button
        self.s_recommend_image = PhotoImage(file=self.relative_to_assets("btn_recommend.png"))
        self.s_btn_recommend = Button(
            self.canvas,
            image=self.s_recommend_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("ObesityRiskPredictionFrame"),
            relief="flat"
        )
        self.s_btn_recommend.place(x=768.0, y=803.0, width=225.0, height=65.0)

        # Setting Button
        self.s_setting_image = PhotoImage(file=self.relative_to_assets("btn_setting.png"))
        self.s_btn_setting = Button(
            self.canvas,
            image=self.s_setting_image,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.s_btn_setting.place(x=1031.0, y=803.0, width=225.0, height=65.0)
