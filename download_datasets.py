import json
import csv
import os
import re
from datasets import load_dataset

def clean_text(text):
    """Clean the text by removing extra whitespace and special characters."""
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def create_cnn_dailymail_files():
    """
    Fetch the CNN/DailyMail dataset and save it in different formats
    compatible with the project.
    """
    print("Loading CNN/DailyMail dataset from Hugging Face...")
    
    # Load a subset of the dataset (you can adjust the number of examples)
    dataset = load_dataset("cnn_dailymail", "3.0.0", split="test[:1000]")
    
    # Prepare the data in the format required by the project
    formatted_data = []
    
    print("Processing dataset...")
    count = 0
    total = len(dataset)
    
    for item in dataset:
        # Clean the article and highlights
        article = clean_text(item['article'])
        summary = clean_text(item['highlights'])
        
        # Format data according to project requirements
        formatted_item = {
            "input_text": article,
            "target_text": summary
        }
        
        formatted_data.append(formatted_item)
        
        # Simple progress update
        count += 1
        if count % 100 == 0:
            print(f"Processed {count}/{total} samples")
    
    num_samples = len(formatted_data)
    print(f"Processed {num_samples} samples")
    
    # Create JSON file
    json_file_path = "cnn_dailymail.json"
    print(f"Creating JSON file: {json_file_path}")
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(formatted_data, json_file)
    
    # Create CSV file
    csv_file_path = "cnn_dailymail.csv"
    print(f"Creating CSV file: {csv_file_path}")
    with open(csv_file_path, 'w', encoding='utf-8', newline='') as csv_file:
        fieldnames = ['input_text', 'target_text']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for item in formatted_data:
            writer.writerow(item)
    
    # Create TXT file
    txt_file_path = "cnn_dailymail.txt"
    print(f"Creating TXT file: {txt_file_path}")
    with open(txt_file_path, 'w', encoding='utf-8') as txt_file:
        for item in formatted_data:
            txt_file.write(f"INPUT: {item['input_text']}\n")
            txt_file.write(f"TARGET: {item['target_text']}\n\n")
    
    print("\nData files created successfully!")
    print(f"Number of examples: {num_samples}")
    print("\nFiles generated:")
    print(f"- JSON: {json_file_path}")
    print(f"- CSV: {csv_file_path}")
    print(f"- TXT: {txt_file_path}")
    
    print("\nTo use these files with your project:")
    print("1. Select the appropriate file format")
    print("2. Configure the dataset path in your application")
    print("3. Set appropriate start_idx and end_idx values based on how many samples you want to process")

if __name__ == "__main__":
    # Check for required libraries
    try:
        import datasets
    except ImportError:
        print("Missing required libraries. Installing...")
        import subprocess
        subprocess.check_call(["pip", "install", "datasets"])
        
    create_cnn_dailymail_files()