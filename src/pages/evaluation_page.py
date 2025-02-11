import tkinter as tk
from tkinter import ttk
import threading
from pathlib import Path
from utils.evaluation import Evaluator
from components.evaluation_form import EvaluationForm

class EvaluationPage:
    def __init__(self, root):
        self.root = root
        # Run method right below 
        self.setup_page()
        
    def setup_page(self):
        self.container = tk.Frame(self.root, bg="#EBF3FF")
        self.container.grid(row=1, column=1, sticky="nsew")
        self.container.grid_columnconfigure(0, weight=1)
        
        content = tk.Frame(self.container, bg="white")
        content.grid(row=0, column=0, sticky="nsew", padx=30, pady=30)
        content.grid_columnconfigure(0, weight=1)
        
        tk.Label(
            content,
            text="Evaluate Model",
            font=("SF Pro Display", 24),
            bg="white"
        ).grid(row=0, column=0, sticky="w", padx=20, pady=(20,10))
        
        ttk.Separator(content, orient="horizontal").grid(row=1, column=0, sticky="ew", padx=20)
        
        self.form = EvaluationForm(content, self.handle_start_evaluation)
        
    def run_evaluation(self, dataset_path, model_path, start_idx, end_idx):
        try:
            # Initialize evaluator
            self.form.update_status("Loading model...")
            evaluator = Evaluator(model_path)
            
            # Load dataset with specified range
            self.form.update_status(f"Loading dataset (indices {start_idx}-{end_idx})...")
            try:
                test_data = evaluator.load_dataset(dataset_path, start_idx, end_idx)
                self.form.update_status(f"Successfully loaded {len(test_data)} samples from index range {start_idx}-{end_idx}")
            except ValueError as e:
                raise ValueError(f"Failed to load dataset: {str(e)}")
            
            self.form.update_status("Starting evaluation...")
            
            # Define progress callback
            def progress_callback(progress_info):
                current = progress_info['current']
                total = progress_info['total']
                successful = progress_info['successful']
                rouge1 = progress_info['rouge1']
                
                # Update status with current progress
                status_text = (
                    f"Evaluating samples {start_idx}-{end_idx}\n"
                    f"Current sample: {start_idx + current}/{end_idx} "
                    f"(Processed {successful} successfully)\n"
                    f"Current ROUGE-1: {rouge1:.4f}\n"
                )
                self.root.after(0, lambda: self.form.update_status(status_text))
            
            # Run evaluation
            final_scores = evaluator.evaluate(
                test_data,
                progress_callback=progress_callback
            )
            
            # Update status with final scores
            final_status = (
                f"\nEvaluation complete for samples {start_idx}-{end_idx}!\n"
                f"Successfully processed {final_scores['processed_samples']} out of {final_scores['total_samples']} samples\n"
                f"Final ROUGE-1: {final_scores['rouge1']:.4f}\n"
            )
            self.root.after(0, lambda: self.form.update_status(final_status))
            self.root.after(0, lambda: self.form.start_btn.config(state="normal"))
            
        except Exception as e:
            # Handle any errors during evaluation
            self.root.after(0, lambda: self.form.update_status(f"Error: {str(e)}", is_error=True))
            self.root.after(0, lambda: self.form.start_btn.config(state="normal"))
            
    def handle_start_evaluation(self, dataset_path, model_path, start_idx, end_idx):
        # Start evaluation in a separate thread
        thread = threading.Thread(
            target=self.run_evaluation,
            # Passes parameters needed to run evaluation
            args=(dataset_path, model_path, start_idx, end_idx),
            daemon=True
        )
        thread.start()
