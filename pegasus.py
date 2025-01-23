# import pegasus
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from GUI import *

class Pegasus:
    def __init__ (self, input_text):
        # load pegasus for summarization
        self.model_name = "google/pegasus-xsum"
        self.tokenizer  = PegasusTokenizer.from_pretrained(self.model_name) # initialize pegasus' tokenizer
        self.model  = PegasusForConditionalGeneration.from_pretrained(self.model_name) # initialize pegasus model
        self.input_text = input_text


    def tokenizer(input_text): 
        # tokenize text 
        tokenized = self.tokenizer(input_text, truncation = True, padding = "longest", return_tensors = "pt")
        return tokenized

    def summarizer(tokenized_text):
        #   summarize
        summarized = self.model.generate(**tokenized)
        return summarized

    def detokenize(summarized_text):
        # detokenize
        summary = self.tokenizer.batch_decode (summarized)
        return summary

# run summarized text through LLM

# input text (example text for now)
sample_text = ("""The chicken nugget was developed in the 1950s by Robert C. Baker,
                   a food science professor at Cornell University, and published as unpatented academic work.
                   Bite-sized pieces of chicken, coated in batter and then deep fried,
                   were called "Chicken Crispies" by Baker and his associates.
                   Two problems the meat industry was facing at the time were being able to clump
                   ground meat without a skin and producing a batter coating that could be both deep
                   fried and frozen without becoming detached. Baker's innovations solved these
                   problems and made it possible to form chicken nuggets in any shape by first
                   coating the meat in vinegar, salt, grains, and milk powder to make it hold together
                   and then using an egg- and grain-based batter that could be fried as well as frozen.
                    Dinosaur-shaped (or simply dino) chicken nuggets were first trademarked by
                    Perdue Farms in 1991, and its rise in popularity was possibly assisted by the
                    success of the Jurassic Park franchise.
 """ )
    
