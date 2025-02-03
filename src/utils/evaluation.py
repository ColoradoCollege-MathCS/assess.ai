import torch
<<<<<<< HEAD
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from rouge_score import rouge_scorer
from pathlib import Path
from .data_loader import load_dataset
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
=======
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from rouge_score import rouge_scorer
from pathlib import Path
from .data_loader import load_dataset

>>>>>>> a0610ba1835c74dcf76d954652a1a43adb5e15a1

"""
ROUGE-1: Measures unigram (single word) overlap
For example, if the target text has "the cat sat" and the generated text has "the cat ran", it counts matches of individual words ("the" and "cat" match)
"""

class Evaluator:
    def __init__(self, model_path):
        self.model_path = Path(model_path)
        # Use CPU
        self.device = torch.device('cpu')
        
<<<<<<< HEAD
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(
=======
        self.tokenizer = PegasusTokenizer.from_pretrained(self.model_path)
        self.model = PegasusForConditionalGeneration.from_pretrained(
>>>>>>> a0610ba1835c74dcf76d954652a1a43adb5e15a1
            self.model_path,
            low_cpu_mem_usage=True
        )
        self.model.to(self.device)
<<<<<<< HEAD
        self.model.to(self.device)
=======
>>>>>>> a0610ba1835c74dcf76d954652a1a43adb5e15a1
        
        # use_stemmer=True means the ROUGE scorer will use word stemming ("running" -> "run")
        self.scorer = rouge_scorer.RougeScorer(['rouge1'], use_stemmer=True)

        self.max_input_length = 512
        self.max_output_length = 128
        self.min_output_length = 30
        
<<<<<<< HEAD
        # Initialize plotting variables
        self.figure = None
        self.ax = None
        self.canvas = None
        self.rouge_scores = []
        self.sample_indices = []
        
    def setup_plot(self, parent_widget):
        # Initialize the matplotlib plot
        self.figure = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, master=parent_widget)
        self.canvas.get_tk_widget().grid(row=4, column=0, columnspan=3, padx=20, pady=10, sticky="nsew")
        
        # Setup initial plot
        self.ax.set_title('ROUGE-1 Scores Over Time')
        self.ax.set_xlabel('Sample Number')
        self.ax.set_ylabel('ROUGE-1 Score')
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.ax.xaxis.set_major_locator
        self.ax.xaxis.set_major_locator(plt.MaxNLocator(integer=True))
        self.figure.tight_layout()
        
    def update_plot(self, current_sample, rouge1_score):
        if not self.figure or not self.ax:
            return
            
        self.rouge_scores.append(rouge1_score)
        self.sample_indices.append(current_sample)
        
        # Clear and redraw
        self.ax.clear()
        
        # Plot scores
        self.ax.plot(self.sample_indices, self.rouge_scores, 'b-', label='ROUGE-1')

        self.ax.xaxis.set_major_locator(plt.MultipleLocator(base=1.0))
        
        # Reset plot styling
        self.ax.set_title('ROUGE-1 Scores Over Time')
        self.ax.set_xlabel('Sample Number')
        self.ax.set_ylabel('ROUGE-1 Score')
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.ax.legend()
        self.figure.tight_layout()
        
        # Refresh canvas
        self.canvas.draw()
        
    def clear_plot(self):
        if not self.ax:
            return
            
        self.rouge_scores = []
        self.sample_indices = []
        self.ax.clear()
        self.ax.set_title('ROUGE-1 Scores Over Time')
        self.ax.set_xlabel('Sample Number')
        self.ax.set_ylabel('ROUGE-1 Score')
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.figure.tight_layout()
        self.canvas.draw()
        
    def load_dataset(self, data_path, start_idx, end_idx):
=======
    def load_dataset(self, data_path,start_idx,end_idx):
