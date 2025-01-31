# Assess.ai
Team Members: Ronan Takizawa, Kaylie Stuteville, Willa Polman, Anna Vu.

A Python-based chat interface using the Pegasus model from HuggingFace Transformers.

https://github.com/user-attachments/assets/82a473e8-4ae2-4352-b59b-a112da76b475



## Features
- Text Summarization with Pegasus LLM
- Chat history storage 
- Finetune models 
- Model Evaluation
## Installation

1. Clone this repository:
```bash
git clone https://github.com/ColoradoCollege-MathCS/assess.ai
cd assess.ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Setup and Usage

1. Download the required model first (this is required before first run):
```bash
cd src
python download_pegasus.py
```

2. Start the application:
```bash
python main.py
```

