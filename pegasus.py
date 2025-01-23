# import pegasus
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
from GUI import *

class Pegasus:
    def __init__ (self):
        # load pegasus for summarization
        self.model_name = "google/pegasus-xsum"
        self.tokenizer  = PegasusTokenizer.from_pretrained(self.model_name) # initialize pegasus' tokenizer
        self.model  = PegasusForConditionalGeneration.from_pretrained(self.model_name) # initialize pegasus model


    def tokenize(self, input_text): 
        # tokenize text 
        tokenized = self.tokenizer(input_text, truncation = True, padding = "longest", return_tensors = "pt")
        return tokenized

    def summarizer(self, tokenized_text):
        #   summarize
        summarized = self.model.generate(**tokenized_text)
        return summarized

    def detokenize(self, summarized_text):
        # detokenize
        summary = self.tokenizer.batch_decode (summarized_text)
        return summary

