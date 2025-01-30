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


def rouge_calculator(reference, candidate): #caulculates rouge metric
    
#rouge = evaluate.load('rouge') #load metric
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    
    scores = scorer.score(reference, candidate)

    for key in scores:
        print(f'{key}: {scores[key]}')

    return scores


def bleu_calculator(reference, candidate):
    weights = (0.25, 0.25, 0, 0)  # Weights for uni-gram, bi-gram, tri-gram, and 4-gram
    candidate_tokens = candidate.split() #tokenize
    reference_tokens = reference.split()

    #works by comparing ngrams in both refernece and candidate text

    bleu_results = sentence_bleu([reference_tokens], candidate_tokens, weights=weights)
    # print the BLEU score
    print(f"BLEU score: {bleu_results:.4f}")

    return bleu_results


#def meteor_calculator(reference, candidate):
  #  score = meteor_score([reference], candidate)
#


  #  print(f"METEOR Score: {score}")
  #  return score



def BERTScore_calculator(reference, candidate):
    #bertscore = load("bertscore")
   # scores = bertscore.compute(reference, candidate, lang="en")
   # print(scores)
   # BERTScore calculation
    scorer = BERTScorer(model_type='bert-base-uncased')
    P, R, F1 = scorer.score([candidate], [reference])
    print(f"BERTScore Precision: {P.mean():.4f}, Recall: {R.mean():.4f}, F1: {F1.mean():.4f}")


    return P, R, F1
    
    

#def average_scores(ref_list, candid_list):
    
#calculate the averagbe score across all ex
#for BLEU- compure BLEU for each sentence pair take the mean of BLEU scores
#for rouge, you can take thw average precision, recall, and f1 scores




#def display_results(rouge_results, bleu_results)
#bleu is a single score, float between 0 and 1
# rouge provudes precision, recall, and f1 scores for each metric (rouge1 rouge2 rougeL
#print them and display them to a save file


#def graph_results(rouge_results, bleu_results):
#graph and display calculated results above in a fgraph or trendlune.
#plotting the BLEU/ROUGE scores over time
#mathplotlib

def main():
    reference = "The Great Barrier Reef, a sprawling coral ecosystem off the coast of Australia,is facing significant threats from climate change, including rising ocean temperatures and ocean acidification.These factors are causing coral bleaching, a process where the coral loses its vibrant colors and essential algae,leading to potential coral death. Furthermore, pollution from coastal runoff can contribute to algal blooms,further stressing the reef's delicate balance.."
    candidate = "The Great Barrier Reef is under severe threat from climate change,primarily through rising ocean temperatures and acidification, which cause coral bleaching and potential coral death.Coastal pollution also adds stress to the reef's fragile ecosystem by triggering harmful algal blooms."
    print("Calculating ROUGE scores:")
    rouge_scores = rouge_calculator(reference, candidate)
    print("Calculating BLEU score:")
    bleu_score = bleu_calculator(reference, candidate)
    #print("Calculating METEOR scores:")
    #meteor_score = meteor_calculator(reference, candidate)
    print("Calculating BERTScore scores:")
    BERTScore_scores = BERTScore_calculator(reference, candidate)

if __name__ == '__main__':
    main()


