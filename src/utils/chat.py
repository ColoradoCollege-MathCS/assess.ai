from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch
from pathlib import Path
import json
import threading
from datetime import datetime

class ChatBot:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.device = None
<<<<<<< HEAD
        self.current_model = None
        base_path = Path(__file__).parent
        self.model_files_path = base_path / "../../model_files"
        self.chat_history_path = None
        self._ensure_model_directories()
=======
        self.model_path = Path(__file__).parent / "../../model_files/pegasus"
        self.chat_history_path = Path("../chat_data/chat_history.txt")
        self._ensure_chat_directories()

    def _ensure_chat_directories(self):
        # Checks if chat history already exists. If it doesn't it creates one.
        self.chat_history_path.parent.mkdir(exist_ok=True)
        if not self.chat_history_path.exists():
            self.chat_history_path.write_text("")

    def _save_chat_entry(self, entry_data):
        # Save chat history in the background
        try:
            entry = {
                'timestamp': datetime.now().isoformat(),
                'data': entry_data,
                'type': 'chat_entry'
            }
            
            # Write to file in background
            def write_to_file():
                try:
                    with open(self.chat_history_path, 'a', encoding='utf-8') as f:
                        f.write(json.dumps(entry) + '\n')
                except Exception as e:
                    print(f"Failed to write chat entry: {str(e)}")
            
            threading.Thread(target=write_to_file, daemon=True).start()
                
        except Exception as e:
            print(f"Failed to save chat entry: {str(e)}")

    def load_chat_history(self, limit=None):
        entries = []
        try:
            with open(self.chat_history_path, 'r', 
                     encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            entry = json.loads(line.strip())
                            if entry['type'] == 'chat_entry':
                                entries.append(entry)
                        except json.JSONDecodeError:
                            continue
                                
            return entries
        except Exception as e:
            print(f"Failed to load chat history: {str(e)}")
            return []

>>>>>>> a0610ba1835c74dcf76d954652a1a43adb5e15a1


    # parents=True makes the necessary parent directories before mmaking subdirectories exist_ok=True doesn't throw an error if the folder exists, 
    def _ensure_model_directories(self):
        if not self.model_files_path.exists():
            self.model_files_path.mkdir(parents=True, exist_ok=True)

    def _ensure_chat_directories(self):
        if self.chat_history_path:
            self.chat_history_path.parent.mkdir(parents=True, exist_ok=True)
            if not self.chat_history_path.exists():
                self.chat_history_path.write_text("")

    def get_available_models(self):
        if not self.model_files_path.exists():
            return []
        # Iterate through all directories in model_files
        return [d.name for d in self.model_files_path.iterdir() if d.is_dir()]

    def set_model(self, model_name):
        try:
            self.current_model = model_name
            self.model_path = self.model_files_path / model_name
            self.chat_history_path = Path(__file__).parent / f"../../chat_data/{model_name}/chat_history.txt"
            # Check or create the chat history if it doesn't exist
            self._ensure_chat_directories()
            
            # Set new model
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(
                self.model_path,
                low_cpu_mem_usage=True
            )
            self.device = torch.device('cpu')
            self.model = self.model.to(self.device)
<<<<<<< HEAD
            return True
            
        except Exception as e:
            raise ValueError(f"Failed to set model {model_name}: {str(e)}")

    def _save_chat_entry(self, entry_data):
        # Save chat history in the background
        try:
            entry = {
                'timestamp': datetime.now().isoformat(),
                'data': entry_data,
                'type': 'chat_entry'
            }
            
            # Write to file in background
            def write_to_file():
                try:
                    with open(self.chat_history_path, 'a', encoding='utf-8') as f:
                        f.write(json.dumps(entry) + '\n')
                except Exception as e:
                    print(f"Failed to write chat entry: {str(e)}")
            
            threading.Thread(target=write_to_file, daemon=True).start()
                
        except Exception as e:
            print(f"Failed to save chat entry: {str(e)}")

    def load_chat_history(self, limit=None):
        if not self.chat_history_path:
            return []
            
        entries = []
        try:
            with open(self.chat_history_path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        try:
                            entry = json.loads(line.strip())
                            if entry['type'] == 'chat_entry':
                                entries.append(entry)
                        except json.JSONDecodeError:
                            continue
                                
            return entries
        except Exception as e:
            print(f"Failed to load chat history: {str(e)}")
            return []
            

    def get_response(self, user_input):
        if not self.current_model:
            raise ValueError("No model selected. Please select a model first.")
=======
        # else load selected model

    def get_response(self, user_input):
>>>>>>> a0610ba1835c74dcf76d954652a1a43adb5e15a1
            
        try:

            # Process input in smaller chunks if needed
            max_length = 1024
            # Implement chunking logic here. If the user sends a load higher than 1024, we process outputs in different batches.
            if len(user_input) > max_length:
                chunks = [user_input[i:i + max_length] for i in range(0, len(user_input), max_length)]
            else:
                chunks = [user_input]

            full_response = []
            for chunk in chunks:
                inputs = self.tokenizer(
                    chunk,
                    return_tensors="pt",
                    max_length=max_length,
                    truncation=True,
                    padding=True
                )
                inputs = {k: v.to(self.device) for k, v in inputs.items()}

                try:
                    # Don't track gradients when chatting to not affect model.
                    with torch.no_grad():
                        output_ids = self.model.generate(
                            **inputs,
                            max_length=512,
                            min_length=30,
                            num_beams=4,
                            length_penalty=2.0,
                            no_repeat_ngram_size=3,
                            early_stopping=True
                        )

                        decoded = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
                        if decoded:
                            full_response.append(decoded)

                except Exception as chunk_error:
                    print(f"Error processing chunk: {str(chunk_error)}")
                    continue

            if not full_response:
                return "I apologize, but I couldn't generate a proper response. Please try rephrasing your input."

            response = " ".join(full_response)
            
            # Save the chat entry after successful response generation
            self._save_chat_entry({
                'user_input': user_input,
                'ai_response': response
            })
            
            return response

        except Exception as e:
            print(f"Error in get_response: {str(e)}")
<<<<<<< HEAD
            return f"An error occurred: {str(e)}"
=======
            return f"An error occurred: {str(e)}"

>>>>>>> a0610ba1835c74dcf76d954652a1a43adb5e15a1
