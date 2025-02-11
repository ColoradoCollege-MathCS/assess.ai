import os
from tkinter import messagebox, filedialog

# Define parameter limits for model fine-tuning
param_limits = {
    "num_epochs": {"min": 1, "max": 20},          # Number of training epochs
    "batch_size": {"min": 1, "max": 32},          # Batch size for training
    "learning_rate": {"min": 0.000001, "max": 0.001},  # Learning rate range
}

default_config = {
    "training": {
        "num_epochs": 3,
        "batch_size": 2,
        "learning_rate": 0.001,
        "start_idx": 0,
        "end_idx": 100
    }
}

def _validate_number_input(value, is_int=True, min_val=None, max_val=None):
        if not value.strip():
            messagebox.showerror("Error", "Value cannot be empty")
            return None
        
        try:
            if is_int:
                num_value = int(value)
                if not float(value).is_integer():  # Check if it is actually an integer
                    messagebox.showerror("Error", "Value must be a whole number")
                    return None
            else:
                num_value = float(value)
            
            if (min_val is not None and num_value < min_val) or (max_val is not None and num_value > max_val): 
                messagebox.showerror("Error", f"Invalid indices")
                return None
            
            return num_value
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
            return None

def validate_dataset_indices(start_idx_var, end_idx_var):
    
    # Validate start index
    start_idx = _validate_number_input(start_idx_var, is_int=True, min_val=0)
    if start_idx is None:
        return None
    
    # Validate end index
    end_idx = _validate_number_input(end_idx_var, is_int=True, min_val=start_idx + 1)
    if end_idx is None:
        return None
    
    if start_idx >= end_idx:
        messagebox.showerror("Error", f"Start index ({start_idx}) must be less than end index ({end_idx})")
        return None
    
    if end_idx - start_idx == 0:
        messagebox.showerror("Error", f"Invalid Indices")
        return None
    
    return start_idx, end_idx

def validate_parameters(param, value):
    if not value.strip():
        messagebox.showerror("Error", f"{param} cannot be empty")
        return None

    try:
        limits = param_limits[param]
        
        # Determine whether the parameter should be an integer or float
        is_int = param in ["num_epochs", "batch_size"] 

        num_value = _validate_number_input(
            value,
            is_int=is_int,  # learning_rate will be validated as a float, others as ints
            min_val=limits["min"],
            max_val=limits["max"]
        )

        if num_value is None:
            return None
        
        return num_value

    except Exception as e:
        messagebox.showerror("Error", f"Invalid value for {param}: {str(e)}")
        return None

def browse_file(file_type, path_var):
    if file_type == "dataset":
        filetypes = (
            ('JSON files', '.json'),
            ('JSONL files', '.jsonl'),
            ('CSV files', '.csv'),
            ('Text files', '.txt')
        )
        title = 'Select Dataset File'
    else:  # model
        filetypes = (('All files', '*.*'),)
        title = 'Select Model Directory'
        
    if file_type == "model":
        # Look for directories
        filename = filedialog.askdirectory(title=title)
    else:
        # Look for files
        filename = filedialog.askopenfilename(title=title, filetypes=filetypes)
        
    if not filename:
        return None
    
    # Validation logic
    if not filename.strip():
        messagebox.showerror("Error", f"Please select a {file_type} {'file' if file_type == 'dataset' else 'directory'}")
        return None
        
    if not os.path.exists(filename):
        messagebox.showerror("Error", f"{file_type.capitalize()} {'file' if file_type == 'dataset' else 'directory'} does not exist")
        return None

    path_var.set(filename)
        
    return filename
