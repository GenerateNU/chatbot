# Genny - Generate Chatbot
### Operations - Data Solutions - Internal Insights
### Spring 2025
### Chigo Ike, Matthew Li, Kaydence Lin
The purpose of the chatbot is to streamline the process of gathering organization wide information for answering internal questions in real-time.
This documentation is for internal Generate members who may implement or work on the chatbot in the future.
Knowledge of Python, APIs, LLM, Hugging Face, and Digital Ocean may be useful to understand this documentation.

## Setup - matthew
### Slack
1. Create a Slack App at https://api.slack.com/apps
   - Enable Socket Mode
   - Add bot token scopes: `chat:write`, `app_mentions:read`, `channels:history`, `im:history`
   - Install the app to your workspace

2. Set up your environment:
xyz

### DigitalOcean
xyz

## Data
The data that was used was an export of the Generate Notion Wiki (folder named "Wiki Export"). The export contained markdown files of each page. To preprocess this data, we converted all the .md into .txt files (md_to_txt.py). The text files are stored in a folder called "Wiki_txt". We cleaned the .txt files to delete any unnecessary md formatting, emojis, and empty lines and combined all the .txt files to a .json file (wiki_json.py and gen_wiki.json). The gen_wiki.json was used as the knowledge base for the models. 

### Training Data
We created training data with Question-Answer pairs called training.json. This data encompasses content that can be found in Generate's Notion and was manually created.
We created a parser to convert the .json to .jsonl file (json_jsonl.py and training.jsonl). We found that the training.jsonl worked better for the DistilBERT model. This data was not used for the RAG.
- xyz, fix and clean

## Models
### Introduction
- we initially tried the rag.py, didnt work well
- rag3.py works well
- xyz - talk about other limitations and processes to reach final stage

### rag3.py - Matthew
- doesnt run on a M1 Mac Pro with 8GB of memory
- runs on a M1 Mac Pro with 16 GB of memory, however it runs very slow 
- if taking an LLM class, you may have access to a GPU you can run this on, it will be much faster
xyz

### rag.py - matthew
xyz

### rag_ollama.py - edit this, kaydence
- download ollama and models
- uses a RAG and feeds it into Ollama
- Ollama produces good responses, however, after initial research Ollama isn't meant to be deployed, only to use on your local machine
- this model is a good example of what the chatbot responses should look like


