import tkinter as tk
from tkinter import ttk
import threading
from utils.fine_tuning import FineTuner
from components.finetune_form import FinetuneForm

class FinetunePage:
    def __init__(self, root):
        # Initialize the main window
        self.root = root
        self.setup_page()
        
    def setup_page(self):
        # Create main container with light blue background
        self.container = tk.Frame(self.root, bg="#EBF3FF")
        self.container.grid(row=1, column=1, sticky="nsew")
        self.container.grid_columnconfigure(0, weight=1)
        
        # Create white content frame
        content = tk.Frame(self.container, bg="white")
        content.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)
        content.grid_columnconfigure(0, weight=1)
        
        tk.Label(
            content,
            text="Fine-tune Model",
            font=("SF Pro Display", 24),
            bg="white"
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(20,10))
        
        ttk.Separator(content, orient="horizontal").grid(row=1, column=0, sticky="ew", padx=20)
        
        # Initialize the form component
        self.form = FinetuneForm(content, self.handle_start_finetuning)
        
    def run_finetuning(self, config, dataset_path, model_path, start_idx, end_idx):
        try:         
            # Initialize fine-tuning process
            self.form.update_status("Loading model...")
            fine_tuner = FineTuner(model_path, config)
            
            # Load dataset
            self.form.update_status(f"Loading dataset")
            try:
                train_data = fine_tuner.load_dataset(dataset_path,start_idx,end_idx)
                self.form.update_status(f"Successfully loaded {len(train_data)} samples from index range {start_idx}-{end_idx}")
            except ValueError as e:
                raise ValueError(f"Failed to load dataset: {str(e)}")
            
            self.form.update_status("Starting fine-tuning...")
            
            # Define progress callback function for actual training progress
            def progress_callback(progress_info):
                epoch = progress_info['epoch']
                total_epochs = progress_info['total_epochs']
                batch = progress_info['batch']
                total_batches = progress_info['total_batches']
                loss = progress_info['loss']  # This is now the actual training loss
                
                # Update status with real training progress
                status_text = f"Epoch {epoch}/{total_epochs} - Batch {batch}/{total_batches} - Loss: {loss:.4f}"
                self.root.after(0, lambda: self.form.update_status(status_text))
            
            output_directory = fine_tuner.fine_tune(
                train_data,
                progress_callback=progress_callback
            )
            
            # Update status on completion
            self.root.after(0, lambda: self.form.update_status(f"Fine-tuning complete! Model saved to: {output_directory}"))
            self.root.after(0, lambda: self.form.start_btn.config(state="normal"))
            
        except Exception as e:
            # Handle any errors during fine-tuning
            self.root.after(0, lambda: self.form.update_status(f"Error: {str(e)}", is_error=True))
            self.root.after(0, lambda: self.form.start_btn.config(state="normal"))
            
    def handle_start_finetuning(self, config, dataset_path, model_path, start_idx, end_idx):
        # Start fine-tuning in a separate thread
        thread = threading.Thread(
            target=self.run_finetuning,
            args=(config, dataset_path, model_path, start_idx, end_idx),
            daemon=True
        )
        thread.start()