import tkinter as tk
from utils.model_config import validate_dataset_indices, browse_file

class Form:
    def __init__(self, parent, start_callback):
        self.parent = parent
        # Passes handle_start_evaluation from evaluation_page.py
        self.start_callback = start_callback
        self.setup_form()
        # Calls the function below
    
    def setup_form(self):
        self.form = tk.Frame(self.parent, bg="white")
        self.form.grid(row=2, column=0, sticky="nsew", padx=30, pady=25)
        self.form.grid_columnconfigure(1, weight=1)
        
        # Dataset path selection
        tk.Label(self.form, text="Dataset Path", bg="white").grid(row=0, column=0, sticky="w", pady=5)
        self.dataset_path_var = tk.StringVar()
        tk.Entry(self.form, textvariable=self.dataset_path_var).grid(row=0, column=1, sticky="ew", padx=(10,10), pady=5)
        tk.Button(
            self.form,
            text="Browse",
            command=lambda: self.browse_file("dataset"),
            relief="solid",
            bd=1
        ).grid(row=0, column=2, pady=5)
        
        # Model path selection
        tk.Label(self.form, text="Model Path", bg="white").grid(row=1, column=0, sticky="w", pady=5)
        self.model_path_var = tk.StringVar()
        tk.Entry(self.form, textvariable=self.model_path_var).grid(row=1, column=1, sticky="ew", padx=(10,10), pady=5)
        tk.Button(
            self.form,
            text="Browse",
            command=lambda: self.browse_file("model"),
            relief="solid",
            bd=1
        ).grid(row=1, column=2, pady=5)
        
        # Data range selection
        range_frame = tk.Frame(self.form, bg="white")
        range_frame.grid(row=2, column=0, columnspan=3, sticky="ew", pady=10)
        range_frame.grid_columnconfigure(1, weight=1)
        range_frame.grid_columnconfigure(3, weight=1)
        
        tk.Label(range_frame, text="Data Range", font=("SF Pro Display", 12, "bold"), bg="white").grid(
            row=0, column=0, columnspan=4, sticky="w", pady=(10,5)
        )
        
        # Start index
        tk.Label(range_frame, text="Start Index", bg="white").grid(row=1, column=0, sticky="w", padx=(0,5))
        self.start_idx_var = tk.StringVar(value="0")
        tk.Entry(range_frame, textvariable=self.start_idx_var, width=10).grid(row=1, column=1, sticky="w")
        
        # End index
        tk.Label(range_frame, text="End Index", bg="white").grid(row=1, column=2, sticky="w", padx=(20,5))
        self.end_idx_var = tk.StringVar(value="100")
        tk.Entry(range_frame, textvariable=self.end_idx_var, width=10).grid(row=1, column=3, sticky="w")
        
        # Create the log label
        self.log_label = tk.Label(
            self.form,
            text="Log",
            font=("SF Pro Display", 14, "bold"),
            bg="white"
        )
        self.log_label.grid(row=4, column=0, columnspan=3, sticky="w", pady=(20,10))
        
        self.log_text = tk.Text(
            self.form,
            height=10,
            width=50,
            relief="solid",
            bd=1,
            font=("Courier", 10),
            bg="#FAFAFA"
        )
        self.log_text.grid(row=5, column=0, columnspan=3, sticky="ew")
    
    def browse_file(self, file_type):
        browse_file(file_type, self.dataset_path_var if file_type == "dataset" else self.model_path_var)
    
    def update_status(self, message, is_error=False):
        # adds new messages to the log window
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
    
    def validate(self):
        # Validate indices
        indices = validate_dataset_indices(self.start_idx_var.get(), self.end_idx_var.get())
        start_idx, end_idx = indices
        if not indices:
            return None
            
        return self.dataset_path_var.get(), self.model_path_var.get(), start_idx, end_idx

