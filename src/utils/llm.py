from transformers import AutoTokenizer, AutoModelForSequenceClassification

class LLM:
    def __init__(self, pathname):
        # load LLM from Hugging Face
        self.model_name = pathname

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(pathname)
            self.model = AutoModelForSequenceClassification.from_pretrained(pathname)

        except Exception as e:
            print (f"Error handling LLM: {str(e)}")

    def tokenize (self, input_text):
        # tokenize text
        return self.tokenizer(input_text, padding=True, truncation=True, return_tensors="pt")

    def summarizer(self, tokenized_text):
        # summarize text
        return self.model.generate(**tokenized_text)

    def detokenize(self, summarized_text):
        # detokenize text
        return self.tokenizer.batch_decode(summarized_text)

