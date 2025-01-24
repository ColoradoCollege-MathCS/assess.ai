# medscribe.ai
Repo for Medscribe.ai 
Team Members: Ronan Takizawa, Kaylie Stuteville, Willa Polman, Anna Vu.

A Python-based chat interface using the Pegasus model from HuggingFace Transformers, featuring secure chat history persistence and a modern user interface.

## Features
- Secure password protection for chat history
- Modern, responsive GUI using tkinter
- Encrypted chat history storage
- Asynchronous message processing
- Rate limiting and DoS protection

## Installation

1. Clone this repository:
```bash
git clone https://github.com/ColoradoCollege-MathCS/medscribe.ai
cd medscribe.ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Setup and Usage

1. Download the required model first (this is required before first run):
```bash
python download_model.py
```

2. Start the application:
```bash
python main.py
```

3. Enter your password in the login screen
4. Start chatting with the AI:
   - Type your message and press Enter or click the send button
   - Wait for the AI response
   - Messages are automatically saved and encrypted

Note: The first time you run the application, it will create necessary secure directories and encryption keys.

## Security Features
- Password-based encryption
- Secure chat history storage
- Access logging
- Rate limiting
- DoS protection
- Memory usage monitoring

## Important Notes
- Make sure to run `download_model.py` before first use of the application
- The Pegasus model download may take some time depending on your internet connection
- The model files will be stored locally after download