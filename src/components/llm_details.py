import tkinter as tk
from components.rounded_frame import RoundedFrame
import json
import os
from itertools import islice
from collections import OrderedDict

class LLMDetails(tk.Frame):
    def __init__(self, parent, llm, **kwargs):
        super().__init__(parent, bg="#D2E9FC", **kwargs)
        self.llm = llm
        self.setup_input_area()

    def setup_input_area(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Container frame for LLM Name, LLM Details
        self.container = tk.Frame(self, bg="#D2E9FC")
        self.container.grid(row=0, column=0, sticky="nsew", padx=0, pady=15)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=1)
        self.container.grid_columnconfigure(0, weight=1)  # for name frame
        self.container.grid_columnconfigure(1, weight=1)  # for details frame

        # LLM Name container
        self.llm_name_container = tk.Frame(self.container, bg="#D2E9FC")
        self.llm_name_container.grid(row=0, column=0, sticky="ew", padx=(5, 10), pady=(20, 5))
        self.llm_name_container.grid_columnconfigure(0, weight=1)
        
	# LLM details container frame with rounded corners
        self.llm_details_container = RoundedFrame(self.container, "#FFFFFF", radius=50)
        self.llm_details_container.grid(row=1, column=0, sticky="nsew", padx=(20, 5), pady=10)
        self.llm_details_container.grid_rowconfigure(0, weight=1)
        self.llm_details_container.grid_columnconfigure(0, weight=1)

        # "LLM Name" string variable
        string = tk.StringVar()
        string.set("LLM: " + self.llm)

        # "Import LLM" area
        self.name_label = tk.Label(
            self.llm_name_container,
            textvariable=string,
            bg="#D2E9FC",
            font=("SF Pro Text", 30),
            fg="black",
            anchor="w",
            justify="left"
        )
        self.name_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        # LLM detail area
        self.details = tk.Text(
            self.llm_details_container,
            height=30,
            width=40,
            font=("SF Pro Text", 14),
            wrap=tk.WORD,
            bd=0,
            bg="white",
            highlightthickness=0,
            relief="flat"
        )

        self.details.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.details.grid_rowconfigure(0, weight=1)
        config = self.get_model_info()

        # get first 10 in config
        first_twenty = dict(islice(config.items(), 20))
        rev = OrderedDict(reversed(list(first_twenty.items())))
        for key, value in rev.items():
            str_key = str(key)
            str_value = str(value)
            self.details.insert("1.0", "\n")
            self.details.insert("1.0", str_key + ": " + str_value)
            self.details.insert("1.0", "\n")


    def get_model_info(self):
        # cd to model_files
        cwd = os.getcwd()
        parent = os.path.dirname(cwd)
        file = "model_files/" + self.llm + "/" + 'config.json'
        model_dir = os.path.join(parent, file)
        f = open(model_dir) # read config file of selected model
        config = json.load(f) # load configurations
        return config

