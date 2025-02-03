import tkinter as tk
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
        
        # Evaluation Button
        button_frame = tk.Frame(self.form, bg="white")
        button_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=20)
        
        self.start_btn = tk.Button(
            button_frame,
            text="Start Evaluation",
            command=self.start_evaluation,
            relief="solid",
            bg="white",
            bd=1
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
<<<<<<< HEAD
        
=======
    
>>>>>>> a0610ba1835c74dcf76d954652a1a43adb5e15a1
    def start_evaluation(self):
        validation_result = self.validate()
        if not validation_result:
            return
            
        dataset_path, model_path, start_idx, end_idx = validation_result
<<<<<<< HEAD
        
        # Clear any existing plot
        if hasattr(self, 'evaluator') and self.evaluator:
            self.evaluator.clear_plot()
=======
>>>>>>> a0610ba1835c74dcf76d954652a1a43adb5e15a1
            
        # Disable start button
        self.start_btn.config(state="disabled")
        
        # Call the callback function with indices
        self.start_callback(
            dataset_path, 
            model_path,
            start_idx,
            end_idx
<<<<<<< HEAD
        )
=======
        )
>>>>>>> a0610ba1835c74dcf76d954652a1a43adb5e15a1
