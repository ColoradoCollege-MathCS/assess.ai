from transformers import PegasusForConditionalGeneration, PegasusTokenizer

def download_model():
    print("Downloading Pegasus model...")
    model_name = "google/pegasus-xsum"
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name)
    
    # Save model and tokenizer to local directory
    print("Saving model locally...")
    tokenizer.save_pretrained("model_files")
    model.save_pretrained("model_files")
    print("Model downloaded and saved successfully!")

if __name__ == "__main__":
    download_model()