>>>>>>> a0610ba1835c74dcf76d954652a1a43adb5e15a1
        # Load dataset with dataset validation
        return load_dataset(data_path, start_idx=start_idx, end_idx=end_idx)
        
    def generate_summary(self, text):
        try:
            if not text:
                return ""
                
            # Tokenize with padding and truncation
            inputs = self.tokenizer(
                text,
                max_length=self.max_input_length,
                truncation=True,
                padding='max_length',
                return_tensors="pt"
            )
            
            # Generate summary
            try:
                with torch.no_grad():
                    summary_ids = self.model.generate(
                        inputs["input_ids"].to(self.device),
                        max_length=self.max_output_length,
                        min_length=self.min_output_length,
                        num_beams=4,
                        length_penalty=2.0,
                        pad_token_id=self.tokenizer.pad_token_id,
                        bos_token_id=self.tokenizer.bos_token_id,
                        eos_token_id=self.tokenizer.eos_token_id
                    )
            except RuntimeError as e:
                if "out of memory" in str(e):
                    torch.cuda.empty_cache()
                    return ""
                raise
                
            # Decode summary
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            return summary.strip()
            
        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            return ""
        
    def calculate_rouge_scores(self, reference, candidate):
        # Reference = Target, Candidate = LLM generated summary. Use this terminology here for good practice
        # Return F1 scores of
        try:
            if not reference or not candidate:
                return None
            scores = self.scorer.score(reference, candidate)
            return {
                'rouge1': scores['rouge1'].fmeasure, # # This is the F1 score
            }
        except Exception as e:
            print(f"Error calculating ROUGE scores: {str(e)}")
            return None
        
    def evaluate(self, test_data, progress_callback=None):
        try:
            if not test_data:
                raise ValueError("Test data is empty")
                
            total_samples = len(test_data)
<<<<<<< HEAD
            successful_samples = 0
=======
            successful_samples = 0 # Store this to report how many samples were processed
>>>>>>> a0610ba1835c74dcf76d954652a1a43adb5e15a1
            rouge_scores = []
            
            for idx, item in enumerate(test_data):
                try:
                    generated_summary = self.generate_summary(item.get('input_text', ''))
                    if not generated_summary:
<<<<<<< HEAD
                        raise ValueError(f"Failed to generate summary for sample {idx}")
                        
=======
                        raise ValueError(f"Failed to generate summary for sample {idx}. Summary is empty or invalid.")
                    # Calculate ROUGE scores between generated and target summaries
>>>>>>> a0610ba1835c74dcf76d954652a1a43adb5e15a1
                    scores = self.calculate_rouge_scores(
                        item.get('target_text', ''),
                        generated_summary
                    )
                    
                    if scores:
                        rouge_scores.append(scores)
                        successful_samples += 1
                        
<<<<<<< HEAD
                        # Update progress and plot
                        if progress_callback:
=======
                        # Update progress
                        if progress_callback:
                            avg_scores = {
                                'rouge1': sum(s['rouge1'] for s in rouge_scores) / len(rouge_scores)
                            }
>>>>>>> a0610ba1835c74dcf76d954652a1a43adb5e15a1
                            
                            progress = {
                                'current': idx + 1,
                                'total': total_samples,
                                'successful': successful_samples,
<<<<<<< HEAD
                                'rouge1': scores['rouge1']  # Use current score instead of average
=======
                                'rouge1': avg_scores['rouge1']
>>>>>>> a0610ba1835c74dcf76d954652a1a43adb5e15a1
                            }
                            progress_callback(progress)
                            
                except Exception as e:
                    print(f"Error processing sample {idx}: {str(e)}")
                    continue
                    
            if not rouge_scores:
                raise ValueError("No valid samples were processed")
                
<<<<<<< HEAD
=======
            # Calculate final average scores
>>>>>>> a0610ba1835c74dcf76d954652a1a43adb5e15a1
            final_scores = {
                'rouge1': sum(s['rouge1'] for s in rouge_scores) / len(rouge_scores),
                'processed_samples': successful_samples,
                'total_samples': total_samples
            }
            
            return final_scores
            
        except Exception as e:
            print(f"Evaluation error: {str(e)}")
<<<<<<< HEAD
            raise

"""
For AutoModelForSeq2SeqLM and AutoTokenizer to work properly with a model, the model directory must contain these essential files:

config.json - Contains model architecture and configuration details
pytorch_model.bin or weights.safetensors - The actual model weights
tokenizer.json - Contains tokenizer configuration
special_tokens_map.json - Defines special tokens used by the model
tokenizer_config.json - Additional tokenizer configuration

"""
=======
            raise
>>>>>>> a0610ba1835c74dcf76d954652a1a43adb5e15a1
