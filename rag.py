from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import faiss
import numpy as np
import re

with open("combined.txt", "r", encoding="utf-8") as file:
    wiki_text = file.read()

<<<<<<< HEAD
text_splitter = RecursiveCharacterTextSplitter(chunk_size=650, chunk_overlap=150)
=======
text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
>>>>>>> 29af43c09000932430aadce02411e424632a1f59
chunks = text_splitter.split_text(wiki_text)

# client = OpenAI() 
model = SentenceTransformer('all-MiniLM-L6-v2')  # Small, fast, and accurate, embedding tool
embeddings = [model.encode(chunk) for chunk in chunks]
# embeddings = [client.embeddings.create(input=chunk, model="text-embedding-ada-002") for chunk in chunks]

dimension = len(embeddings[0])  # Get embedding size
index = faiss.IndexFlatL2(dimension) # store faiss data?
index.add(np.array(embeddings))


################################ Testing random queries
<<<<<<< HEAD
query = "git commit vs git push"
query_embedding = model.encode(query)
query_vector = np.array([query_embedding])
distances, indices = index.search(query_vector, k=3)  # Retrieve top 3 results
retrieved_texts = [chunks[i] for i in indices[0]]
=======
def expand_to_sentence(text, start, end):
    """
    Expands the extracted answer to the full sentence by finding the nearest periods.
    """
    before = text.rfind('.', 0, start) + 1  # Start of previous sentence
    after = text.find('.', end) + 1  # End of next sentence
>>>>>>> 29af43c09000932430aadce02411e424632a1f59

    # Ensure valid indices
    before = max(0, before)
    after = len(text) if after == 0 else after

    return text[before:after].strip()

# Load QA model
qa_pipeline = pipeline("question-answering", model="twmkn9/distilbert-base-uncased-squad2")

query = "What are Generate's mission?" ## need to make this a function to pass in new question
query_embedding = model.encode(query)
query_vector = np.array([query_embedding])

# Retrieve top 3 results
distances, indices = index.search(query_vector, k=3)
retrieved_texts = [chunks[i] for i in indices[0]]

best_index = 0
best_answer = None
best_score = float("-inf")
best_start = None
best_end = None

for i, context in enumerate(retrieved_texts):
    result = qa_pipeline(question=query, context=context)

    # Track the best scoring result
    if result["score"] > best_score:
        best_index = i
        best_score = result["score"]
        best_answer = result["answer"]
        best_start = result["start"]
        best_end = result["end"]

    print(result)

# Expand answer to full sentence
expanded_sentence = expand_to_sentence(retrieved_texts[best_index], best_start, best_end) # This is what you want to pass in as context for qa model

print(f"Best Answer: {best_answer} (Confidence: {best_score:.4f})")
print(f"Expanded Sentence: {expanded_sentence}") 
