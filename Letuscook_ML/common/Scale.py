
class UIAutoScaler:
    def __init__(self, frame, canvas, base_width=1380, base_height=980):
        self.frame = frame
        self.canvas = canvas
        self.base_width = base_width
        self.base_height = base_height

        self.screen_w = frame.winfo_screenwidth()
        self.screen_h = frame.winfo_screenheight()

        self.scale_x = self.screen_w / base_width
        self.scale_y = self.screen_h / base_height
        self.scale = min(self.scale_x, self.scale_y)

    def scale_canvas(self):
        self.canvas.scale("all", 0, 0, self.scale, self.scale)
        self.canvas.config(width=self.screen_w, height=self.screen_h)

    def scale_widgets(self):
        for widget in self.canvas.winfo_children():
            info = widget.place_info()
            if isinstance(info, dict):
                x = float(info["x"]) * self.scale
                y = float(info["y"]) * self.scale
                w = float(info["width"]) * self.scale
                h = float(info["height"]) * self.scale
                widget.place(x=x, y=y, width=w, height=h)
            else:
                pass

    def scale_font(self, base_font_size=16):
        new_font_size = int(base_font_size * self.scale)
        for widget in self.frame.winfo_children():
            try:
                widget.config(font=("Young Serif", new_font_size))
            except :
                pass


    def autoScale(self, font):
        self.scale_canvas()
        self.scale_widgets()
        self.scale_font(font)




