import tkinter as tk
from tkinter import ttk
from utils.llm import LLM
from components import (
    LLMInput,
    TitleFrame,
)


class LLMsPage:
    def __init__(self, root):
        self.root = root
        self.container = tk.Frame(self.root, bg="#D2E9FC")
        self.container.grid(row=1, column=1, sticky="nsew")

        self.setup_page()

    def setup_page(self):
        """Initialize and set up the LLMs page """

        self._configure_root()
        self._configure_grid()
        self._setup_styles()
        self._initialize_components()
        self._setup_bindings()

        """ Placeholder content
        tk.Label(
            self.container,
            text="LLMs",
            font=("SF Pro Display", 24, "bold"),
            bg="#D2E9FC"
        ).pack(pady=20)
        """
    def _configure_root(self):
        """Configure root window settings"""
        self.root.title("Assess.ai")
        self.root.configure(bg="#D2E9FC")

    def _configure_grid(self):
        """Configure grid layout"""
        self.container.grid_rowconfigure(0, weight=0)  # Title
        self.container.grid_rowconfigure(1, weight=0)  # LLM Input
        self.container.grid_columnconfigure(0, weight=1)

    def _setup_styles(self):
        """Setup ttk styles"""
        style = ttk.Style()

    def _initialize_components(self):
        # Title
        self.title_frame = TitleFrame(self.container)
        self.title_frame.grid(row=0, column=0, sticky="ew", pady=(0,50))

        # LLM input area
        self.LLMInput = LLMInput(self.container, self.send_path)
        self.LLMInput.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 5))


    def _setup_bindings(self):
        self.root.bind('<Escape>', lambda e: self.root.destroy())

    def send_path(self, model_path):
        # if message is empty
        if not model_path.strip():
            return

        # if message not empty
        self.disable_input(True) # disable text input
        self.LLMInput.output_text.configure(state="normal")
        self.LLMInput.output_text.delete("1.0", tk.END)
        #self.LLMInput.output_text.configure(state="disable")

        # connect to indicated LLM in Hugging Face
        try:
            self.LLM = LLM(model_path)
        except OSError as e:
            #self.LLMInput.output_text.configure(state="normal")
            self.LLMInput.output_text.insert("1.0", "Unsuccessful. Try again.")
            self.LLMInput.output_text.configure(state="disable")
            self.disable_input(False)
            print(f"Error handling LLM: {str(e)}")

        else:
            #self.LLMInput.output_text.configure(state="normal")
            self.LLMInput.output_text.insert("1.0", "Successful!")
            self.LLMInput.output_text.configure(state="disable")
            self.disable_input(False)
            # if successfully connected, save in LLM.txt

    def disable_input(self, disable):
        self.disable = disable
        if disable == True:
            self.LLMInput.input_text.configure(state="disable")
            self.LLMInput.upload_button.configure(state="disable")
        else:
            self.LLMInput.input_text.configure(state="normal")
            self.LLMInput.upload_button.configure(state="normal")



    
