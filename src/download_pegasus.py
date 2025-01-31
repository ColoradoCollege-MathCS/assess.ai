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
    print("Model downloaded and saved successfully!")

if __name__ == "__main__":
    download_model()

"""
Model Details:
├── config.json              (Architecture blueprint)
├── generation_config.json   (Controls how the model generates text: beam search)
├── model.safetensors       (Weights that change when doing finetuning)
├── special_tokens_map.json  (Maps special tokens like [PAD], [EOS], [UNK] to their IDs, Used for handling start/end of text, padding, unknown words)
├── spiece.model            (The tokenizer's vocabulary and rules, Defines how to split text into tokens)
└── tokenizer_config.json    (Configuration for the tokenizer's behavior)

"""