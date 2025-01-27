# Assess.ai
Team Members: Ronan Takizawa, Kaylie Stuteville, Willa Polman, Anna Vu.

A Python-based chat interface using the Pegasus model from HuggingFace Transformers.

https://github.com/user-attachments/assets/82a473e8-4ae2-4352-b59b-a112da76b475



## Features
- Text Summarization with Pegasus LLM
- Chat history storage (Currently not encrypted)
- 
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

Note: The first time you run the application, it will create necessary secure directories and encryption keys.

## Important Notes
- This app follows best practices of HIPAA compliant applications, but is not HIPAA compliant.
- Make sure to run `download_model.py` before first use of the application
