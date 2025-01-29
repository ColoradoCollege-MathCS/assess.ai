#import evaluate library for now
import evaluate
import nltk
import pycocovalcap
import rouge-score
import mathplotlib.pyplot as plt
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



def rouge_calculator(reference, candidate)
rouge = evaluate.load('rouge') #load metric
reference = []
candidate []
#reference text
#candidate- generated LLM text
#use rouge-score package
#use rouge-1 rouge-2 and rouge-L metrics
#report precision,recall, f1 score for each rouge metric
rouge_results = rouge.compute(predictions=candidate,
                                     references=reference)

print(f"ROUGE-1 Precision : {rouge_results['rouge1'].precision:.4f}, Recall : {rouge_results['rouge1'].recall:.4f}, F1 Score: {rouge_results['rouge1'].f1:.4f}")

print(f"ROUGE-2 Precision : {rouge_results['rouge2'].precision:.4f}, Recall : {rouge_results['rouge2'].recall:.4f},  F1 Score: {rouge_results['rouge2'].f1:.4f}")
print(f"ROUGE-L Precision : {rouge_results['rougeL'].precision:.4f}, Recall : {rouge_results['rougeL'].recall:.4f}, F1 Score: {rouge_results['rougeL'].f1:.4f}")

#print result for ROUGE -1

#print result for Rouge -2


#print result for rouge-L

return results







def bleu_calculator(reference, candidate)
bleu = evaluate.load("bleu") #load metric
reference = []word_tokenize(ref) for ref in reference]
candidate [word_tokenizer(cand) for cand in candidate]
#reference text
#candidate- generated LLM text
#tokenize
#use nltk.translate.bley_score.sentence_bley
#works by comparing ngrams in both refernece and candidate text
#calculate BLEU for single sentence or over multiple samples
bleu_results = sentence_bleu(reference, candidate)

print(f"BLEU Score: {bleu_results['bleu'] * 100:.2f}")

return bleu_results



# takes in a reference (the original) and a candidate (the generated)
def meteor_calculator(reference, candidate)

	# hardcode for now
	candidate = "the quick brown fox jumped over the lazy dog"
	reference = "a fast brown fox leads over a lazy dog"
	
	# uses nlkt translator
	score = meteor_score([reference], candidate)
	print(f"METEOR Score: {score}")



def average_scores(ref_list, candid_list)
#calculate the averagbe score across all ex
#for BLEU- compure BLEU for each sentence pair take the mean of BLEU scores
#for rouge, you can take thw average precision, recall, and f1 scores




def display_results(rouge_results, bleu_results)
#bleu is a single score, float between 0 and 1
# rouge provudes precision, recall, and f1 scores for each metric (rouge1 rouge2 rougeL
#print them and display them to a save file


#print statements
#print statements





def graph_results(rouge_results, bleu_results)
#graph and display calculated results above in a fgraph or trendlune.
#plotting the BLEU/ROUGE scores over time
#mathplotlib






#example sentences (non tokenized)
reference = ["the cat is on the mat"]
candidate = ["the cat is on mat"]


# BLEU expects plain text inputs
bleu_results = bleu_metric.compute(predictions=candidate, references=reference)
print(f"BLEU Score: {bleu_results['bleu'] * 100:.2f}")


# ROUGE expects plain text inputs
rouge_results = rouge_metric.compute(predictions=candidate,
                                     references=reference)

