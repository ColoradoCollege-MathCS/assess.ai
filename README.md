# AssessAI
Team Members: Ronan Takizawa, Kaylie Stuteville, Willa Polman, Anna Vu.

AssessAI is a desktop software tool designed to help users evaluate and test the performance of large language models (LLMs) specifically in summarizing custom datasets. The tool allows clients to upload their datasets and assess how well various LLMs summarize their content. With this, users can determine how effectively these models could potentially serve their own projects.


https://github.com/user-attachments/assets/82a473e8-4ae2-4352-b59b-a112da76b475



## Features
- Load Huggingface models
- Finetune models with summarization dataset
- Model Evaluation (ROUGE, BLEU, METEOR)
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

1. Download the required model first (this is required before first run to do G-EVAL):
```bash
cd src
python download_mistral.py
```

2. Start the application:
```bash
python main.py
```

