import sys
import tkinter as tk
import io
import os
from tkinter import ttk
from tkinter import PhotoImage
from subprocess import run
from pages.llms_page import LLMsPage
from utils.llm import LLM
from components import (
    LLMInput,
    TitleFrame,
    LLMList
)

class HomePage:
    def __init__(self, root, show_page_callback):
        self.home = None
        self.root = root
        self.container = tk.Frame(self.root, bg="#D2E9FC")
        self.container.grid(row=1, column=1, sticky="nsew")
        self.llmlist = None
        self.show_page_callback = show_page_callback
        self.setup_page()


    def setup_page(self):
<<<<<<< HEAD
        """Initialize and set up the homepage page """
        self._configure_root()
        self._configure_grid()
        self._setup_styles()
        self._initialize_components()
        self._setup_bindings()


    def _configure_root(self):
        """Configure root window settings"""
        self.root.title("Assess.ai")
        self.root.configure(bg="#D2E9FC")

    def _configure_grid(self):
        """Configure grid layout"""
        self.container.grid_rowconfigure(0, weight=0)  # Title
        self.container.grid_rowconfigure(1, weight=0) #homepage label
        self.container.grid_rowconfigure(2, weight=0) #button
        self.container.grid_rowconfigure(3, weight=0)  #labels
        self.container.grid_rowconfigure(4, weight=1)   #list boxes
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)

    def _setup_styles(self):
        """Setup ttk styles"""
        style = ttk.Style()


    def _initialize_components(self):

        # welcome label
        title_lbl = tk.Label(self.container, text="WELCOME TO ASSESS.AI", font=("SF Pro Display", 24, "bold"), bg="#D2E9FC", fg="black")
        title_lbl.grid(row=0,column=0, columnspan=2,pady=10,sticky="n")

        # homepage label
        homepage_lbl = tk.Label(self.container, text="Homepage", font=("SF Pro Display", 18, "bold"), bg="#D2E9FC", fg="black")
        homepage_lbl.grid(row=1,column=0, columnspan=2,pady=5,sticky="n")

        # nav button
        self.llm_button = ttk.Button(self.container, text="New? Get started with LLM page", command=self.nav_to_llm)
        # the command is a placeholder for now
        self.llm_button.grid(row=2, column=0, columnspan=2, pady=10, padx=20, sticky="ew")

        # Listbox for past llms used
        llm_lbl=tk.Label(self.container, text="Past LLMs Used:", font=("SF Pro Display", 14), bg="#D2E9FC", fg="black")
        llm_lbl.grid(row=3,column=0, padx=20, pady=(5, 0),sticky="w")
        self.llm_lb = tk.Listbox(self.container, height=10)
        self.llm_lb.grid(row=4,column=0, padx=20, pady=10, sticky="nsew")
        self.load_past_llms() #loading past llms CHANGE (changed)


        # List box for past evals
        eval_label = tk.Label(self.container, text="Past Evaluations:", font=("SF Pro Display", 14), bg="#D2E9FC", fg="black")
        eval_label.grid(row=3,column=1, padx=20, pady=(5,0),sticky="w")
        self.eval_lb = tk.Listbox(self.container, height=10)
        self.eval_lb.grid(row=4, column=1, padx=20, pady=10, sticky="nsew")
        # load eval results into lb
        # placeholder content
        self.load_evaluations()


    def _setup_bindings(self):
        self.root.bind('<Escape>', lambda e: self.root.destroy())


    def load_evaluations(self):
        # cd to parent directory
        cwd = os.getcwd() # current directory
        parent = os.path.dirname(cwd) # parent directory
        eval_folder = os.path.join(parent, "eval_files")
        if not os.path.exists(eval_folder):
            print(f"Error: {eval_folder} directory does not exist.")
            return
        try:
            eval_dirs = [d for d in os.listdir(eval_folder) if os.path.isdir(os.path.join(eval_folder, d))]
            # Insert directory names into the Listbox
            for eval_dir in eval_dirs:
                self.eval_lb.insert(tk.END, eval_dir)  # Add the directory name to Listbox (this could also be filename if saved differently)

        except FileNotFoundError:
            print(f"Error: {eval_folder} not found.")


    def nav_to_llm(self):
        # change displaying page
        print("navigating to llm page...")
        self.show_page_callback("llms")


    def load_past_llms(self):
        # load past llms in to the listbox
        self.llmlist = LLMList (self.container, self.root)# create LLMList object
        imported_models = self.llmlist.get_models() # get_models

        # write to listbox
        self.llm_lb.delete(0, tk.END)  # delete existing entries
        count = 0
        for model in imported_models:
            count += 1
            self.llm_lb.insert(count, model)



