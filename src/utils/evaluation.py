import torch
import nltk
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from pathlib import Path
from .data_loader import load_dataset
from .eval_scores import ScoreCalculator, prevent_download, setup_nltk_paths

class Evaluator:
    def __init__(self, model_path):
        self.model_path = Path(model_path)
        # Use CPU
        self.device = torch.device('cpu')
        
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

        self.max_input_length = 512
        self.max_output_length = 128
        self.min_output_length = 30
        
        # Dict to store scores
        self.scores = {
            'rouge1': [],
            'rouge2': [],
            'rougeL': [],
            'bleu': [],
            'meteor': [],
            'bert_f1': []
        }
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
                    
                    # Calculate all metrics with safe defaults using ScoreCalculator
                    rouge_scores = self.score_calculator.rouge_calculator(reference, generated_summary)
                    bleu_score = self.score_calculator.bleu_calculator(reference, generated_summary)
                    meteor_score = self.score_calculator.meteor_calculator(reference, generated_summary)
                    bert_scores = self.score_calculator.bertscore_calculator(reference, generated_summary)
                    
                    # Combine all scores
                    sample_scores = {
                        'rouge1': rouge_scores['rouge1'],
                        'rouge2': rouge_scores['rouge2'],
                        'rougeL': rouge_scores['rougeL'],
                        'bleu': bleu_score,
                        'meteor': meteor_score,
                        'bert_f1': bert_scores['f1']
                    }
                    
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
            
            return final_scores
            
        except Exception as e:
            print(f"Evaluation error: {str(e)}")
            raise

    def load_dataset(self, data_path, start_idx, end_idx):
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
            return ""