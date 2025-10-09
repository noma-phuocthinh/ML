import tkinter as tk
from pathlib import Path
from tkinter import Canvas, Entry, Text, Button, PhotoImage

class PickingPackRecommendFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.OUTPUT_PATH = Path(__file__).parent.parent
        # Thiết lập đường dẫn assets
        self.ASSETS_PATH = self.OUTPUT_PATH / "assets" / "PickingPackRecommend"
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
        self.ppr_img_background = self.canvas.create_image(690.0, 490.0, image=self.background_image)

        # Back button
        self.ppr_back_image = PhotoImage(file=self.relative_to_assets("btn_back.png"))
        self.ppr_btn_back = Button(
            self.canvas,
            image=self.ppr_back_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("ShowPredictFrame"),
            relief="flat"
        )
        self.ppr_btn_back.place(x=41.0, y=32.0, width=36.0, height=37.0)

        # Show recipe button
        self.ppr_showrecipe_image = PhotoImage(file=self.relative_to_assets("btn_showrecipe.png"))
        self.ppr_btn_showrecipe1 = Button(
            self.canvas,
            image=self.ppr_showrecipe_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("ShowRecipeFrame"),
            relief="flat"
        )
        self.ppr_btn_showrecipe1.place(x=835.0, y=422.0, width=289.0, height=50.0)

        self.ppr_btn_showrecipe2 = Button(
            self.canvas,
            image=self.ppr_showrecipe_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("ShowRecipeFrame"),
            relief="flat"
        )
        self.ppr_btn_showrecipe2.place(x=838.0, y=486.0, width=289.0, height=50.0)

        self.ppr_btn_showrecipe3 = Button(
            self.canvas,
            image=self.ppr_showrecipe_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("ShowRecipeFrame"),
            relief="flat"
        )
        self.ppr_btn_showrecipe3.place(x=838.0, y=555.0, width=289.0, height=50.0)

        # Homepage button
        self.ppr_homepage = PhotoImage(file=self.relative_to_assets("btn_homepage.png"))
        self.ppr_btn_homepage = Button(
            self.canvas,
            image=self.ppr_homepage,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("HomepageFrame"),
            relief="flat"
        )
        self.ppr_btn_homepage.place(x=125.0, y=803.0, width=225.0, height=65.0)

        # Write journal button
        self.ppr_writejournal_image = PhotoImage(file=self.relative_to_assets("btn_writejournal.png"))
        self.ppr_btn_writejournal = Button(
            self.canvas,
            image=self.ppr_writejournal_image,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.ppr_btn_writejournal.place(x=388.0, y=803.0, width=225.0, height=65.0)

        # Recommend button
        self.ppr_recommend_image = PhotoImage(file=self.relative_to_assets("btn_recommend.png"))
        self.ppr_btn_recommend = Button(
            self.canvas,
            image=self.ppr_recommend_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("ObesityRiskPredictionFrame"),
            relief="flat"
        )
        self.ppr_btn_recommend.place(x=768.0, y=803.0, width=225.0, height=65.0)

        # Setting Button
        self.ppr_setting = PhotoImage(file=self.relative_to_assets("btn_setting.png"))
        self.ppr_btn_setting = Button(
            self.canvas,
            image=self.ppr_setting,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("SettingFrame"),
            relief="flat"
        )
        self.ppr_btn_setting.place(x=1031.0, y=803.0, width=225.0, height=65.0)

        # calories text
        self.ppr_text_calories1 = self.canvas.create_text(
            542.0,
            423.0,
            anchor="nw",
            text="2000 calories",
            fill="#FDFEDF",
            font=("Young Serif", 32 * -1)
        )
        self.ppr_text_calories2 = self.canvas.create_text(
            542.0,
            487.0,
            anchor="nw",
            text="1000 calories",
            fill="#FDFEDF",
            font=("Young Serif", 32 * -1)
        )
        self.ppr_text_calories3 = self.canvas.create_text(
            542.0,
            556.0,
            anchor="nw",
            text="1000 calories",
            fill="#FDFEDF",
            font=("Young Serif", 32 * -1)
        )

        # calories per day text
        self.ppr_text_caloriesperday = self.canvas.create_text(
            225.0,
            250.0,
            anchor="nw",
            text="",
            fill="#000000",
            font=("Young Serif", 32 * -1)
        )
