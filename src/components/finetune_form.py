import json
import tkinter as tk
from utils.model_config import (
    validate_parameters,
    param_limits,
    default_config
)
from .form import Form

"""
Call backs:
User clicks "Start" → Form validates & calls start_callback
start_callback launches training thread
Training process calls progress_callback
progress_callback updates UI through update_status
"""

class FinetuneForm(Form):
    def __init__(self, parent, start_callback):
        super().__init__(parent, start_callback)
        
    def setup_form(self):
        super().setup_form()
        
        # Training Configuration label
        tk.Label(
            self.form,
            text="Training Configuration",
            font=("SF Pro Display", 14, "bold"),
            bg="white"
        ).grid(row=3, column=0, columnspan=3, sticky="w", pady=(20,10))
        
        # Create configuration grid
        config_frame = tk.Frame(self.form, bg="white")
        config_frame.grid(row=4, column=0, columnspan=3, sticky="ew")
        config_frame.grid_columnconfigure(1, weight=1)
        config_frame.grid_columnconfigure(3, weight=1)
        
        # Create configuration input fields
        self.config_vars = {}
        row = 0
        col = 0
        for param, value in default_config["training"].items():
            if param in ['start_idx', 'end_idx']:  # Skip these as they're handled separately
                continue
                
            limits = param_limits[param]
            label_text = param.replace("_", " ").title()
            
            # Add label with parameter limits
            tk.Label(
                config_frame,
                text=f"{label_text} ({limits['min']} - {limits['max']})",
                bg="white"
            ).grid(row=row, column=col*2, sticky="w", pady=5)
            
            # Create variable to store parameter value
            var = tk.StringVar(value=str(value))
            self.config_vars[param] = var
            
            # Create entry field
            entry = tk.Entry(
                config_frame,
                textvariable=var,
                width=20
            )
            entry.grid(row=row, column=col*2+1, sticky="w", padx=(10,20), pady=8)
            
            # Layout management for grid (For every 2 inputs skip a line)
            col = (col + 1) % 2
            if col == 0:
                row += 1
        
        # Create Finetuning button
        button_frame = tk.Frame(self.form, bg="white")
        button_frame.grid(row=6, column=0, columnspan=3, sticky="ew", pady=20)
        
        self.start_btn = tk.Button(
            button_frame,
            text="Start Fine-tuning",
            command=self.start_finetuning,
            relief="solid",
            bg="white",
            bd=1
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
    
    def start_finetuning(self):
        validation_result = self.validate()
        if not validation_result:
            return
            
        dataset_path, model_path, start_idx, end_idx = validation_result
        
        # Build and validate config
        config = {"training": {}}
        
        # Validate training parameters
        for param, var in self.config_vars.items():
            value = validate_parameters(param, var.get())
            if not value:
                return
            config["training"][param] = value
            
        # Disable Finetuning button
        self.start_btn.config(state="disabled")
        # Start training
        self.start_callback(json.dumps(config), dataset_path, model_path, start_idx, end_idx)