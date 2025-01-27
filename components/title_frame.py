import tkinter as tk

class TitleFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="#D2E9FC", **kwargs)
        
        self.title_label = tk.Label(
            self,
            text="Assess.ai",
            bg="#D2E9FC",
            fg="#1a1a1a",
            font=("SF Pro Display", 24, "bold")
        )
        self.title_label.pack()  