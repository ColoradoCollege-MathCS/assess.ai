import tkinter as tk
from tkinter import *
import os
from tkinter import ttk
from pages.indiv_page import LLMPage
from components import (
    LLMList
)
from components.eval_window import EvaluationWindow

class HomePage:
    def __init__(self, root, show_page_callback, navbar):
        self.home = None
        self.root = root
        self.navbar = navbar
        self.container = tk.Frame(self.root, bg="#D2E9FC")
        self.container.grid(row=1, column=1, sticky="nsew")
        self.llmlist = LLMList(self.container, self.root)
        self.show_page_callback = show_page_callback
        self.eval_window = EvaluationWindow(self.root)
        self.setup_page()

    def setup_page(self):
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
        self.container.grid_rowconfigure(1, weight=0)  #homepage label
        self.container.grid_rowconfigure(2, weight=0)  #button
        self.container.grid_rowconfigure(3, weight=0)  #labels
        self.container.grid_rowconfigure(4, weight=1)  #list boxes
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=1)

    def _setup_styles(self):
        """Setup ttk styles"""
        style = ttk.Style()

    def _initialize_components(self):
        # welcome label
        title_lbl = tk.Label(self.container, text="Welcome to ASSESS.AI!", font=("SF Pro Display", 24, "bold"), bg="#D2E9FC", fg="black")
        title_lbl.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

        
        # nav button
        self.llm_button = tk.Canvas(
            self.container,
            width=300,  # Wider to accommodate longer text
            height=60,
            bg="#D2E9FC",
            highlightthickness=0,
            cursor="hand2"
        )
        self.llm_button.grid(row=2, column=0, columnspan=2, pady=10, padx=20)

        # Use blue button design from LLMPage
        padding = 10
        self.button_rect = self.llm_button.create_rectangle(
            padding, padding,
            300-padding, 50,  # Adjusted for wider button
            fill="#0A84FF",
            outline=""
        )
        self.button_text = self.llm_button.create_text(
            150, 30,  # Centered in the wider button
            text="New? Get started with LLM page",
            fill="white",
            font=("SF Pro Text", 15),
            anchor="center"
        )
        # Bind click event
        self.llm_button.bind("<Button-1>", lambda e: self.nav_to_llm())

        # Listbox for past llms used
        llm_lbl = tk.Label(self.container, text="Past LLMs Used:", font=("SF Pro Display", 14), bg="#D2E9FC", fg="black")
        llm_lbl.grid(row=3, column=0, padx=20, pady=(5, 0), sticky="w")
        self.llm_lb = tk.Listbox(self.container, height=10)
        self.llm_lb.grid(row=4, column=0, padx=20, pady=10, sticky="nsew")

        self.llm_lb.bind("<ButtonRelease-1>", self.model_selected)  # bind list
        self.load_past_llms()  #loading past llms CHANGE (changed)

        # List box for past evals
        eval_label = tk.Label(self.container, text="Past Evaluations:", font=("SF Pro Display", 14), bg="#D2E9FC", fg="black")
        eval_label.grid(row=3, column=1, padx=20, pady=(5,0), sticky="w")
        self.eval_lb = tk.Listbox(self.container, height=10)
        self.eval_lb.grid(row=4, column=1, padx=20, pady=10, sticky="nsew")
        self.eval_lb.bind("<ButtonRelease-1>", self.evaluation_selected)
        # load eval results into lb
        # placeholder content
        self.load_evaluations()

    def _setup_bindings(self):
        self.root.bind('<Escape>', lambda e: self.root.destroy())

    def load_evaluations(self):
        # cd to parent directory
        cwd = os.getcwd()  # current directory 
        parent = os.path.dirname(cwd)  # parent directory
        eval_folder = os.path.join(parent, "eval_files")
        if not os.path.exists(eval_folder):
            os.makedirs(eval_folder)
            print(f"Created directory: {eval_folder}")
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
        self.navbar.set_active_page("llms")

    def load_past_llms(self):
        # load past llms in to the listbox
        imported_models = self.llmlist.get_models()  # get_models

        # write to listbox
        self.llm_lb.delete(0, tk.END)  # delete existing entries
        count = 0
        for model in imported_models:
            count += 1
            self.llm_lb.insert(count, model)

    def model_selected(self, event):
        selection = self.llm_lb.curselection()
        if selection:
            self.selected_model = self.llm_lb.get(selection)
            self.create_window(self.selected_model)

    def create_window(self, model_name):
        # main window object
        new_win = Toplevel(self.root)  # create toplevel widget

        # set title + dimensions
        new_win.title(model_name)
        new_win.geometry("500x500")

        # populate window with model specific material
        self.detail_page = LLMPage(new_win, self.selected_model)

    def evaluation_selected(self, event):
        selection = self.eval_lb.curselection()
        if selection:
            selected_eval = self.eval_lb.get(selection)
            self.eval_window.show_evaluation(selected_eval)