import sys
import tkinter as tk
import io
from tkinter import ttk
from subprocess import run
from utils.llm import LLM
from components import (
    LLMInput,
    TitleFrame,
    LLMList
)


class LLMsPage:
    def __init__(self, root):
        self.LLM = None
        self.root = root
        self.container = tk.Frame(self.root, bg="#D2E9FC")
        self.container.grid(row=1, column=1, sticky="nsew")
        self.term_output = ""
        self.setup_page()

    def setup_page(self):
        """Initialize and set up the LLMs page """
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
        self.container.grid_rowconfigure(1, weight=0)  # LLM Input
        self.container.grid_rowconfigure(2, weight=0)
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

        # LLM list area
        self.LLMList = LLMList(self.container)
        self.LLMList.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 5))

    def _setup_bindings(self):
        self.root.bind('<Escape>', lambda e: self.root.destroy())

    def send_path(self, model_path):
        # if message is empty
        if not model_path.strip():
            return

        # if message not empty
        self.disable_input(True) # disable text input
        self.disable_output(False)
        self.LLMInput.output_text.delete("1.0", tk.END)

        # connect to indicated LLM in Hugging Face
        try:
            self.LLM = LLM(model_path) # create LLM
            self.get_output(model_path)
            self.LLM.download_LLM() # download model to file in directory
            output = self.get_output(model_path) # get output from Hugging Face
            self.LLMInput.output_text.insert("1.0", model_path + " was successfully downloaded! \n " + output)

            self.disable_output(True)
            self.disable_input(False)

        except Exception as e:
            self.LLMInput.output_text.insert("1.0", model_path + " could not be downloaded. Try again.")
            self.disable_output(True)
            self.disable_input(False)
            print(f"Error handling LLM: {str(e)}")

    def disable_input(self, disable):
        if disable:
            self.LLMInput.input_text.configure(state="disable")
            self.LLMInput.download_button.configure(state="disable")
        else:
            self.LLMInput.input_text.configure(state="normal")
            self.LLMInput.download_button.configure(state="normal")

    def disable_output(self, disable):
        if disable:
            self.LLMInput.output_text.configure(state="disable")
        else:
            self.LLMInput.output_text.configure(state="normal")

    ### revisit this for later iterations
    def get_output(self, model_path):
        buffer = io.StringIO()
        sys.stdout = buffer
        sys.stderr = buffer

        try:
            self.term_output = buffer.getvalue()
        except Exception as e:
            self.term_output = f"Error: {str(e)}"

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        return self.term_output












