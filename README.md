## AssessAI
Team Members: Ronan Takizawa, Kaylie Stuteville, Willa Polman, Anna Vu.

AssessAI is a desktop software tool designed to help users evaluate and test the performance of large language models (LLMs) specifically in summarizing custom datasets. The tool allows clients to upload their datasets and assess how well various LLMs summarize their content. With this, users can determine how effectively these models could potentially serve their own projects.

https://github.com/user-attachments/assets/f7ffeffc-5cc3-40f8-82a3-7846976aca34


## Features
- Load Huggingface models
- Finetune models with summarization dataset
- Model Evaluation (ROUGE, BLEU, METEOR)

## Prerequisites
- Python 3.8 to 3.11
- git
- Minimum: 8GB RAM, Recommended: 16GB RAM
- Storage: 10GB+ free space
- CPU: Multi-core processor supporting AVX2 instructions (AVX2 instructions are used in llama.cpp to run mistral-7B)
- Text summarization datasets in “input_text” “target_text” format

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



## Capstone Poster

![new_new_poster](https://github.com/user-attachments/assets/fb0964d7-3173-4d2f-ae8e-0ac75174e592)




