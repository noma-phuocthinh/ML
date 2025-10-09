import tkinter as tk
from pathlib import Path
from tkinter import Canvas, Entry, Text, Button, PhotoImage

from frontend.resources.Effect import auto_update_date


class ChangeUserInformationFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.OUTPUT_PATH = Path(__file__).parent.parent
        # Thiết lập đường dẫn assets
        self.ASSETS_PATH = self.OUTPUT_PATH / "assets" / "ChangeUserInformation"
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
        self.cui_img_background = self.canvas.create_image(690.0, 490.0, image=self.background_image)

        # Date text
        self.cui_text_date = self.canvas.create_text(
            506.0,
            45.0,
            anchor="nw",
            text="",
            fill="#FFFFFF",
            justify="center",
            font=("Young Serif Regular", 25)
        )

        # Gọi update_date lần đầu
        auto_update_date(self.canvas, self.cui_text_date)

        # Fullname Entry
        self.cui_entry_image = PhotoImage(file=self.relative_to_assets("entry_background.png"))
        self.cui_fullname_bg = self.canvas.create_image(767.0, 256.5, image=self.cui_entry_image)
        self.cui_entry_fullname = Entry(
            self.canvas,
            bd=0,
            bg="#FAFDE0",
            fg="#000716",
            font=("Young Serif", 16),
            highlightthickness=0
        )
        self.cui_entry_fullname.place(x=630.0, y=237.0, width=274.0, height=37.0)

        # Phone Entry
        self.cui_phone_bg = self.canvas.create_image(767.0, 316.5, image=self.cui_entry_image)
        self.cui_entry_phone = Entry(
            self.canvas,
            bd=0,
            bg="#FAFDE0",
            fg="#000716",
            font=("Young Serif", 16),
            highlightthickness=0
        )
        self.cui_entry_phone.place(x=630.0, y=297.0, width=274.0, height=37.0)

        # Email Entry
        self.cui_email_bg = self.canvas.create_image(767.0, 376.5, image=self.cui_entry_image)
        self.cui_entry_email = Entry(
            self.canvas,
            bd=0,
            bg="#FAFDE0",
            fg="#000716",
            font=("Young Serif", 16),
            highlightthickness=0
        )
        self.cui_entry_email.place(x=630.0, y=357.0, width=274.0, height=37.0)

        # Bio Entry
        self.cui_bio_bg = self.canvas.create_image(767.0, 437.5, image=self.cui_entry_image)
        self.cui_entry_bio = Entry(
            self.canvas,
            bd=0,
            bg="#FAFDE0",
            fg="#000716",
            font=("Young Serif", 16),
            highlightthickness=0
        )
        self.cui_entry_bio.place(x=630.0, y=418.0, width=274.0, height=37.0)

        # Back Button
        self.cui_back_image = PhotoImage(file=self.relative_to_assets("btn_back.png"))
        self.cui_btn_back = Button(
            self.canvas,
            image=self.cui_back_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("SettingFrame"),
            relief="flat"
        )
        self.cui_btn_back.place(x=41.0, y=32.0, width=36.0, height=37.0)

        # Log out Button
        self.cui_logout_image = PhotoImage(file=self.relative_to_assets("btn_logout.png"))
        self.cui_btn_logout = Button(
            self.canvas,
            image=self.cui_logout_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("LogInFrame"),
            relief="flat"
        )
        self.cui_btn_logout.place(x=1122.0, y=60.0, width=193.0, height=50.0)

        # Upload photo Button
        self.cui_uploadphoto_image = PhotoImage(file=self.relative_to_assets("btn_uploadphoto.png"))
        self.cui_btn_uploadphoto = Button(
            self.canvas,
            image=self.cui_uploadphoto_image,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.cui_btn_uploadphoto.place(x=607.0, y=474.0, width=319.0, height=46.0)

        # Save Button
        self.cui_save_image = PhotoImage(file=self.relative_to_assets("btn_save.png"))
        self.cui_btn_save = Button(
            self.canvas,
            image=self.cui_save_image,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.cui_btn_save.place(x=447.0, y=565.0, width=486.0, height=49.0)

        # Homepage Button
        self.cui_homepage_image = PhotoImage(file=self.relative_to_assets("btn_homepage.png"))
        self.cui_btn_homepage = Button(
            self.canvas,
            image=self.cui_homepage_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("HomepageFrame"),
            relief="flat"
        )
        self.cui_btn_homepage.place(x=125.0, y=803.0, width=225.0, height=65.0)

        # Write Journal Button
        self.cui_writejournal_image = PhotoImage(file=self.relative_to_assets("btn_writejournal.png"))
        self.cui_btn_writejournal = Button(
            self.canvas,
            image=self.cui_writejournal_image,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.cui_btn_writejournal.place(x=388.0, y=803.0, width=225.0, height=65.0)

        # Recommend Button
        self.cui_recommend_image = PhotoImage(file=self.relative_to_assets("btn_recommend.png"))
        self.cui_btn_recommend = Button(
            self.canvas,
            image=self.cui_recommend_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("ObesityRiskPredictionFrame"),
            relief="flat"
        )
        self.cui_btn_recommend.place(x=768.0, y=803.0, width=225.0, height=65.0)

        # Setting Button
        self.cui_setting_image = PhotoImage(file=self.relative_to_assets("btn_setting.png"))
        self.cui_btn_setting = Button(
            self.canvas,
            image=self.cui_setting_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("SettingFrame"),
            relief="flat"
        )
        self.cui_btn_setting.place(x=1031.0, y=803.0, width=225.0, height=65.0)




