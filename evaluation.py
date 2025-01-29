#import evaluate library for now
import evaluate
import nltk
#import mathplotlib.pyplot as plt
from nltk.translate.bleu_score import sentence_bleu
from rouge_score import rouge_scorer
from nltk.tokenize import word_tokenize
from nltk.translate.meteor_score import meteor_score

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

#print(f"BLEU Score: {bleu_results['bleu'] * 100:.2f}")

    return bleu_results


# takes in a reference (the original) and a candidate (the generated)
def meteor_calculator(reference, candidate)

	# hardcode for now
	candidate = "the quick brown fox jumped over the lazy dog"
	reference = "a fast brown fox leads over a lazy dog"
	
	# uses nlkt translator
	score = meteor_score([reference], candidate)
	print(f"METEOR Score: {score}")
	return score


def average_scores(ref_list, candid_list):
#calculate the averagbe score across all ex
#for BLEU- compure BLEU for each sentence pair take the mean of BLEU scores
#for rouge, you can take thw average precision, recall, and f1 scores




def display_results(rouge_results, bleu_results):
#bleu is a single score, float between 0 and 1
# rouge provudes precision, recall, and f1 scores for each metric (rouge1 rouge2 rougeL
#print them and display them to a save file


#print statements
#print statements




def graph_results(rouge_results, bleu_results):
#graph and display calculated results above in a fgraph or trendlune.
#plotting the BLEU/ROUGE scores over time
#mathplotlib

def main():
    reference = "The cat was found under the bed."
    candidate = "The cat was under the bed."
    print("Calculating ROUGE scores:")
    rouge_scores = rouge_calculator(reference, candidate)
    print("\nCalculating BLEU score:")
    bleu_score = bleu_calculator(reference, candidate)


if __name__ == '__main__':
    main()
