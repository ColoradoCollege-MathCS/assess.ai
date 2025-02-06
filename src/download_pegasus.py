<<<<<<< HEAD
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
=======
from transformers import PegasusForConditionalGeneration, PegasusTokenizer

def download_model():
    print("Downloading Pegasus model...")
    model_name = "google/pegasus-xsum"
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name)
    
    # Save model and tokenizer to local directory
    print("Saving model locally...")
    tokenizer.save_pretrained("../model_files/pegasus")
    model.save_pretrained("../model_files/pegasus")
>>>>>>> a0610ba1835c74dcf76d954652a1a43adb5e15a1
    print("Model downloaded and saved successfully!")

if __name__ == "__main__":
    download_model()

"""
Model Details:
<<<<<<< HEAD
├── config.json              (Model architecture configuration)
├── generation_config.json   (Text generation parameters)
├── model.safetensors       (Model weights)
├── special_tokens_map.json  (Mapping of special tokens like [PAD], [EOS])
├── tokenizer.json          (Tokenizer vocabulary and rules)
└── tokenizer_config.json    (Tokenizer configuration)
=======
├── config.json              (Architecture blueprint)
├── generation_config.json   (Controls how the model generates text: beam search)
├── model.safetensors       (Weights that change when doing finetuning)
├── special_tokens_map.json  (Maps special tokens like [PAD], [EOS], [UNK] to their IDs, Used for handling start/end of text, padding, unknown words)
├── spiece.model            (The tokenizer's vocabulary and rules, Defines how to split text into tokens)
└── tokenizer_config.json    (Configuration for the tokenizer's behavior)

>>>>>>> a0610ba1835c74dcf76d954652a1a43adb5e15a1
"""