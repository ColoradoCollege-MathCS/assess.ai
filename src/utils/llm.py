from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

class LLM:
    def __init__(self, model_id):
        # load LLM from Hugging Face
        self.model_id = model_id
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_id)


    def tokenize (self, input_text):
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
        self.model.save_pretrained ("../model_files/" + path_name)
        self.tokenizer.save_pretrained("../model_files/" + path_name)
        print (self.model_id + " was successfully downloaded!")