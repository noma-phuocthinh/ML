import tkinter as tk
from pathlib import Path
from tkinter import Canvas, Button, PhotoImage

from frontend.resources.Effect import auto_update_date

class HomepageFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.OUTPUT_PATH = Path(__file__).parent.parent
        # Thiết lập đường dẫn assets
        self.ASSETS_PATH = self.OUTPUT_PATH / "assets" / "Homepage"
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

        # Background image
        self.background_image = PhotoImage(file=self.relative_to_assets("background.png"))
        self.hp_img_background = self.canvas.create_image(690.0, 490.0, image=self.background_image)

        # See Details Button
        self.hp_seedetails_image = PhotoImage(file=self.relative_to_assets("btn_seedetails.png"))
        self.hp_btn_seedetails = Button(
            self.canvas,
            image=self.hp_seedetails_image,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.hp_btn_seedetails.place(x=40.0,y=52.0,width=225.0,height=65.0)

        # Sound Button
        self.hp_sound_image = PhotoImage(file=self.relative_to_assets("btn_sound.png"))
        self.hp_btn_sound = Button(
            self.canvas,
            image=self.hp_sound_image,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.hp_btn_sound.place(x=1242.0,y=40.0,width=69.0,height=69.0)

        # Homepage button
        self.hp_homepage = PhotoImage(file=self.relative_to_assets("btn_homepage.png"))
        self.hp_btn_homepage = Button(
            self.canvas,
            image=self.hp_homepage,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.hp_btn_homepage.place(x=125.0,y=803.0,width=225.0,height=65.0)

        # Write Journal Button
        self.hp_writejournal = PhotoImage(file=self.relative_to_assets("btn_writejournal.png"))
        self.hp_btn_writejournal = Button(
            self.canvas,
            image=self.hp_writejournal,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.hp_btn_writejournal.place(x=388.0,y=803.0,width=225.0,height=65.0)

        # Recommend Button
        self.hp_recommend = PhotoImage(file=self.relative_to_assets("btn_recommend.png"))
        self.hp_btn_recommend = Button(
            self.canvas,
            image=self.hp_recommend,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("ObesityRiskPredictionFrame"),
            relief="flat"
        )
        self.hp_btn_recommend.place(x=768.0,y=803.0,width=225.0,height=65.0)

        # Setting Button
        self.hp_setting = PhotoImage(file=self.relative_to_assets("btn_setting.png"))
        self.hp_btn_setting = Button(
            self.canvas,
            image=self.hp_setting,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("SettingFrame"),
            relief="flat"
        )
        self.hp_btn_setting.place(x=1031.0,y=803.0,width=225.0,height=65.0)

        # Date text
        self.hp_text_date = self.canvas.create_text(
            506.0,
            45.0,
            anchor="nw",
            text="",
            fill="#00545F",
            justify="center",
            font=("Young Serif", 25)
        )
        # Gọi update_date lần đầu
        auto_update_date(self.canvas, self.hp_text_date)

        # Fullname text
        self.hp_text_fullname = self.canvas.create_text(
            52.0,
            421.0,
            anchor="nw",
            text="Le Phuoc Thinh",
            fill="#FAFDE0",
            font=("Young Serif", 32 * -1),
            width=400  #
        )

        # lấy đáy của Fullname text
        bbox_fullname = self.canvas.bbox(self.hp_text_fullname)  # (x1, y1, x2, y2)
        fullname_bottom = bbox_fullname[3]  # y2 = đáy của text fullname

        # Quote text
        self.hp_text_quote = self.canvas.create_text(
            54.0,
            fullname_bottom + 10,
            anchor="nw",
            text="“ Bất kì kẻ ngốc nào cũng có thể viết code mà máy tính có thể hiểu. Lập trình viên giỏi viết code mà con người hiểu được. ”",
            fill="#FFFFFF",
            font=("Crimson Pro Italic", 20 * -1),
            width=390
        )

        # Avatar image
        self.hp_avatar_image = PhotoImage(file=self.relative_to_assets("avatar.png"))
        self.hp_img_avatar = self.canvas.create_image(238.0,285.0,image=self.hp_avatar_image)




