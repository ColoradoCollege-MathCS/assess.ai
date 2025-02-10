import sys
import tkinter as tk
import io
from tkinter import ttk
from utils.llm import LLM
from components import (
    TitleFrame,
    LLMInput,
    LLMList
)


class LLMsPage:
    def __init__(self, root):
        self.LLM = None
        self.root = root

        self.container = tk.Frame(self.root, bg="#D2E9FC")
        self.container.grid(row=1, column=1, sticky="nsew")
        self.setup_page()

    def setup_page(self):
        """Initialize and set up the LLMs page """
        self._configure_root()
        self._configure_grid()
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
        self.container.grid_columnconfigure(0, weight=1)

    def _initialize_components(self):
        # Title
        self.title_frame = TitleFrame(self.container)
        self.title_frame.grid(row=0, column=0, sticky="ew", pady=(0,50))

        # LLM input area
        self.LLMInput = LLMInput(self.container, self.root, self.send_path)
        self.LLMInput.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 5))

    def _setup_bindings(self):
        self.root.bind('<Escape>', lambda e: self.root.destroy())

    def send_path(self, model_path):
        self.LLMInput.disable_input(True) # disable text input
        self.LLMInput.output_text.delete("1.0", tk.END)

        # connect to indicated LLM in Hugging Face
        try:
            self.LLM = LLM(model_path) # create LLM
            self.LLM.load_LLM() # load LLM
            self.LLM.import_LLM() # import model to file in directory
            output = self.get_output(model_path) # get output from Hugging Face
            self.LLMInput.output_text.insert("1.0", model_path + " was successfully imported! \n " + output)
            self.LLMInput.disable_input(False)
            self.LLMInput.disable_output(True)

        except Exception as e:
            self.LLMInput.output_text.insert("1.0", model_path + " could not be imported. Try again.")
            self.LLMInput.disable_input(False)
            self.LLMInput.disable_output(True)
            print(f"Error handling LLM: {str(e)}")

        self.LLMInput.LLMList.write_list(self.LLMInput.LLMList.get_models())


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















