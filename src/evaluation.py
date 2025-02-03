#import evaluate library for now
import evaluate
import nltk
import os
#import mathplotlib.pyplot as plt
from nltk.translate.bleu_score import sentence_bleu
from transformers import BertTokenizer, BertForMaskedLM, BertModel
from rouge_score import rouge_scorer
from nltk.tokenize import word_tokenize
from bert_score import BERTScorer
from nltk.translate.meteor_score import meteor_score
from evaluate import load
from summarizer import generate_summary
#from deepeval.metrics import GEval
#from deepeval.test_case import LLMTestCaseParams
from tqdm import tqdm
from openai import OpenAI
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCase
from deepeval.test_case import LLMTestCaseParams

# REMEMBER TO DELETE THE KEY WHEN PUSHING TO GITHUB

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY", ""))

def load_summaries(original_abstracts, generated_summaries):
    #reads the entire file as a string
    with open(original_abstracts, 'r', encoding='utf-8') as f:
        original_summaries = f.read().strip()  
    with open(generated_summaries, 'r', encoding='utf-8') as f:
        generated_summaries = f.read().strip() 
    #printing a preview as debugging purposes
    print(f"Original Summary: {original_summaries[:200]}...") 
    print(f"Generated Summary: {generated_summaries[:200]}...")  

    return original_summaries, generated_summaries
    

def rouge_calculator(reference, candidate): #caulculates rouge metric
    
#rouge = evaluate.load('rouge') #load metric
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    rouge_data = scorer.score(reference, candidate)
    for key in rouge_data:
        print(f'{key}: {rouge_data[key]}')
    return rouge_data


def bleu_calculator(reference, candidate):
    weights = (0.25, 0.25, 0, 0)  # Weights for uni-gram, bi-gram, tri-gram, and 4-gram
    candidate_tokens = candidate.split() #tokenize
    reference_tokens = reference.split()
    #works by comparing ngrams in both refernece and candidate text
    bleu_results = sentence_bleu([reference_tokens], candidate_tokens, weights=weights)
    #print the BLEU score
    print(f"BLEU score: {bleu_results:.4f}")
    return bleu_results

def meteor_calculator(reference, candidate):
    meteor = evaluate.load('meteor')
    ref_list = []
    ref_list.append(reference)
    candidate_list = []
    candidate_list.append(candidate)
    results = meteor.compute(predictions=candidate_list,references=ref_list)
    mt_score = round(results['meteor'],2)
    return mt_score

def bertscore_calculator(reference, candidate):
    #bertscore = load("bertscore")
   # scores = bertscore.compute(reference, candidate, lang="en")
   # print(scores)
   # BERTScore calculation
    scorer = BERTScorer(model_type='bert-base-uncased')
    P, R, F1 = scorer.score([candidate], [reference])
    print(f"BERTScore Precision: {P.mean():.4f}, Recall: {R.mean():.4f}, F1: {F1.mean():.4f}")
    return P, R, F1

def geval_calculator(reference, candidate):
	correctness_metric = GEval(
		name="Correctness",
		criteria="Determine whether the actual output is factually correct based on the expected output.",
		evaluation_steps=[
			"Check whether the facts in 'actual output' contradicts any facts in 'expected output",
			"You should also heavily penalize omission of detail",
			"Vague language, or contradicting OPINIONS, are ok"
		],
		evaluation_params=[LLMTestCaseParams.INPUT,LLMTestCaseParams.ACTUAL_OUTPUT,LLMTestCaseParams.EXPECTED_OUTPUT],
	)
	test_case = LLMTestCase(reference, candidate, reference)

	correctness_metric.measure(test_case)
	return(correctness_metric.score)




def evaluate_summaries(original_file, generated_file):
      # open the file data.txt; if there is no file, create one
    # append
    data_file = open("data.txt","w")
    try:
              original_summaries, generated_summaries = load_summaries(original_file, generated_file)
              original = original_summaries.strip()
              generated = generated_summaries.strip()
              #initialize
              rouge_scores = []
              bleu_scores = []
              BERTScore_scores = []
              meteor_scores = []
              geval_scores = []
              #original = original.strip()
              #generated = generated.strip()
             
              # writes files as the stuff is calculated
              print("Calculating ROUGE scores for generated summary:")
              rouge_data = rouge_calculator(original, generated)
              rouge_scores.append(rouge_data)
              # have to convert rouge_data which is an object to a string to write to file
              str_rg = str(rouge_data)
              data_file.write("Rouge Results:" + str_rg + "\n")

              print("Calculating BLEU score for generated summary:")
              bleu_score = bleu_calculator(original, generated)
              bleu_scores.append(bleu_score)
              str_bl = str(bleu_score)
              data_file.write("BLEU results:" + str_bl + "\n")

              print("Calculating BERTScore scores for generated summary :")
              BERTScore_results = bertscore_calculator(original, generated)
              BERTScore_scores.append(BERTScore_results)
              str_bt = str(BERTScore_results)
              data_file.write("BERTScore results:" + str_bt + "\n")

              print("Calculating METEOR scores for generated summary :")
              METEOR_results = meteor_calculator(original, generated)
              meteor_scores.append(METEOR_results)
              str_mt = str(METEOR_results)
              data_file.write("METEOR results:" + str_mt + "\n")

              print("Calculating GEval score for generated summary :")
              GEval_results = geval_calculator(original, generated)
              geval_scores.append(GEval_results)
              str_ge = str(GEval_results)
              print(str_ge)
              data_file.write("GEval results:" + str_ge + "\n")

    
    except Exception as e:
              print(f"Failed to evaluate: {e}")

      # always close your files!!
    data_file.close()
            

def main():
    original_file = 'original_abstracts.txt'
    summarized_file = 'pegasus_summaries.txt'
   # load_summaries(original_file, summarized_file)
    evaluate_summaries(original_file, summarized_file)
    
#def display_results(rouge_results, bleu_results)
#bleu is a single score, float between 0 and 1
# rouge provudes precision, recall, and f1 scores for each metric (rouge1 rouge2 rougeL
#print them and display them to a save file

#def graph_results(rouge_results, bleu_results):
#graph and display calculated results above in a fgraph or trendlune.
#plotting the BLEU/ROUGE scores over time
#mathplotlib



    
if __name__ == '__main__':
    main()
