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
        # tokenize text
        return self.tokenizer(input_text, padding=True, truncation=True, return_tensors="pt")

    def summarizer(self, tokenized_text):
        # summarize text
        return self.model.generate(**tokenized_text)

    def detokenize(self, summarized_text):
        # detokenize text
        return self.tokenizer.batch_decode(summarized_text)

    def import_LLM(self):
        # save model and tokenizer
        path_name = f"../model_files/{self.model_id.replace('/', '_')}"
        self.model.save_pretrained("../model_files/" + path_name)
        self.tokenizer.save_pretrained("../model_files/" + path_name)
        print(self.model_id + " was successfully imported!")


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
