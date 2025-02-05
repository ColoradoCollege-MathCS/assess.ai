from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

def download_model():
    print("Downloading FLAN-T5-small model...")
    model_name = "google/pegasus-xsum"
    
    # Download tokenizer and model
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    
    # Save model and tokenizer locally
    print("Saving model locally...")
    save_path = "../model_files/pegasus"
    tokenizer.save_pretrained(save_path)
    model.save_pretrained(save_path)
    print("Model downloaded and saved successfully!")

if __name__ == "__main__":
    download_model()

"""
Model Details:
├── config.json              (Model architecture configuration)
├── generation_config.json   (Text generation parameters)
├── model.safetensors       (Model weights)
├── special_tokens_map.json  (Mapping of special tokens like [PAD], [EOS])
├── tokenizer.json          (Tokenizer vocabulary and rules)
└── tokenizer_config.json    (Tokenizer configuration)
"""