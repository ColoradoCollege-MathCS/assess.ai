# Import required libraries
from torch.utils.data import Dataset
import json
from pathlib import Path
import csv

class TextDataset(Dataset):
    def __init__(self, data, tokenizer, max_length=256):
        self.data = data
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        # Return the total number of samples
        return len(self.data)

    def __getitem__(self, idx):
        # Get a single data item (input ID, attention mask, label, input text, target text)
        item = self.data[idx]
        # Tokenize input text with padding and truncation
        inputs = self.tokenizer(
            item['input_text'],
            max_length=self.max_length,
            truncation=True,
            padding='max_length',
            return_tensors='pt'
        )
        
        # Tokenize target text similarly
        targets = self.tokenizer(
            item['target_text'],
            max_length=self.max_length,
            truncation=True,
            padding='max_length',
            return_tensors='pt'
        )

        # Attention Mask: A binary mask (1s and 0s) that tells the model which tokens are real text and which are padding 1 means "pay attention to this token. 0 means "ignore this token (it's just padding)"
        # Return processed tensors and original text
        return {
            'input_ids': inputs['input_ids'].squeeze(),
            'attention_mask': inputs['attention_mask'].squeeze(),
            'labels': targets['input_ids'].squeeze(),
            'input_text': item['input_text'],
            'target_text': item['target_text']
        }

def load_dataset(data_path, max_samples=None):
    data_path = Path(data_path)
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found at {data_path}")
        
    file_extension = data_path.suffix.lower() # Get file extension (.json, .csv...)
    
    try:
        # Handle different file formats
        if file_extension == '.json':
            # Load standard JSON file
            with open(data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
        elif file_extension == '.jsonl':
            # Load JSON Lines file (one JSON object per line)
            data = []
            with open(data_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        data.append(json.loads(line))
                        
        elif file_extension == '.csv':
            # Load CSV file with specific columns
            data = []
            with open(data_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if 'input_text' not in row or 'target_text' not in row:
                        raise ValueError("CSV must contain 'input_text' and 'target_text' columns")
                    data.append({
                        'input_text': row['input_text'],
                        'target_text': row['target_text']
                    })
                    
        elif file_extension == '.txt':
            # Load custom format text file with INPUT: and TARGET: prefixes
            data = []
            current_item = {}
            with open(data_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
                
            for line in lines:
                line = line.strip()
                if line.startswith('INPUT:'):
                    if current_item:
                        data.append(current_item)
                    current_item = {'input_text': line[6:].strip()}
                elif line.startswith('TARGET:'):
                    if 'input_text' in current_item:
                        current_item['target_text'] = line[7:].strip()
                        data.append(current_item)
                        current_item = {}
                        
            # Add last item if complete
            if current_item and 'input_text' in current_item and 'target_text' in current_item:
                data.append(current_item)
                
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
            
        for item in data:
            if not isinstance(item, dict) or 'input_text' not in item or 'target_text' not in item:
                raise ValueError("Data must contain 'input_text' and 'target_text' fields")
                
        if max_samples is not None:
            data = data[:max_samples]
            
        return data
        
    except Exception as e:
        print(f"Error loading dataset: {str(e)}")
        raise