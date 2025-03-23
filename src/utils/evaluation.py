import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from pathlib import Path
from .data_loader import load_dataset
from .eval_scores import ScoreCalculator

class Evaluator:
    def __init__(self, model_path, use_geval=True):
        self.model_path = Path(model_path)
        self.use_geval = use_geval
        # Use CPU
        self.device = torch.device('cpu')
        
        # Initialize log storage
        self.progress_logs = []
        
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
        
        # Dictionary to store scores - include G-EVAL metrics only if enabled
        self.scores = {
            'rouge1': [],
            'rouge2': [],
            'rougeL': [],
            'bleu': [],
            'meteor': [],
            'bert_f1': [],
        }
        if self.use_geval:
            self.scores.update({
                'coherence': [],
                'consistency': [],
                'fluency': [],
                'relevance': []
            })
        self.sample_indices = []

    def save_logs(self, log_dir, final_scores, successful_samples, total_samples, custom_folder_name=None):
        if custom_folder_name and custom_folder_name.strip():
            # Sanitize folder name to remove invalid characters
            sanitized_name = "".join(c for c in custom_folder_name if c.isalnum() or c in [' ', '_', '-']).strip()
            log_dir = Path("../eval_files") / sanitized_name
            log_dir.mkdir(parents=True, exist_ok=True)
        # Create the log file
        log_file = log_dir / "logs.txt"
        
        with open(log_file, "w", encoding="utf-8") as f:
            # Write progress logs first
            f.write("=== EVALUATION PROGRESS LOGS ===\n\n")
            for log in self.progress_logs:
                f.write(f"{log}\n")
            
            # Write final evaluation results
            f.write("\n=== FINAL EVALUATION RESULTS ===\n\n")
            f.write("Here are the metrics of your summarized dataset versus the original copy. A score closer to 1.0 is perfect and the worst is 0.0.\n")
            f.write(f"Processed Samples: {successful_samples}\n")
            f.write(f"Total Samples: {total_samples}\n\n")
            f.write(f"Average Scores:\n")
            f.write(f"Bleu Score: {final_scores['bleu']}\n")
            f.write(f"Rouge Scores:\n")
            f.write(f"  ROUGE-1: {final_scores['rouge1']}\n")
            f.write(f"  ROUGE-2: {final_scores['rouge2']}\n")
            f.write(f"  ROUGE-L: {final_scores['rougeL']}\n")
            f.write(f"Meteor Score: {final_scores['meteor']}\n")
            f.write(f"BERTScore F1: {final_scores['bert_f1']}\n")
            
            if self.use_geval:
                f.write(f"G-Evaluation Scores:\n")
                f.write(f"  Coherence: {final_scores.get('coherence', 0)}\n")
                f.write(f"  Consistency: {final_scores.get('consistency', 0)}\n")
                f.write(f"  Fluency: {final_scores.get('fluency', 0)}\n")
                f.write(f"  Relevance: {final_scores.get('relevance', 0)}\n")

    def evaluate(self, test_data, progress_callback=None):
        try:
            if not test_data:
                raise ValueError("Test data is empty")
                
            total_samples = len(test_data)
            successful_samples = 0
            all_scores = []
            
            # Clear previous progress logs
            self.progress_logs = []
            
            for idx, item in enumerate(test_data):
                try:
                    generated_summary = self.generate_summary(item.get('input_text', ''))
                    if not generated_summary:
                        print(f"Empty generated summary for sample {idx}")
                        continue
                    
                    reference = item.get('target_text', '')
                    if not reference:
                        print(f"Empty reference for sample {idx}")
                        raise 
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
                    
                    # Update progress and store log
                    if progress_callback:
                        progress = {
                            'current': idx + 1,
                            'total': total_samples,
                            'successful': successful_samples,
                            'scores': sample_scores
                        }
                        progress_callback(progress)
                        
                        # Store progress log
                        log_msg = [
                            f"Sample {idx + 1}/{total_samples} (Successful: {successful_samples})",
                            f"Traditional Metrics:",
                            f"  ROUGE-1: {sample_scores['rouge1']:.4f}",
                            f"  ROUGE-2: {sample_scores['rouge2']:.4f}",
                            f"  ROUGE-L: {sample_scores['rougeL']:.4f}",
                            f"  BLEU: {sample_scores['bleu']:.4f}",
                            f"  METEOR: {sample_scores['meteor']:.4f}",
                            f"  BERTScore F1: {sample_scores['bert_f1']:.4f}"
                        ]
                        
                        if self.use_geval:
                            log_msg.extend([
                                f"G-Eval Metrics:",
                                f"  Coherence: {sample_scores.get('coherence', 0):.4f}",
                                f"  Consistency: {sample_scores.get('consistency', 0):.4f}",
                                f"  Fluency: {sample_scores.get('fluency', 0):.4f}",
                                f"  Relevance: {sample_scores.get('relevance', 0):.4f}"
                            ])
                        
                        self.progress_logs.extend(log_msg)
                        self.progress_logs.append("")  # Add blank line between samples
                        
                except Exception as e:
                    print(f"Error processing sample {idx}: {str(e)}")
                    raise
                    
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