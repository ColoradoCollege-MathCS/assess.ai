import tkinter as tk
from tkinter import ttk
import threading
from utils.evaluation import Evaluator
from components.evaluation_form import EvaluationForm
from components.graph import EvaluationVisualizer

class EvaluationPage:
    def __init__(self, root):
        self.root = root
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
        
        # Initialize visualizer after form setup
        self.visualizer = EvaluationVisualizer(content)
        
    def format_metrics(self, scores):
        return (
            f"ROUGE-1: {scores.get('rouge1', 0):.4f}, "
            f"ROUGE-2: {scores.get('rouge2', 0):.4f}, "
            f"ROUGE-L: {scores.get('rougeL', 0):.4f}\n"
            f"BLEU: {scores.get('bleu', 0):.4f}, "
            f"METEOR: {scores.get('meteor', 0):.4f}, "
            f"BERTScore F1: {scores.get('bert_f1', 0):.4f}\n"
            f"G-Eval Metrics:\n"
            f"  Coherence: {scores.get('coherence', 0):.4f}\n"
            f"  Consistency: {scores.get('consistency', 0):.4f}\n"
            f"  Fluency: {scores.get('fluency', 0):.4f}\n"
            f"  Relevance: {scores.get('relevance', 0):.4f}"
        )
        
    def run_evaluation(self, dataset_path, model_path, start_idx, end_idx):
        try:
            # Initialize evaluator
            self.form.update_status("Loading model...")
            evaluator = Evaluator(model_path)
            
            self.form.evaluator = evaluator
            
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
                scores = progress_info.get('scores', {})
                
                # Update status with current progress and all metrics
                status_text = (
                    f"Current sample: {start_idx + current}/{end_idx} "
                    f"(Processed {successful} successfully)"
                    f"\n{self.format_metrics(scores)}\n"
                )
                self.root.after(0, lambda: self.form.update_status(status_text))
                # Update graph
                self.root.after(0, lambda: self.visualizer.update_plots(scores))
            # Run evaluation
            final_scores = evaluator.evaluate(
                test_data,
                progress_callback=progress_callback
            )
            
            # Update status with final scores
            final_status = (
                f"\nEvaluation complete for samples {start_idx}-{end_idx}!\n"
                f"Successfully processed {final_scores['processed_samples']} out of {final_scores['total_samples']} samples\n\n"
                f"Final Metrics:\n{self.format_metrics(final_scores)}\n"
            )
            self.root.after(0, lambda: self.form.update_status(final_status))
            self.root.after(0, lambda: self.form.start_btn.config(state="normal"))
            
            # Show final radar chart
            self.root.after(0, lambda: self.visualizer.plot_final_radar(final_scores))
            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            self.root.after(0, lambda: self.form.update_status(error_msg, is_error=True))
            self.root.after(0, lambda: self.form.start_btn.config(state="normal"))
            
    def handle_start_evaluation(self, dataset_path, model_path, start_idx, end_idx):
        # Clear previous plots
        self.visualizer.clear_plots()
        
        # Disable start button while evaluation is running
        self.form.start_btn.config(state="disabled")
        
        # Clear previous status
        self.form.update_status("")
        
        # Start evaluation in a separate thread
        thread = threading.Thread(
            target=self.run_evaluation,
            args=(dataset_path, model_path, start_idx, end_idx),
            daemon=True
        )
        thread.start()