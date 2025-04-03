'''
rag_ollama.py 
Uses JSON as a knowledge base to feed into a RAG and Ollama model.
User inputs a question, model returns an answer based on the context.
''' 

from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import requests
import json
import os
import time

# Configuration
OLLAMA_ENDPOINT = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral" 
# llama3.2 model returns good answer, although model may be too big 
# mistral model returns good answer, more concise and faster, need to check model size
EMBEDDINGS_CACHE_FILE = "json_embeddings_cache.npz"
CHUNKS_METADATA_FILE = "chunks_metadata.json"
KNOWLEDGE_BASE_FILE = "gen_wiki.json"
CHUNK_SIZE = 650
CHUNK_OVERLAP = 150

# Function to load and prepare chunks from JSON knowledge base
def load_and_prepare_chunks():
    """Load JSON data, split it into chunks, and cache embeddings for faster startup"""
    print("Loading and preparing chunks from JSON knowledge base...")
    
    # Read the JSON knowledge base
    try:
        with open(KNOWLEDGE_BASE_FILE, "r", encoding="utf-8") as file:
            knowledge_base = json.load(file)
    except FileNotFoundError:
        print(f"Error: Knowledge base file '{KNOWLEDGE_BASE_FILE}' not found.")
        return [], None
    
    # Create chunks with metadata
    chunks = []
    chunks_metadata = []
    
    for title, entry in knowledge_base.items():
        # Extract text content for embedding
        text_parts = []
        
        # Add title as part of content
        text_parts.append(title)
        
        # Add metadata fields that might be useful for searching
        if "author" in entry:
            text_parts.append(f"Author: {entry['author']}")
        
        if "tags" in entry:
            text_parts.append(f"Tags: {entry['tags']}")
            
        # Add the main content
        if "content" in entry:
            text_parts.append(entry["content"])
        
        # Combine all text parts
        full_text = "\n".join(text_parts)
        
        # Split text into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE, 
            chunk_overlap=CHUNK_OVERLAP
        )
        entry_chunks = text_splitter.split_text(full_text)
        
        # Store chunks and their metadata
        for chunk in entry_chunks:
            chunks.append(chunk)
            # Store metadata to know which entry this chunk belongs to
            chunks_metadata.append({
                "title": title,
                "chunk_text": chunk[:50] + "...",  # Store preview for debugging
                "source": title
            })
    
    # Check if embeddings cache exists
    if os.path.exists(EMBEDDINGS_CACHE_FILE) and os.path.exists(CHUNKS_METADATA_FILE):
        print("Loading embeddings from cache...")
        try:
            cache = np.load(EMBEDDINGS_CACHE_FILE)
            embeddings = cache['embeddings']
            
            # Load chunks metadata
            with open(CHUNKS_METADATA_FILE, "r", encoding="utf-8") as f:
                loaded_chunks_metadata = json.load(f)
                
            # Verify cache matches current chunks
            if len(loaded_chunks_metadata) == len(chunks):
                chunks_metadata = loaded_chunks_metadata
            else:
                print("Cache metadata doesn't match current chunks. Regenerating embeddings...")
                embeddings = generate_embeddings(chunks)
                save_cache(embeddings, chunks_metadata)
        except Exception as e:
            print(f"Error loading cache: {e}. Regenerating embeddings...")
            embeddings = generate_embeddings(chunks)
            save_cache(embeddings, chunks_metadata)
    else:
        print("Generating embeddings (this might take a while)...")
        embeddings = generate_embeddings(chunks)
        save_cache(embeddings, chunks_metadata)
    
    # Create a FAISS index for efficient similarity search
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    
    print(f"Prepared {len(chunks)} chunks with dimension {dimension}")
    return chunks, chunks_metadata, index

def generate_embeddings(chunks):
    """Generate embeddings for chunks using SentenceTransformer"""
    # Initialize the embedding model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    
    # Generate embeddings in batches to save memory
    batch_size = 32
    embeddings = []
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        batch_embeddings = model.encode(batch)
        embeddings.extend(batch_embeddings)
        print(f"Processed {i+len(batch)}/{len(chunks)} chunks")
    
    # Convert to numpy array
    return np.array(embeddings)

def save_cache(embeddings, chunks_metadata):
    """Save embeddings and chunks metadata to cache files"""
    np.savez(EMBEDDINGS_CACHE_FILE, embeddings=embeddings)
    with open(CHUNKS_METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks_metadata, f, ensure_ascii=False, indent=2)

# Global variables to store loaded data
print("Initializing JSON-based RAG system...")
chunks, chunks_metadata, index = load_and_prepare_chunks()
# Keep embedding model loaded for queries
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
print("RAG system ready!")

def query_ollama(query, context, max_tokens=250):
    """Send a query to Ollama with relevant context and get the response"""
    try:
        prompt = f"""
You are a helpful assistant and innovative friend named genny for Generate Product Development Studio at Northeastern University. 
Answer the following question based on the provided context. Be concise but informative. 
You are allowed to be personal by aligning yourself with Generate's mission and values.
If the context doesn't contain the answer, say so.

Context:
{context}

Question: {query}

Answer:
"""
        
        payload = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.1,
                "num_predict": max_tokens
            }
        }
        
        response = requests.post(OLLAMA_ENDPOINT, json=payload, timeout=30)
        if response.status_code == 200:
            result = response.json()
            return result.get("response", "Sorry, I couldn't generate a response.")
        else:
            print(f"Error from Ollama API: {response.text}")
            return "I'm having trouble connecting to my knowledge base. Please try again later."
    
    except Exception as e:
        print(f"Exception when calling Ollama: {e}")
        return "Sorry, I encountered an error while processing your question."

def get_relevant_context(query, k=3):
    """
    Get most relevant context chunks and use Ollama to generate an answer
    """
    try:
        # Clean the query if it starts with "!"
        if query.startswith("!"):
            query = query[1:].strip()
        
        # Encode the query
        query_embedding = embedding_model.encode(query)
        query_vector = np.array([query_embedding])
        
        # Retrieve top k chunks from FAISS index
        distances, indices = index.search(query_vector, k=k)
        
        # Prepare context with source information
        context_parts = []
        sources_set = set()  # Track unique sources
        
        for i, idx in enumerate(indices[0]):
            chunk_text = chunks[idx]
            source = chunks_metadata[idx]["title"]
            sources_set.add(source)
            
            # Add source information to the context
            context_parts.append(f"--- From: {source} ---\n{chunk_text}")
        
        # Combine the chunks into a single context (with length limit)
        combined_context = "\n\n".join(context_parts)
        if len(combined_context) > 2000:
            combined_context = combined_context[:2000] + "..."
        
        # Add sources summary
        sources_list = list(sources_set)
        sources_summary = f"\nInformation sourced from: {', '.join(sources_list)}"
        
        # Use Ollama to generate the answer
        response = query_ollama(query, combined_context)
        
        # Add sources to response if needed
        # response += sources_summary
        
        return response
        
    except Exception as e:
        print(f"Error in get_relevant_context: {e}")
        return "Sorry, I encountered an error while processing your question."

# Example usage for testing rag.py:
if __name__ == "__main__":
    test_queries = [
        "What is Generate's mission?",
        "How do I get access to the space?",
        "When is the next showcase?",
        "What are some morale budget ideas?",
        "Tell me about team engagement activities"
    ]
    
    for query in test_queries:
        print(f"\nQuestion: {query}")
        start_time = time.time()
        answer = get_relevant_context(query)
        end_time = time.time()
        print(f"Answer: {answer}")
        print(f"Time taken: {end_time - start_time:.2f} seconds")