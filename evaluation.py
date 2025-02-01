#import evaluate library for now
import evaluate
import nltk
#import mathplotlib.pyplot as plt
from nltk.translate.bleu_score import sentence_bleu
from transformers import BertTokenizer, BertForMaskedLM, BertModel
from rouge_score import rouge_scorer
from nltk.tokenize import word_tokenize
from bert_score import BERTScorer
from nltk.translate.meteor_score import meteor_score
from evaluate import load
<<<<<<< HEAD
from main import generate_summary
from tqdm import tqdm


#preprocess data
#DATASETS shold be structured in a way that makes it easy to pair w ref texts. AKA
#CSV format/ JSOMN format
#clean and tokenize the reference and generated text in consisten manner
#nltk.word_tokenizer()

#for BLEU - one word- level tokenization - nltk.word_tokenize
#for ROUGE- sentence level tokenizatiomn and use libraries like rouge-score

#THIS WORKs BEST FOR ENGLISH LANGUAGES
#test originl version
#test

# load a submitted file
# print it out in terminal (can be changed, but as an example)
# close the file
def load_text_from_file(filename):
    data_file = open(filename, r)
    file_info = data_file.read()
    print(file_info)
    data_file.close()
=======
from summarizer import generate_summary
#from deepeval.metrics import GEval
#from deepeval.test_case import LLMTestCaseParams
from tqdm import tqdm



def load_summaries(original_abstracts, generated_summaries):
    with open(original_abstracts, 'r', encoding='utf-8') as f:
         original_summaries = f.readlines()
    with open(generated_summaries, 'r', encoding='utf-8') as f:
         generated_summaries = f.readlines()

    return original_summaries, generated_summaries
>>>>>>> 060f57572b6b041cdc7955dbb50b9998d99df92d
    

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

#GROSS def meteor_calculator(reference, candidate):

	# uses nlkt translator
	#score = meteor_score([reference], candidate)
	#print(f"METEOR Score: {score}")
	#return score

def BERTScore_calculator(reference, candidate):
    #bertscore = load("bertscore")
   # scores = bertscore.compute(reference, candidate, lang="en")
   # print(scores)
   # BERTScore calculation
    scorer = BERTScorer(model_type='bert-base-uncased')
    P, R, F1 = scorer.score([candidate], [reference])
    print(f"BERTScore Precision: {P.mean():.4f}, Recall: {R.mean():.4f}, F1: {F1.mean():.4f}")
    return P, R, F1


<<<<<<< HEAD
def evaluate_summaries():

    # open the file data.txt; if there is no file, create one
=======
#def gEVAL_calculator(reference,candidate):

#pip instal deepeval

   # correctness_metric = GEval(
    #    name="Accurateness",
    #    criteria="Determine whether the candidate summary is accurate compared to the reference summary.",
        # NOTE: you can only provide either criteria or evaluation_steps, and not both
    
      #  evaluation_params=[LLMTestCaseParams.INPUT, LLMTestCaseParams.ACTUAL_OUTPUT, LLMTestCaseParams.TARGET],
 #   )
    

    

def evaluate_summaries(original_file, generated_file):
      # open the file data.txt; if there is no file, create one
>>>>>>> 060f57572b6b041cdc7955dbb50b9998d99df92d
    # append
    data_file = open("data.txt","a")
    try:
              
<<<<<<< HEAD
              # writes files as the stuff is calculated
              print("Calculating ROUGE scores:")
              rouge_data = rouge_calculator(original, generated)
              rouge_scores.append(rouge_data)
              str_rg = str(rouge_data)
              data_file.write("Rouge:" + str_rg)

              print("Calculating BLEU score:")
              bleu_score = bleu_calculator(original, generated)
              bleu_scores.append(bleu_score)
              str_bl = str(bleu_score)
              data_file.write("BLEU:" + str_bl)

              print("Calculating BERTScore scores:")
              BERTScore_results = BERTScore_calculator(original, generated)
              BERTScore_scores.append(BERTScore_result)
              str_bt = str(BERTScore_results)
              data_file.write("BERT:" + str_bt)

    except Exception as e:
              print(f"Failed to evaluate")

=======
              original_summaries,  generated_summaries = load_summaries(original_file, generated_file)
              
              #initialize
              rouge_scores = []
              bleu_scores = []
              BERTScore_scores = []

              for original, generated in zip(original_summaries, generated_summaries):
                   original = original.strip()
                   generated = generated.strip()
                   # writes files as the stuff is calculated
                   print("Calculating ROUGE scores:")
                   rouge_data = rouge_calculator(original, generated)
                   rouge_scores.append(rouge_data)
                   str_rg = str(rouge_data)
                   data_file.write("Rouge:" + str_rg + "\n")

                   print("Calculating BLEU score:")
                   bleu_score = bleu_calculator(original, generated)
                   bleu_scores.append(bleu_score)
                   str_bl = str(bleu_score)
                   data_file.write("BLEU:" + str_bl + "\n")

                   print("Calculating BERTScore scores:")
                   BERTScore_results = BERTScore_calculator(original, generated)
                   BERTScore_scores.append(BERTScore_results)
                   str_bt = str(BERTScore_results)
                   data_file.write("BERT:" + str_bt + "\n")

    except Exception as e:
              print(f"Failed to evaluate")

>>>>>>> 060f57572b6b041cdc7955dbb50b9998d99df92d
      # always close your files!!
    data_file.close()
            



def main():
    original_file = 'original_abstracts.txt'
    summarized_file = 'pegasus_summaries.txt'


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
