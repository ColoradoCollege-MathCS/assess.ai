import tkinter as tk
import os
from components.rounded_frame import RoundedFrame

class LLMList(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, bg="#D2E9FC", **kwargs)
        self.setup_list_area()

    def setup_list_area(self):
        self.grid_columnconfigure(0, weight=1)

        # Container frame for list
        self.container = tk.Frame(self, bg="#D2E9FC")
        self.container.grid(row=0, column=0, sticky="ew", padx=20, pady=15)
        self.container.grid_columnconfigure(0, weight=1)

        # list container with rounded corners
        self.list_container = RoundedFrame(self.container, "#FFFFFF", radius=50)
        self.list_container.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.list_container.grid_columnconfigure(0, weight=1)

        # LLM list area
        self.list = tk.Listbox(
            self.list_container,
            height=20,
            width=20,
            font=("SF Pro Text", 14),
            bd=0,
            bg="white",
            highlightthickness=0,
            relief="flat"
        )
        self.list.grid(row=0, column=0, sticky="ew", padx=20, pady=2)
        self.write_list(self.get_models())


    def get_models(self):
        folder_list = []
        cwd = os.getcwd() # current directory
        parent = os.path.dirname(cwd)# parent directory
        model_dir = os.path.join(parent, "model_files")
        # check if model_files
        for folder in os.listdir(model_dir): # list all folders in model_files folder
            if os.path.isdir(os.path.join(model_dir, folder)):
                folder_list.append(folder)
        return folder_list

    def write_list(self, list):
        self.list.delete(0,tk.END) # delete existing entries
        count = 0
        for model in list:
            count += 1
            self.list.insert(count, model)








