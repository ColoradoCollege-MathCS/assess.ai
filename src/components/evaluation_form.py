import tkinter as tk
from tkinter import simpledialog
from .form import Form

"""
Call backs:
User clicks "Start" → Form validates & calls start_callback
start_callback launches evaluation thread
Evaluation process calls progress_callback
progress_callback updates UI through update_status
"""

class EvaluationForm(Form):
    def __init__(self, parent, start_callback):
        # Passes handle_start_evaluation from evaluation_page.py
        super().__init__(parent, start_callback)
        
    def setup_form(self):
        super().setup_form()
        
        geval_frame = tk.Frame(self.form, bg="white")
        geval_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(0, 10))
            
        # Add G-EVAL toggle after the range frame
        # tk.BooleanVar sets a boolean value for Tkinter widgets
        self.use_geval = tk.BooleanVar(value=True)
        self.geval_toggle = tk.Checkbutton(
            geval_frame,
            text="Enable G-EVAL Metrics",
            variable=self.use_geval,
            bg="white",
            font=("SF Pro Display", 12)
        )
        self.geval_toggle.pack(side=tk.LEFT)
        
        button_frame = tk.Frame(self.form, bg="white")
        button_frame.grid(row=4, column=0, columnspan=3, sticky="ew", pady=20)
        
        self.start_btn = tk.Button(
            button_frame,
            text="Start Evaluation",
            command=self.start_evaluation,
            relief="solid",
            bg="white",
            bd=1
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
    def start_evaluation(self):
        validation_result = self.validate()
        if not validation_result:
            return
            
        dataset_path, model_path, start_idx, end_idx = validation_result
        
        # Ask for folder name using a popup dialog
        custom_folder_name = simpledialog.askstring(
            "Custom Folder Name", 
            "Enter a custom folder name (optional):",
            parent=self.form
        )
            
        # Disable start button
        self.start_btn.config(state="disabled")
        
        # Call the callback function with indices
        self.start_callback(
            dataset_path, 
            model_path,
            start_idx,
            end_idx,
            self.use_geval.get(),
            custom_folder_name  # Pass the custom folder name
        )