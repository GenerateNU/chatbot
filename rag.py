from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import faiss
import numpy as np
import re

# Read the combined text from combined.txt
with open("combined.txt", "r", encoding="utf-8") as file:
    wiki_text = file.read()

# Create a text splitter (adjust chunk size and overlap as needed)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=650, chunk_overlap=150)
chunks = text_splitter.split_text(wiki_text)

# Load SentenceTransformer for embeddings
model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = [model.encode(chunk) for chunk in chunks]

# Create a FAISS index to store the embeddings
dimension = len(embeddings[0])
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))

def expand_to_sentence(text, start, end):
    """
    Expands the extracted answer to the full sentence by finding the nearest periods.
    """
    before = text.rfind('.', 0, start) + 1  # start of previous sentence
    after = text.find('.', end) + 1  # end of next sentence
    before = max(0, before)
    after = len(text) if after == 0 else after
    return text[before:after].strip()

def get_relevant_context(query, k=3):
    """
    Given a query, retrieves the most relevant context chunk from the combined wiki text.
    This function uses the FAISS index over text chunks and a QA model to pick the best matching chunk,
    then expands the answer to the full sentence.
    
    Args:
        query (str): The input query.
        k (int): Number of top chunks to retrieve.
    
    Returns:
        str: The expanded answer from the most relevant context chunk.
    """
    # Encode the query
    query_embedding = model.encode(query)
    query_vector = np.array([query_embedding])
    
    # Retrieve top k chunk indices
    distances, indices = index.search(query_vector, k=k)
    retrieved_texts = [chunks[i] for i in indices[0]]
    
    # Load QA model for evaluation on the retrieved chunks
    qa_pipeline = pipeline("question-answering", model="twmkn9/distilbert-base-uncased-squad2")
    
    best_answer = None
    best_score = float("-inf")
    best_chunk = None
    best_start = None
    best_end = None
    
    # Iterate over retrieved chunks to find the best answer
    for context in retrieved_texts:
        result = qa_pipeline(question=query, context=context)
        if result["score"] > best_score:
            best_score = result["score"]
            best_answer = result["answer"]
            best_chunk = context
            best_start = result["start"]
            best_end = result["end"]
        print(result)  # Debug output for each chunk's result
    
    # Expand the best answer to a full sentence for better clarity
    if best_chunk is not None:
        expanded_sentence = expand_to_sentence(best_chunk, best_start, best_end)
    else:
        expanded_sentence = "Sorry, no relevant context found."
    
    return expanded_sentence

# For testing purposes:
if __name__ == "__main__":
    query = "What is the purpose of the Flexible Spending Pool (FSP)?"
    context = get_relevant_context(query)
    print(f"Best Answer: {context}")
