import torch
<<<<<<< HEAD
<<<<<<< HEAD
=======
import nltk
>>>>>>> 18b5a80842d2d547646a5a0f221bdf64cdc5890d
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from pathlib import Path
from .data_loader import load_dataset
<<<<<<< HEAD
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
=======
from .eval_scores import ScoreCalculator, prevent_download, setup_nltk_paths
>>>>>>> 18b5a80842d2d547646a5a0f221bdf64cdc5890d

class Evaluator:
    def __init__(self, model_path, use_geval=True):
        self.model_path = Path(model_path)
        self.use_geval = use_geval
        # Use CPU
        self.device = torch.device('cpu')
        
<<<<<<< HEAD
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
=======
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(
                self.model_path,
                low_cpu_mem_usage=True
            )
            self.model.to(self.device)
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            raise

        # Initialize score calculator
        self.score_calculator = ScoreCalculator()
>>>>>>> 18b5a80842d2d547646a5a0f221bdf64cdc5890d

        self.max_input_length = 512
        self.max_output_length = 128
        self.min_output_length = 30
        
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        # Initialize plotting variables
        self.figure = None
        self.ax = None
        self.canvas = None
        self.rouge_scores = []
=======
        # Dict to store scores
=======
        # Dictionary to store scores - include G-EVAL metrics only if enabled
>>>>>>> d56d1de2de58700d2f6094e5ed4f1e5a0c3f81cc
        self.scores = {
            'rouge1': [],
            'rouge2': [],
            'rougeL': [],
            'bleu': [],
            'meteor': [],
            'bert_f1': [],
        }
<<<<<<< HEAD
>>>>>>> 18b5a80842d2d547646a5a0f221bdf64cdc5890d
=======
        if self.use_geval:
            self.scores.update({
                'coherence': [],
                'consistency': [],
                'fluency': [],
                'relevance': []
            })
>>>>>>> d56d1de2de58700d2f6094e5ed4f1e5a0c3f81cc
        self.sample_indices = []

    def evaluate(self, test_data, progress_callback=None):
        try:
            if not test_data:
                raise ValueError("Test data is empty")
                
            total_samples = len(test_data)
            successful_samples = 0
            all_scores = []
            
            for idx, item in enumerate(test_data):
                try:
                    generated_summary = self.generate_summary(item.get('input_text', ''))
                    if not generated_summary:
                        print(f"Empty generated summary for sample {idx}")
                        continue
                    
                    reference = item.get('target_text', '')
                    if not reference:
                        print(f"Empty reference for sample {idx}")
                        continue
                    
                    # Calculate traditional metrics
                    rouge_scores = self.score_calculator.rouge_calculator(reference, generated_summary)
                    bleu_score = self.score_calculator.bleu_calculator(reference, generated_summary)
                    meteor_score = self.score_calculator.meteor_calculator(reference, generated_summary)
                    bert_scores = self.score_calculator.bertscore_calculator(reference, generated_summary)
                    
                    # Initialize sample scores with traditional metrics
                    sample_scores = {
                        'rouge1': rouge_scores['rouge1'],
                        'rouge2': rouge_scores['rouge2'],
                        'rougeL': rouge_scores['rougeL'],
                        'bleu': bleu_score,
                        'meteor': meteor_score,
                        'bert_f1': bert_scores['f1']
                    }
                    
                    # Add G-EVAL metrics if enabled
                    if self.use_geval:
                        g_eval_scores = self.score_calculator.g_eval(reference, generated_summary)
                        sample_scores.update({
                            'coherence': g_eval_scores.get('coherence', {}).get('average', 0),
                            'consistency': g_eval_scores.get('consistency', {}).get('average', 0),
                            'fluency': g_eval_scores.get('fluency', {}).get('average', 0),
                            'relevance': g_eval_scores.get('relevance', {}).get('average', 0)
                        })
                    
                    # Store scores
                    all_scores.append(sample_scores)
                    successful_samples += 1
                    
                    # Update progress
                    if progress_callback:
                        progress = {
                            'current': idx + 1,
                            'total': total_samples,
                            'successful': successful_samples,
                            'scores': sample_scores
                        }
                        progress_callback(progress)
                        
                except Exception as e:
                    print(f"Error processing sample {idx}: {str(e)}")
                    continue
                    
            if not all_scores:
                raise ValueError("No valid samples were processed")
                
            # Calculate final average scores
            final_scores = {
                metric: sum(scores[metric] for scores in all_scores) / len(all_scores)
                for metric in all_scores[0].keys()
            }
            final_scores.update({
                'processed_samples': successful_samples,
                'total_samples': total_samples
            })
            
            # Write results to file
            data_file = open("evaluation_results.txt", "a")
            try:
                data_file.write("Here are the metrics of your summarized dataset versus the original copy. A score closer to 1.0 is perfect and the worst is 0.0." + "\n")
                data_file.write(f"Processed Samples: {successful_samples}\n")
                data_file.write(f"Average Scores:\n")
                data_file.write(f"Bleu Score: {final_scores['bleu']}\n")
                data_file.write(f"Rouge Scores:\n")
                data_file.write(f"  ROUGE-1: {final_scores['rouge1']}\n")
                data_file.write(f"  ROUGE-2: {final_scores['rouge2']}\n")
                data_file.write(f"  ROUGE-L: {final_scores['rougeL']}\n")
                data_file.write(f"Meteor Score: {final_scores['meteor']}\n")
                data_file.write(f"BERTScore F1: {final_scores['bert_f1']}\n")
                
                if self.use_geval:
                    data_file.write(f"G-Evaluation Scores:\n")
                    data_file.write(f"  Coherence: {final_scores.get('coherence', 0)}\n")
                    data_file.write(f"  Consistency: {final_scores.get('consistency', 0)}\n")
                    data_file.write(f"  Fluency: {final_scores.get('fluency', 0)}\n")
                    data_file.write(f"  Relevance: {final_scores.get('relevance', 0)}\n")

            except Exception as e:
                print(f"Unable to write in file: {e}")
            finally:
                data_file.close()
            
            return final_scores
            
        except Exception as e:
            print(f"Evaluation error: {str(e)}")
            raise

    def load_dataset(self, data_path, start_idx, end_idx):
<<<<<<< HEAD
=======
    def load_dataset(self, data_path,start_idx,end_idx):
>>>>>>> a0610ba1835c74dcf76d954652a1a43adb5e15a1
        # Load dataset with dataset validation
=======
>>>>>>> 18b5a80842d2d547646a5a0f221bdf64cdc5890d
        return load_dataset(data_path, start_idx=start_idx, end_idx=end_idx)
        
    def generate_summary(self, text):
        try:
            if not text:
                return ""
                
            inputs = self.tokenizer(
                text,
                max_length=self.max_input_length,
                truncation=True,
                padding='max_length',
                return_tensors="pt"
            )
            
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
                raise ValueError(f"Error: {str(e)}")
                
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            return summary.strip()
            
        except Exception as e:
            print(f"Error generating summary: {str(e)}")
<<<<<<< HEAD
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
=======
            return ""
>>>>>>> 18b5a80842d2d547646a5a0f221bdf64cdc5890d
