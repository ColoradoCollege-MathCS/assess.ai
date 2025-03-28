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
                lines = [line.strip() for line in f.readlines() if line.strip()]  # Remove empty lines
                
                current_idx = 0
                while current_idx < len(lines):
                    # Find next input/target pair
                    while current_idx < len(lines) and not any(lines[current_idx].startswith(prefix) for prefix in ['INPUT:', 'INPUT :']):
                        current_idx += 1
                    if current_idx >= len(lines):
                        break
                        
                    input_line = lines[current_idx]
                    target_line = lines[current_idx + 1] if current_idx + 1 < len(lines) else None
                    # Check if we have a valid input/target pair
                    if (target_line and 
                        any(input_line.startswith(prefix) for prefix in ['INPUT:', 'INPUT :']) and 
                        any(target_line.startswith(prefix) for prefix in ['TARGET:', 'TARGET :'])):
                        
                        # Extract the text after the prefix
                        input_text = input_line.split(':', 1)[1].strip()
                        target_text = target_line.split(':', 1)[1].strip()
                        
                        if start_idx <= len(data) < end_idx:
                            data.append({
                                'input_text': input_text,
                                'target_text': target_text
                            })
                    
                    current_idx += 2
            
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
