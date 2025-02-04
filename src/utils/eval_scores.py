import os
import nltk
from rouge_score import rouge_scorer
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
import evaluate
from bert_score import BERTScorer
from nltk.data import path as nltk_data_path


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

# Set up NLTK paths and prevent download. NLTK defaults to downloading files for every run but we already have them locally
setup_nltk_paths()

        # The line nltk.download = prevent_download replaces NLTK's original download function with our custom function.
nltk.download = prevent_download

# Declare a class here so you can preinitialize all scorers. If these were all independent function we'd have to initialize the score calculators every time
class ScoreCalculator:
    def __init__(self):
        # Initialize all scorers
        self.rouge_scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
        self.bert_scorer = BERTScorer(model_type='bert-base-uncased')
        self.meteor = evaluate.load('meteor')
        self.smoothing = SmoothingFunction().method1


    def rouge_calculator(self,reference, candidate): #caulculates rouge metric
        scores = self.rouge_scorer.score(reference, candidate)
        return {
            'rouge1': scores['rouge1'].fmeasure if scores['rouge1'].fmeasure is not None else 0,
            'rouge2': scores['rouge2'].fmeasure if scores['rouge2'].fmeasure is not None else 0,
            'rougeL': scores['rougeL'].fmeasure if scores['rougeL'].fmeasure is not None else 0
        }

    def bleu_calculator(self,reference, candidate):
        weights = (0.25, 0.25, 0, 0)  # weights for uni-gram, bi-gram, tri-gram, and 4-gram
        reference_tokens = reference.split() #tokenize
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