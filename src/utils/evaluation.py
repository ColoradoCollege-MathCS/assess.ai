import torch
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from rouge_score import rouge_scorer
from pathlib import Path
from .data_loader import load_dataset


"""
ROUGE-1: Measures unigram (single word) overlap
For example, if the target text has "the cat sat" and the generated text has "the cat ran", it counts matches of individual words ("the" and "cat" match)
"""

class Evaluator:
    def __init__(self, model_path):
        self.model_path = Path(model_path)
        # Use CPU
        self.device = torch.device('cpu')
        
        self.tokenizer = PegasusTokenizer.from_pretrained(self.model_path)
        self.model = PegasusForConditionalGeneration.from_pretrained(
            self.model_path,
            low_cpu_mem_usage=True
        )
        self.model.to(self.device)
        
        # use_stemmer=True means the ROUGE scorer will use word stemming ("running" -> "run")
        self.scorer = rouge_scorer.RougeScorer(['rouge1'], use_stemmer=True)

        self.max_input_length = 512
        self.max_output_length = 128
        self.min_output_length = 30
        
    def load_dataset(self, data_path,start_idx,end_idx):
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
            successful_samples = 0 # Store this to report how many samples were processed
            rouge_scores = []
            
            for idx, item in enumerate(test_data):
                try:
                    generated_summary = self.generate_summary(item.get('input_text', ''))
                    if not generated_summary:
                        raise ValueError(f"Failed to generate summary for sample {idx}. Summary is empty or invalid.")
                    # Calculate ROUGE scores between generated and target summaries
                    scores = self.calculate_rouge_scores(
                        item.get('target_text', ''),
                        generated_summary
                    )
                    
                    if scores:
                        rouge_scores.append(scores)
                        successful_samples += 1
                        
                        # Update progress
                        if progress_callback:
                            avg_scores = {
                                'rouge1': sum(s['rouge1'] for s in rouge_scores) / len(rouge_scores)
                            }
                            
                            progress = {
                                'current': idx + 1,
                                'total': total_samples,
                                'successful': successful_samples,
                                'rouge1': avg_scores['rouge1']
                            }
                            progress_callback(progress)
                            
                except Exception as e:
                    print(f"Error processing sample {idx}: {str(e)}")
                    continue
                    
            if not rouge_scores:
                raise ValueError("No valid samples were processed")
                
            # Calculate final average scores
            final_scores = {
                'rouge1': sum(s['rouge1'] for s in rouge_scores) / len(rouge_scores),
                'processed_samples': successful_samples,
                'total_samples': total_samples
            }
            
            return final_scores
            
        except Exception as e:
            print(f"Evaluation error: {str(e)}")
            raise