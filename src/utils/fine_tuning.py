import torch
from torch.utils.data import DataLoader
from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import json
from pathlib import Path
import time
from datetime import datetime
from .data_loader import TextDataset, load_dataset
import random

# Set single thread for torch operations
torch.set_num_threads(1)
# Set random seeds for reproducibility
random.seed(42)
torch.manual_seed(42)

"""
For fine-tuning, we use the pre-trained Pegasus model's architecture and train it further by having it try to generate target_text from input_text, 
calculating the difference between what it generated and what the target_text actually should be (this difference is the "loss"), 
and adjusting its weights to minimize this difference. Loss is calculated using cross entropy loss

Data is organized into batches using DataLoader. 
During each epoch (a complete pass through the dataset), the model processes these batches one at a time. 
For each batch, it first makes predictions (forward pass) by trying to generate output from the input text, then calculates how wrong it was (loss). 
Using this loss, it figures out how to adjust its weights to do better (backward pass through loss.backward()) and updates these weights using the Adam optimizer (optimizer.step()). 
The loss value reported during training tells you how well the model is learning - a decreasing loss generally means the model is improving at the task.

"""

class FineTuner:
    def __init__(self, model_path, config_str):
        self.model_path = Path(model_path)
        # Use GPU if available
        self.device = torch.device('cpu')
        
        # Parse configuration from JSON string
        self.config = json.loads(config_str)['training']
        
        # Load pre-trained model and tokenizer
        self.tokenizer = PegasusTokenizer.from_pretrained(self.model_path)
        self.model = PegasusForConditionalGeneration.from_pretrained(
            self.model_path,
            low_cpu_mem_usage=True
        )
        self.model.to(self.device)
        
    def load_dataset(self, data_path):
        return load_dataset(data_path, max_samples=self.config['max_samples'])
    
    def fine_tune(self, train_data, progress_callback=None):
        try:
            # Create output directory with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_dir = Path("../model_files/finetunedmodels")
            base_dir.mkdir(exist_ok=True)
            
            output_dir = base_dir / f"fine_tuned_{timestamp}"
            output_dir.mkdir(parents=True)
            
            # Create dataset
            dataset = TextDataset(
                train_data, 
                self.tokenizer
            )
            
            # Calculate training batches
            total_samples = len(train_data)
            batch_size = self.config['batch_size']
            total_batches = (total_samples + batch_size - 1) // batch_size
            
            # Create data loader for batch processing
            train_loader = DataLoader(
                dataset,
                batch_size=batch_size,
                shuffle=True,
                num_workers=0,
                drop_last=False
            )
            
            # Initialize optimizer with learning rate
            optimizer = torch.optim.AdamW(
                self.model.parameters(),
                lr=self.config['learning_rate']
            )
            
            print(f"Starting training with {total_samples} samples in {total_batches} batches per epoch")
            
            for epoch in range(self.config['num_epochs']):
                self.model.train()
                epoch_loss = 0
                batch_count = 0
                
                for batch in train_loader:
                    # Get actual batch size
                    current_batch_size = batch['input_ids'].size(0)
                    
                    input_ids = batch['input_ids'].to(self.device)
                    attention_mask = batch['attention_mask'].to(self.device)
                    labels = batch['labels'].to(self.device)
                    
                    # Forward pass
                    outputs = self.model(
                        input_ids=input_ids,
                        attention_mask=attention_mask,
                        labels=labels
                    )
                    
                    # Get cross entropy loss
                    loss = outputs.loss
                    epoch_loss += loss.item() * current_batch_size
                    batch_count += 1
                    
                    # Backward pass 
                    loss.backward()
                    optimizer.step()
                    optimizer.zero_grad()
                    
                    # Update progress
                    if progress_callback:
                        avg_loss = epoch_loss / (batch_count * batch_size)
                        progress = {
                            'epoch': epoch + 1,
                            'total_epochs': self.config['num_epochs'],
                            'batch': batch_count,
                            'total_batches': total_batches,
                            'loss': avg_loss
                        }
                        progress_callback(progress)
                
                # Save checkpoint after each epoch
                checkpoint_dir = output_dir / f"checkpoint-epoch-{epoch+1}"
                checkpoint_dir.mkdir(exist_ok=True)
                self.model.save_pretrained(checkpoint_dir)
                self.tokenizer.save_pretrained(checkpoint_dir)
                
                print(f"Epoch {epoch+1}/{self.config['num_epochs']} completed. Average loss: {epoch_loss/total_samples:.4f}")
            
            # Save final model and tokenizer
            self.model.save_pretrained(output_dir)
            self.tokenizer.save_pretrained(output_dir)
            
            final_path = output_dir.absolute()
            print(f"Model saved to: {final_path}")
            
            return final_path
            
        except Exception as e:
            print(f"Training error: {str(e)}")
            raise