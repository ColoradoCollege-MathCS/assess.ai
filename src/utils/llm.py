<<<<<<< HEAD
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class LLM:
    def __init__(self, model_id):
        # load LLM from Hugging Face
        self.model_id = model_id
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_id)


    def tokenize (self, input_text):
=======
from transformers import (
    AutoConfig,
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    AutoModel,
    AutoModelForCausalLM
)


class LLM:
    def __init__(self, model_id):
        self.model_id = model_id
        self.config = AutoConfig.from_pretrained(self.model_id)
        self.model_type = self.config.model_type
        self.model_class = None
        self.tokenizer = None
        self.model = None

    def tokenize(self, input_text):
>>>>>>> a0610ba1835c74dcf76d954652a1a43adb5e15a1
        # tokenize text
        return self.tokenizer(input_text, padding=True, truncation=True, return_tensors="pt")

    def summarizer(self, tokenized_text):
        # summarize text
        return self.model.generate(**tokenized_text)

    def detokenize(self, summarized_text):
        # detokenize text
        return self.tokenizer.batch_decode(summarized_text)

    def download_LLM(self):
        # save model and tokenizer
        path_name = f"../model_files/{self.model_id.replace('/', '_')}"
<<<<<<< HEAD
        self.model.save_pretrained ("../model_files/" + path_name)
        self.tokenizer.save_pretrained("../model_files/" + path_name)
        print (self.model_id + " was successfully downloaded!")
=======
        self.model.save_pretrained("../model_files/" + path_name)
        self.tokenizer.save_pretrained("../model_files/" + path_name)
        print(self.model_id + " was successfully downloaded!")

    def load_LLM(self):
        # check model type using AutoConfig
        # dict of model classes
        model_dict = {
            "seq2seq": AutoModelForSeq2SeqLM,
            "causallm": AutoModelForCausalLM,
            "automodel": AutoModel
        }

        # determine which model class -> which model type
        if self.model_type in ["pegasus, pegasus_x", "t5", "mt5", "mbart"]: # models = AutoModelForSeq2SeqLM
            self.model_class = model_dict["seq2seq"]
        elif self.model_type in ["gpt2"]:
            self.model_class = model_dict["causallm"]
        elif self.model_type in ["bart"]:
            self.model_class = model_dict["automodel"]
        else:
            self.model_class = model_dict["automodel"] # generic model class

        # load model with correct configurations
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.model = self.model_class.from_pretrained(self.model_id)
>>>>>>> a0610ba1835c74dcf76d954652a1a43adb5e15a1
