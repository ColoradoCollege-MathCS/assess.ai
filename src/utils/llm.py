<<<<<<< HEAD
<<<<<<< HEAD
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
=======
from transformers import (
    AutoConfig,
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
    AutoModel,
    AutoModelForCausalLM
)

>>>>>>> 18b5a80842d2d547646a5a0f221bdf64cdc5890d

class LLM:
    def __init__(self, model_id):
        self.model_id = model_id
        self.config = AutoConfig.from_pretrained(self.model_id)
        self.model_type = self.config.model_type
        self.model_class = None
        self.tokenizer = None
        self.model = None

<<<<<<< HEAD

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
=======
    def tokenize(self, input_text):
>>>>>>> 18b5a80842d2d547646a5a0f221bdf64cdc5890d
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
<<<<<<< HEAD
        self.model.save_pretrained ("../model_files/" + path_name)
        self.tokenizer.save_pretrained("../model_files/" + path_name)
        print (self.model_id + " was successfully downloaded!")
=======
        self.model.save_pretrained("../model_files/" + path_name)
        self.tokenizer.save_pretrained("../model_files/" + path_name)
=======
        self.model.save_pretrained("../model_files/" + path_name)
        self.tokenizer.save_pretrained("../model_files/" + path_name)
>>>>>>> 18b5a80842d2d547646a5a0f221bdf64cdc5890d
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
<<<<<<< HEAD
        self.model = self.model_class.from_pretrained(self.model_id)
>>>>>>> a0610ba1835c74dcf76d954652a1a43adb5e15a1
=======
        self.model = self.model_class.from_pretrained(self.model_id)
>>>>>>> 18b5a80842d2d547646a5a0f221bdf64cdc5890d
