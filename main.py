from datasets import load_dataset
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import torch
from tqdm import tqdm

def load_model_and_tokenizer():
    model_name = "google/pegasus-xsum"
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = model.to(device)
    
    return model, tokenizer, device

def generate_summary(text, model, tokenizer, device):
    try:
        if not text or not isinstance(text, str):
            return "Error: Invalid input text"
        
        # Process text in smaller chunks if it's too long
        max_chunk_length = 1024
        chunks = [text[i:i + max_chunk_length] for i in range(0, len(text), max_chunk_length)]
        summaries = []
        
        for chunk in chunks:
            inputs = tokenizer(
                chunk,
                max_length=512,  # Reduced from 1024
                padding=True,
                truncation=True,
                return_tensors="pt"
            )
            
            inputs = inputs.to(device)
            
            summary_ids = model.generate(
                inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                num_beams=2,  # Reduced from 4
                max_length=256,  # Reduced from 512
                min_length=128,  # Reduced from 256
                length_penalty=1.5,  # Reduced from 2.0
                no_repeat_ngram_size=2,
                early_stopping=True,
                do_sample=False,
                temperature=1.0,
                top_k=50,
                top_p=0.95,
            )
            
            chunk_summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            summaries.append(chunk_summary)
        
        # Combine summaries
        final_summary = ' '.join(summaries)
        return final_summary
        
    except Exception as e:
        print(f"Error generating summary: {str(e)}")
        print(f"Text length: {len(text)}")
        return f"Error: {str(e)}"

def save_to_file(items, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        for i, item in enumerate(items, 1):
            f.write(f"Article {i}\n")
            f.write("-" * 80 + "\n")
            f.write(item.strip() + "\n\n")

def main():
    try:
        # Reduced to 10 entries for testing
        dataset = load_dataset("scientific_papers", "pubmed", split="train[:1]")
        
        print("Loading PEGASUS model and tokenizer...")
        model, tokenizer, device = load_model_and_tokenizer()
        
        original_abstracts = []
        generated_summaries = []
        
        print("Generating summaries...")
        for article in tqdm(dataset):
            text = article['article']
            
            if len(text) > 0:
                original_abstracts.append(text)
                summary = generate_summary(text, model, tokenizer, device)
                generated_summaries.append(summary if summary else "Error: Failed to generate summary")
                
        save_to_file(original_abstracts, 'original_abstracts.txt')
        save_to_file(generated_summaries, 'pegasus_summaries.txt')
        
        print("Results saved to 'original_abstracts.txt' and 'pegasus_summaries.txt'")
        
        return original_abstracts, generated_summaries
        
    except Exception as e:
        print(f"Error in main: {str(e)}")
        return [], []

if __name__ == "__main__":
    original_abstracts, generated_summaries = main()
