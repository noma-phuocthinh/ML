import tkinter as tk
from pathlib import Path
from tkinter import Canvas, Entry, Button, PhotoImage

class ShowPredictFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.OUTPUT_PATH = Path(__file__).parent.parent
        # Thiết lập đường dẫn assets
        self.ASSETS_PATH = self.OUTPUT_PATH / "assets" / "ShowPredict"
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
        self.sp_img_background = self.canvas.create_image(690.0, 490.0, image=self.background_image)

        # BMI text
        self.sp_text_bmi = self.canvas.create_text(
            187.0,
            242.0,
            anchor="nw",
            text="",
            fill="#000000",
            font=("Young Serif", 32 * -1)
        )

        # Obesity Level text
        self.sp_text_obesitylevel = self.canvas.create_text(
            774.0,
            242.0,
            anchor="nw",
            text="",
            fill="#000000",
            font=("Young Serif", 32 * -1)
        )

        # Goal weight entry
        self.sp_goalweight_image = PhotoImage(file=self.relative_to_assets("entry_goalweight.png"))
        self.sp_goalweight_bg = self.canvas.create_image(396.0, 493.0, image=self.sp_goalweight_image)
        self.sp_entry_goalweight = Entry(
            self.canvas,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            font=("Young Serif", 16),
            highlightthickness=0
        )
        self.sp_entry_goalweight.place(x=186.0, y = 454.0, width = 420.0, height = 76.0)

        # days entry
        self.sp_days_image = PhotoImage(file=self.relative_to_assets("entry_days.png"))
        self.sp_days_bg = self.canvas.create_image(874.0, 493.0, image=self.sp_days_image)
        self.sp_entry_days = Entry(
            self.canvas,
            bd=0,
            bg="#FFFFFF",
            fg="#000716",
            font=("Young Serif", 16),
            highlightthickness=0
        )
        self.sp_entry_days.place(x=774.0, y=454.0, width=200.0, height=76.0)

        # Back button
        self.sp_back_image = PhotoImage(file=self.relative_to_assets("btn_back.png"))
        self.sp_btn_back = Button(
            self.canvas,
            image=self.sp_back_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("ObesityRiskPredictionFrame"),
            relief="flat"
        )
        self.sp_btn_back.place(x=41.0,y=32.0,width=36.0,height=37.0)

        # Breakfast button
        self.sp_breakfast_image= PhotoImage(file=self.relative_to_assets("btn_breakfast.png"))
        self.sp_btn_breakfast = Button(
            self.canvas,
            image=self.sp_breakfast_image,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.sp_btn_breakfast.place(x=218.0,y=683.0,width=228.0,height=61.0)

        # Lunch button
        self.sp_lunch_image = PhotoImage(file=self.relative_to_assets("btn_lunch.png"))
        self.sp_btn_lunch = Button(
            self.canvas,
            image=self.sp_lunch_image,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.sp_btn_lunch.place(x=466.0,y=683.0,width=228.0,height=61.0)

        # Dinner button
        self.sp_dinner_image = PhotoImage(file=self.relative_to_assets("btn_dinner.png"))
        self_sp_btn_dinner = Button(
            self.canvas,
            image=self.sp_dinner_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: print("button_4 clicked"),
            relief="flat"
        )
        self_sp_btn_dinner.place(x=714.0,y=683.0,width=228.0,height=61.0)

        # None button
        self.sp_none_image = PhotoImage(file=self.relative_to_assets("btn_none.png"))
        self.sp_btn_none = Button(
            self.canvas,
            image=self.sp_none_image,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.sp_btn_none.place(x=962.0,y=683.0,width=228.0,height=61.0)

        # Reset button
        self.sp_reset_image = PhotoImage(file=self.relative_to_assets("btn_reset.png"))
        self.sp_btn_reset = Button(
            self.canvas,
            image=self.sp_reset_image,
            borderwidth=0,
            highlightthickness=0,
            relief="flat"
        )
        self.sp_btn_reset.place(x=92.0,y=859.0,width=405.0,height=76.0)

        # Show button
        self.sp_show_image = PhotoImage(file=self.relative_to_assets("btn_show.png"))
        self.sp_btn_show = Button(
            self.canvas,
            image=self.sp_show_image,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.controller.show_frame("PickingPackRecommendFrame"),
            relief="flat"
        )
        self.sp_btn_show.place(x=552.0,y=859.0,width=735.0,height=76.0)




