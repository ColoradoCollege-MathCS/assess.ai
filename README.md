# medscribe.ai
Repo for Medscribe.ai 
Team Members: Ronan Takizawa, Kaylie Stuteville, Willa Polman, Anna Vu.

A Python-based chat interface for local LLMs using GPT4All, featuring chat history persistence and loading animations.

## Installation

1. Clone this repository:
```bash
git clone https://github.com/ColoradoCollege-MathCS/medscribe.ai
cd medscribe.ai
```

2. Install required dependencies:
```bash
pip install gpt4all
```

3. Create a `models` directory and place your LLM model file inside:
```bash
mkdir models
# Place your .gguf model file in the models directory
```

## Usage

1. Run the script:
```bash
python main.py
```

2. Start chatting with the AI:
- Type your message and press Enter
- Wait for the AI to respond (loading animation will show)
- Type 'exit' to quit the program

3. Chat history will be automatically saved to `chat_history.txt`

## File Structure

```
.
├── main.py              # Main script file
├── models/              # Directory for LLM models
│   └── [your-model].gguf
├── chat_history.txt     # Stored chat history
├── README.md           # This file
└── CHANGELOG.md        # Version history
```

## Chat History Format

Chat history is stored in `chat_history.txt` with the following format:
```
[YYYY-MM-DD HH:MM:SS] User: [user message]
[YYYY-MM-DD HH:MM:SS] AI: [AI response]
--------------------------------------------------
```
