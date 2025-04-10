'''
rag.py
original rag model
'''

from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import faiss
import numpy as np
import re

# Read the combined wiki text
with open("combined.txt", "r", encoding="utf-8") as file:
    wiki_text = file.read()

# Set up the text splitter: adjust chunk size and overlap as needed
text_splitter = RecursiveCharacterTextSplitter(chunk_size=650, chunk_overlap=150)
chunks = text_splitter.split_text(wiki_text)

# Initialize the embedding model (SentenceTransformer)
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = [model.encode(chunk) for chunk in chunks]

# Create a FAISS index for efficient similarity search
dimension = len(embeddings[0])
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

def expand_to_sentence(text, start, end):
    """
    Expands an extracted answer to the full sentence by locating the nearest periods.
    """
    before = text.rfind('.', 0, start) + 1  # Start index of the sentence
    after = text.find('.', end) + 1         # End index of the sentence
    before = max(0, before)
    after = len(text) if after == 0 else after
    return text[before:after].strip()

def get_relevant_context(query, k=3):
    """
    Given a query, retrieves the most relevant context chunk from the combined wiki text.
    Uses SentenceTransformer to encode the query, then FAISS to retrieve the top k chunks.
    Finally, it applies the QA model on these chunks and expands the best answer to a full sentence.
    
    Args:
        query (str): The input question.
        k (int): Number of top chunks to retrieve.
    
    Returns:
        str: The expanded answer from the best matching context.
    """
    # Encode the query
    query_embedding = model.encode(query)
    query_vector = np.array([query_embedding])
    
    # Retrieve top k chunks from FAISS index
    distances, indices = index.search(query_vector, k=k)
    retrieved_texts = [chunks[i] for i in indices[0]]
    
    # Load QA model for evaluating each chunk
    qa_pipeline = pipeline("question-answering", model="twmkn9/distilbert-base-uncased-squad2")
    
    best_answer = None
    best_score = float("-inf")
    best_index = None
    best_start, best_end = None, None
    
    # Evaluate each retrieved chunk with the QA model
    for i, context in enumerate(retrieved_texts):
        result = qa_pipeline(question=query, context=context)
        if result["score"] > best_score:
            best_score = result["score"]
            best_answer = result["answer"]
            best_index = i
            best_start = result["start"]
            best_end = result["end"]
        print(result)  # Debug: print each chunk's result
    
    if best_index is not None:
        expanded_sentence = expand_to_sentence(retrieved_texts[best_index], best_start, best_end)
        return expanded_sentence
    else:
        return "Sorry, I couldn't find relevant context."

# Example usage for testing rag.py:
if __name__ == "__main__":
    query = "What are Generate's mission?"
    context = get_relevant_context(query)
    print(f"Best Answer: {context}")
