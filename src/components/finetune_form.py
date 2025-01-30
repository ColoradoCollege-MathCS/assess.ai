import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import json

"""
Call backs:
User clicks "Start" → Form validates & calls start_callback
start_callback launches training thread
Training process calls progress_callback
progress_callback updates UI through update_status

"""

class FinetuneForm:
    def __init__(self, parent, start_callback):
        self.parent = parent
        self.start_callback = start_callback
        
        # Define parameter limits for model fine-tuning
        self.param_limits = {
            "num_epochs": {"min": 1, "max": 20},          # Number of training epochs
            "batch_size": {"min": 1, "max": 32},          # Batch size for training
            "learning_rate": {"min": 1e-6, "max": 1e-3},  # Learning rate range
            "max_samples": {"min": 10, "max": 10000},     # Maximum number of training samples
            "max_length": {"min": 64, "max": 1024},       # Maximum sequence length
            "num_beams": {"min": 1, "max": 8}             # Number of beams for beam search
        }
        
        self.default_config = {
            "training": {
                "num_epochs": 3,
                "batch_size": 2,
                "learning_rate": 2e-5,
                "max_samples": 100,
                "max_length": 256,
                "num_beams": 4
            }
        }
        
        self.setup_form()
        
    def setup_form(self):
        form = tk.Frame(self.parent, bg="white")
        form.grid(row=2, column=0, sticky="nsew", padx=30, pady=25)
        form.grid_columnconfigure(1, weight=1)
        
        # Dataset path selection UI
        tk.Label(form, text="Dataset Path", bg="white").grid(row=0, column=0, sticky="w", pady=5)
        
        self.path_var = tk.StringVar()
        tk.Entry(form, textvariable=self.path_var).grid(row=0, column=1, sticky="ew", padx=(10,10), pady=5)
        
        tk.Button(
            form,
            text="Browse",
            command=self.browse_dataset,
            relief="solid",
            bd=1
        ).grid(row=0, column=2, pady=5)

        tk.Label(
            form,
            text="Training Configuration",
            font=("SF Pro Display", 14, "bold"),
            bg="white"
        ).grid(row=2, column=0, columnspan=3, sticky="w", pady=(20,10))
        
        # Create configuration grid
        config_frame = tk.Frame(form, bg="white")
        config_frame.grid(row=3, column=0, columnspan=3, sticky="ew")
        config_frame.grid_columnconfigure(1, weight=1)
        config_frame.grid_columnconfigure(3, weight=1)
        
        # Create configuration input fields
        self.config_vars = {}
        row = 0
        col = 0
        for param, value in self.default_config["training"].items():
            limits = self.param_limits[param]
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
            
            # Checks if config for training is valid and not beyond limits
            def validate_input(action, value, param=param):
                if action == '1':  # Insert action
                    try:
                        # Validate integer fields
                        if param in ["num_epochs", "batch_size", "max_samples", "max_length", 
                                   "num_beams"]:
                            if not value == "" and not value.isdigit(): #Check if value is a whole number and not a digit
                                return False
                            if value and int(value) > self.param_limits[param]["max"]: #Check if its within the limit
                                return False
                        else:
                            # Validate float fields
                            if value == "" or value == "-":
                                return True
                            try:
                                float_val = float(value)
                                if float_val > self.param_limits[param]["max"]:
                                    return False
                                if float_val < self.param_limits[param]["min"]:
                                    return False
                            except ValueError:
                                return False
                    except ValueError:
                        return False
                return True
            
            # Register validation command
            vcmd = (self.parent.register(validate_input), '%d', '%P')
            entry.configure(validate='key', validatecommand=vcmd)
            
            # Layout management for grid
            col = (col + 1) % 2
            if col == 0:
                row += 1
        
        # Create control button section
        button_frame = tk.Frame(form, bg="white")
        button_frame.grid(row=4, column=0, columnspan=3, sticky="ew", pady=20)
        
        self.start_btn = tk.Button(
            button_frame,
            text="Start Fine-tuning",
            command=self.start_finetuning,
            relief="solid",
            bg="white",
            bd=1
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        # Training log section
        tk.Label(
            form,
            text="Training Log",
            font=("SF Pro Display", 14, "bold"),
            bg="white"
        ).grid(row=5, column=0, columnspan=3, sticky="w", pady=(20,10))
        
        self.log_text = tk.Text(
            form,
            height=10,
            width=50,
            relief="solid",
            bd=1,
            font=("Courier", 10),
            bg="#FAFAFA"
        )
        self.log_text.grid(row=6, column=0, columnspan=3, sticky="ew")
        
    def validate_param(self, param, value):
        # Check parameters
        try:
            limits = self.param_limits[param]
            if param in ["num_epochs", "batch_size", "max_samples", "max_length", 
                        "num_beams"]:
                value = int(value)
            else:
                value = float(value)
                
            if value < limits["min"] or value > limits["max"]:
                return False, f"{param} must be between {limits['min']} and {limits['max']}"
            return True, value
        except ValueError:
            return False, f"Invalid value for {param}"

    def browse_dataset(self):
        # Open file dialog for dataset selection
        filetypes = (
            ('JSON files', '.json'),
            ('JSONL files', '.jsonl'),
            ('CSV files', '.csv'),
            ('Text files', '.txt')
        )
        filename = filedialog.askopenfilename(
            title='Select Dataset File',
            filetypes=filetypes
        )
        if filename:
            self.path_var.set(filename)
            
    def update_status(self, message, is_error=False):
        # adds new messages to the log window that shows training progress
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
            
    def get_current_config(self):
        # Get and validate current configuration values
        config = {"training": {}}
        for param, var in self.config_vars.items():
            valid, result = self.validate_param(param, var.get())
            if not valid:
                messagebox.showerror("Error", result)
                return None
            config["training"][param] = result
        return json.dumps(config)
        
    def start_finetuning(self):
        if not self.path_var.get():
            messagebox.showerror("Error", "Please select a dataset file")
            return
            
        config = self.get_current_config()
        if config is None:
            return
            
        # Disable start button
        self.start_btn.config(state="disabled")
        
        # Call the callback function directly
        self.start_callback(config, self.path_var.get())