# Import required libraries
from torch.utils.data import Dataset
import json
from pathlib import Path
import csv

# Object to convert text dataset into an object accessible by Pytorch's Dataloader
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


def load_dataset(data_path, start_idx=0, end_idx=100):
    data_path = Path(data_path)
    if not data_path.exists():
        raise FileNotFoundError(f"Data file not found at {data_path}")

    file_extension = data_path.suffix.lower()
    
    try:
        data = []
        with open(data_path, 'r', encoding='utf-8') as f:
            # Handle different file formats
            if file_extension == '.json':
                data = json.load(f)[start_idx:end_idx]
                
            elif file_extension == '.jsonl':
                for i, line in enumerate(f):
                    if start_idx <= i < end_idx and line.strip():
                        data.append(json.loads(line))
                        
            elif file_extension == '.csv':
                reader = csv.DictReader(f)
                for i, row in enumerate(reader):
                    if start_idx <= i < end_idx:
                        if 'input_text' not in row or 'target_text' not in row:
                            raise ValueError("CSV must contain 'input_text' and 'target_text' columns")
                        data.append({
                            'input_text': row['input_text'],
                            'target_text': row['target_text']
                        })
                    
            elif file_extension == '.txt':
                lines = f.readlines()
                for idx in range(start_idx, min(end_idx, len(lines)), 2):
                    if idx + 1 >= len(lines):
                        break
                        
                    input_line = lines[idx].strip()
                    target_line = lines[idx + 1].strip()
                    
                    if input_line.startswith('INPUT:') and target_line.startswith('TARGET:'):
                        data.append({
                            'input_text': input_line[6:].strip(),
                            'target_text': target_line[7:].strip()
                        })
            
            else:
                raise ValueError(f"Unsupported file format: {file_extension}")
        if not data: #There was no data found
            raise ValueError("No valid data found in the specified range. Please check your dataset or specified indices")
            
        # Validate data structure
        if not all(isinstance(item, dict) and 'input_text' in item and 'target_text' in item for item in data):
            raise ValueError("Data must contain 'input_text' and 'target_text' fields")
        return data
        
    except Exception as e:
        print(f"Error loading dataset: {str(e)}")
        raise