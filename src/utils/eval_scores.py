import os
import nltk
from rouge_score import rouge_scorer
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import evaluate
from bert_score import BERTScorer
from nltk.data import path as nltk_data_path
from llama_cpp import Llama
import statistics
import logging
import sys
from contextlib import contextmanager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
llama_logger = logging.getLogger("llama_cpp")
llama_logger.setLevel(logging.ERROR)

def setup_nltk_paths():
    # Clear all default paths
    nltk_data_path.clear()
    
    # Get current file's directory path
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Get parent directory (one level up)
    parent_dir = os.path.dirname(current_dir)
    
    # Set up paths for NLTK data directories
    nltk_data_dir = os.path.join(parent_dir, 'nltk_data')
    punkt_dir = os.path.join(nltk_data_dir, 'tokenizers', 'punkt')
    
    # Add our paths
    nltk_data_path.append(nltk_data_dir)
    nltk_data_path.append(punkt_dir)
    
    # Set environment variable
    os.environ['NLTK_DATA'] = nltk_data_dir

# Prevent NLTK from downloading
def prevent_download(*args, **kwargs):
    print(f"NLTK download attempted (and prevented) for: {args}")
    return

@contextmanager
def suppress_stdout_stderr():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = devnull
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

class ScoreCalculator:
    def __init__(self):
        # Initialize traditional scorers
        self.rouge_scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        self.bert_scorer = BERTScorer(model_type='bert-base-uncased')
        self.meteor = evaluate.load('meteor')
        self.smoothing = SmoothingFunction().method1

        # Get current file's directory path (utils)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        geval_dir = os.path.join(current_dir, '..', 'geval')
        
        # Initialize Mistral model
        try:
            with suppress_stdout_stderr():
                model_path = os.path.join(geval_dir, "mistral-7b-instruct-v0.2.Q4_K_M.gguf")
                self.model = Llama(
                    model_path=model_path,
                    n_ctx=4096,
                    n_threads=4,
                    verbose=False
                )
                # Load prompt templates from geval directory
                self.prompts = {}
                for metric in ['coherence', 'consistency', 'fluency', 'relevance']:
                    prompt_path = os.path.join(geval_dir, f"{metric[0:3]}_detailed.txt")
                    with open(prompt_path, "r") as f:
                        self.prompts[metric] = f.read()
        except Exception as e:
            logger.error(f"Mistral initialization error: {str(e)}")
            raise

    def rouge_calculator(self, reference, candidate):
        scores = self.rouge_scorer.score(reference, candidate)
        return {
            'rouge1': scores['rouge1'].fmeasure if scores['rouge1'].fmeasure is not None else 0,
            'rouge2': scores['rouge2'].fmeasure if scores['rouge2'].fmeasure is not None else 0,
            'rougeL': scores['rougeL'].fmeasure if scores['rougeL'].fmeasure is not None else 0
        }

    def bleu_calculator(self, reference, candidate):
        weights = (0.25, 0.25, 0, 0)
        reference_tokens = reference.split()
        candidate_tokens = candidate.split()
        return sentence_bleu([reference_tokens], candidate_tokens,
                    weights=weights,
                    smoothing_function=self.smoothing)

    def meteor_calculator(self, reference, candidate):
        ref_list = [reference]
        candidate_list = [candidate]
        results = self.meteor.compute(predictions=candidate_list, references=ref_list)
        mt_score = round(results['meteor'], 2)
        return mt_score

    def bertscore_calculator(self, reference, candidate):
        P, R, F1 = self.bert_scorer.score([candidate], [reference])
        precision = P.mean().item() if P is not None else 0
        recall = R.mean().item() if R is not None else 0
        f1_score = F1.mean().item() if F1 is not None else 0
        return {
            'precision': precision,
            'recall': recall,
            'f1': f1_score
        }

    def g_eval(self, reference, candidate):
        results = {}
        for metric, prompt_template in self.prompts.items():
            prompt = prompt_template.replace("{{Document}}", reference).replace("{{Summary}}", candidate)
            scores = []
            for _ in range(20):  # num_samples=20
                output = self.model(
                    prompt,
                    max_tokens=5,
                    temperature=2.0,
                    top_p=1.0,
                )
                generated = output['choices'][0]['text'].strip()
                try:
                    score = float(next(filter(str.isdigit, generated)))
                    if 1 <= score <= 5:
                        scores.append(score)
                except:
                    continue
            
            if scores:
                results[metric] = {
                    'average': round(statistics.mean(scores), 2),
                    'std_dev': round(statistics.stdev(scores), 2) if len(scores) > 1 else 0,
                    'num_samples': len(scores)
                }
        return results