from transformers import PegasusForConditionalGeneration, PegasusTokenizer
import torch
import os
from pathlib import Path

class ChatBot:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.device = None
        self.model_path = Path(__file__).parent / "../model_files" 

    def _load_model(self):
        if self.model is None:
            self.tokenizer = PegasusTokenizer.from_pretrained(self.model_path)
            self.model = PegasusForConditionalGeneration.from_pretrained(self.model_path)
            self.device = torch.device('cpu')
            self.model = self.model.to(self.device)

    def get_response(self, user_input):
        if not user_input.strip():
            return "Please enter a message."
            
        try:
            if self.model is None:
                self._load_model()

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

            return " ".join(full_response)

        except Exception as e:
            print(f"Error in get_response: {str(e)}")
            return f"An error occurred: {str(e)}"
            