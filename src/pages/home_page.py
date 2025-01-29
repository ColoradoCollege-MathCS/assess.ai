import tkinter as tk
import os
from tkinter import *

class HomePage:
    def __init__(self, root):
        self.root = root
        self.setup_page()
        
    def setup_page(self):
        container = tk.Frame(self.root, bg="#D2E9FC")
        container.grid(row=1, column=1, sticky="nsew")
        
        __location__ = os.path.realpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))
        path = os.path.abspath(__location__)
        path = path + "/logo.png"

        print(path)

        # Placeholder content
        tk.Label(
            container,
            text="Home",
            font=("SF Pro Display", 24, "bold"),
            bg="#D2E9FC"
        ).pack(pady=20)
