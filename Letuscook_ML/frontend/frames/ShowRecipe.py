import tkinter as tk
from pathlib import Path
from tkinter import Canvas, Entry, Button, PhotoImage

class ShowRecipeFrame(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.OUTPUT_PATH = Path(__file__).parent.parent
        # Thiết lập đường dẫn assets
        self.ASSETS_PATH = self.OUTPUT_PATH / "assets" / "ShowRecipe"
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
        # self.background_image = PhotoImage(file=self.relative_to_assets("background.png"))
        # self.sp_img_background = self.canvas.create_image(690.0, 490.0, image=self.background_image)