# Genny - Generate Slack Chatbot

## Operations - Data Solutions - Internal Insights Spring 2025

### Chigozirim Ike, Matthew Li, Kaydence Lin

The purpose of the chatbot, Genny, is to streamline the process of gathering organization wide information for answering internal questions in real-time.
This documentation is for internal Generate members who may implement or work on the chatbot in the future.
Knowledge of Python, Slack APIs, LLM, RAG, Hugging Face, and Digital Ocean may be useful to understand this documentation.

## Technical Details

### Data

The data that was used was an export of the Generate Notion Wiki (folder named "Wiki Export"). The export contained markdown files of each page. To preprocess this data, we converted all the .md into .txt files (md_to_txt.py). The text files are stored in a folder called "Wiki_txt". We cleaned the .txt files to delete any unnecessary md formatting, emojis, and empty lines and combined all the .txt files to a .json file (wiki_json.py and gen_wiki.json). The gen_wiki.json was used as the knowledge base for the models.

#### Training Data

We created training data with Question-Answer pairs called training.json. This data encompasses content that can be found in Generate's Notion and was manually created.
We created a parser to convert the .json to .jsonl file (json_jsonl.py and training.jsonl). We found that the training.jsonl worked better for the DistilBERT model. This data was not used for the RAG.

### Models

#### Introduction

Throughout the semester, we created and experimented with different LLM models to find one that works the best. We initially tried the rag.py, however, it did not work well because the responses were not great and had a low confidence score. Currently, we found that rag3.py works well and returns great responses, however, it is a very powerful model and requires a lot of computing resources, which is the current problem and limitation we are facing.

#### rag3.py

The rag3.py is our ideal LLM model for the final chatbot. It does not run on a M1 Mac Pro with 8GB of memory. It may run on a M1 Mac Pro with 16 GB of memory, however, it runs very slowly, and it may not run depending on the available memory on the local machine. If you are taking an LLM class, you may have access to a GPU you can run this on, it will be much faster. We successfully ran this on a GPU with 48 GB of memory. Comments regarding how the code works are within the file. If you have more questions, try running the code through Claude.ai first or reach out to us.

#### rag.py

This file is legacy code. It was the first implementation of our rag model, which originally used combined.txt as the knowledge base. We improved to use the JSON knowledge base in rag2.py.

#### rag_ollama.py

The file is an implementation of a RAG + Ollama model. To use Ollama, please download Ollama https://ollama.com/ and install the mistral model using "ollama pull mistral" in the terminal. This model uses an RAG and feeds it into an Ollama model. This model produces good responses, however, after initial research, Ollama is not meant to be deployed, but only to be used on your local machine. Ollama is also an API. This model is easy to run on your local machine, so it is a good example of what the chatbot responses should look like.

#### training.py

The `training.py` file is responsible for fine-tuning the DistilBERT model using the training.jsonl file. It tokenizes the data, sets up a Trainer pipeline, and saves the trained model checkpoints.

The process includes:
1. Loading the training.jsonl file using the Hugging Face `datasets` library.
2. Tokenizing the data with `distilbert-base-uncased`.
3. Training the model using the Hugging Face `Trainer` API.
4. Saving the model and evaluation logs to an output folder.

## User Guide 

### Slack

To test our model and implementation, we created a new Slack channel separate from the Sherman Center. 
1. Create a Slack App at https://api.slack.com/apps
   - Disable Socket Mode
   - Add bot token scopes: `app_mentions:read`, `channels:history`, `channels:read`, `chat:write`, `chat:write.public`, `groups:history`, `groups:read`, `im:history`, `im:read`, `im:write`, `incoming-webhook`, `mpim:history`, `users:read`
   - Install the app to your workspace

### Environment
libraries needed
  pip install RecursiveCharacterTextSplitter SentenceTransformer numpy faiss-cpu torch
  pip install -r requirements.txt

### DigitalOcean

[DigitalOcean]([url](https://www.digitalocean.com/?utm_campaign=search_us_en_brand&utm_adgroup=brand_do&utm_keyword=digital%20ocean&utm_matchtype=p&utm_adposition=&utm_creative=743532792446&utm_placement=&utm_device=c&utm_location=&utm_location=9001992&utm_term=digital%20ocean&utm_source=google&utm_medium=cpc&gad_source=1&gclid=CjwKCAjw8IfABhBXEiwAxRHlsEV4IY7H41KmyrD9ny5l46WbvNRqCOMvpfBgOGIcV3yuby95FX0mzBoCyIsQAvD_BwE)) is a platform that we decided to use for hosting. There are two components that need to be hosted. First, there is the Slack backend, which can be found in the app.py file. You can host this by creating a App Platform. Once this is done, you will have to change the event subscription link within the slack api website. The second aspect is hosting the model. We were originally going to run an LLM on top of our RAG model to produce conversational answers using the relavant text generated by the RAG model. We were exploring using droplets, but unfortunately the resources that we chose were not enough to run the LLM for the cost. This is something that needs to be looked at. GPU droplets or a higher spec droplets could work. There is also a GenAI Platform on DigitalOcean that we did not look at.

## Final Product

The end goal for our final product is to use the rag3.py LLM model and deploy it through a Slackbot for Generate users to access the chatbot, Genny.

## Maintenance and Updates

Currently, rag3.py is too resource-intensive. The next steps are to figure out a less resource-intensive solution or request more money to be able to host with adequate computing resources (more RAM).

## Potential Future Work

1. Create an API with Notion SDK to integrate with the Generate Notion and create a dynamic knowledge base
2. Integrate with the Notion Calendar and automate reminders for events
3. Automate reminders for team meetings
4. Integrate with Slack message history to return more personalized answers

## Contact Information

| Name         | Email Address            | Role         | Date of Last Edit |
| ------------ | ------------------------ | ------------ | ----------------- |
| Chigozirim Ike    | ike.c@northeastern.edu   | Data Analyst | 4/18/2025         |
| Matthew Li   | li.matt@northeastern.edu | Data Analyst | 4/18/2025         |
| Kaydence Lin | lin.kay@northeastern.edu | Data Analyst | 4/18/2025         |
