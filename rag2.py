"""
improved_json_rag.py
Enhanced RAG model for JSON wiki data with better context retrieval and answer extraction
"""

import os
import json
import numpy as np
import faiss
import re
import gc
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from transformers import pipeline, AutoTokenizer
import torch
from typing import List, Dict, Any, Tuple, Optional

# Set memory limits to prevent crashes
torch.set_num_threads(4)

class ImprovedJsonRAG:
    def __init__(self, 
                 json_file_path="gen_wiki.json", 
                 embedding_model_name="all-MiniLM-L6-v2",
                 qa_model_name="twmkn9/distilbert-base-uncased-squad2",
                 chunk_size=650, 
                 chunk_overlap=150):
        """
        Initialize the RAG model for JSON wiki data.
        
        Args:
            json_file_path: Path to the JSON wiki data
            embedding_model_name: Name of the SentenceTransformer model
            qa_model_name: Name of the QA model
            chunk_size: Size of text chunks
            chunk_overlap: Overlap between chunks
        """
        self.file_path = json_file_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_model_name = embedding_model_name
        self.qa_model_name = qa_model_name
        
        # Initialize text processing and models
        print(f"Loading and processing JSON data from {json_file_path}")
        self.wiki_text, self.structured_data = self.load_and_process_json()
        
        # Create chunks and index
        self.create_chunks_and_index()
        
        # Initialize QA pipeline
        print(f"Loading QA model: {qa_model_name}")
        self.qa_pipeline = pipeline("question-answering", model=qa_model_name)
        
    def load_and_process_json(self) -> Tuple[str, Dict]:
        """
        Load JSON data and extract content, handling multiple possible structures.
        
        Returns:
            Tuple of (combined text, structured data dictionary)
        """
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                try:
                    wiki_data = json.load(file)
                    print("Successfully loaded JSON data")
                except json.JSONDecodeError:
                    file.seek(0)
                    raw_text = file.read()
                    print("Warning: Could not parse JSON. Using raw text content.")
                    return raw_text, {"raw_content": raw_text}
        except FileNotFoundError:
            print(f"Error: File {self.file_path} not found.")
            return "", {}
            
        # Extract all text content from the structured JSON
        all_texts = []
        
        # Create a structured representation for lookup
        structured_data = {}
        
        # Process different JSON structures
        if isinstance(wiki_data, dict):
            # Case 1: Structure with "pages" key (from your example)
            if "pages" in wiki_data:
                for page_obj in wiki_data["pages"]:
                    for page_title, page_data in page_obj.items():
                        if isinstance(page_data, dict) and "content" in page_data:
                            all_texts.append(page_data["content"])
                            structured_data[page_title] = page_data
            # Case 2: Simple key-value structure
            else:
                for key, value in wiki_data.items():
                    if isinstance(value, dict) and "content" in value:
                        all_texts.append(value["content"])
                        structured_data[key] = value
                    elif key == "content" or key == "text":
                        all_texts.append(value)
                        structured_data["main"] = {"content": value}
        
        # Case 3: List of objects
        elif isinstance(wiki_data, list):
            for i, item in enumerate(wiki_data):
                if isinstance(item, dict):
                    item_key = item.get("title", f"item_{i}")
                    if "content" in item:
                        all_texts.append(item["content"])
                        structured_data[item_key] = item
                    elif "text" in item:
                        all_texts.append(item["text"])
                        structured_data[item_key] = item
                    
        # Combine all extracted texts
        combined_text = " ".join(all_texts) if all_texts else ""
        print(f"Extracted {len(all_texts)} content sections with a total of {len(combined_text)} characters")
            
        return combined_text, structured_data
    
    def create_chunks_and_index(self):
        """Create text chunks, generate embeddings, and build the FAISS index."""
        # Split text into chunks with improved chunking strategy
        print(f"Splitting text into chunks (size={self.chunk_size}, overlap={self.chunk_overlap})")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size, 
            chunk_overlap=self.chunk_overlap,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        self.chunks = text_splitter.split_text(self.wiki_text)
        print(f"Created {len(self.chunks)} chunks")
        
        # Initialize embedding model
        print(f"Loading embedding model: {self.embedding_model_name}")
        self.embedding_model = SentenceTransformer(self.embedding_model_name)
        
        # Generate embeddings in batches to save memory
        print("Generating embeddings...")
        batch_size = 32
        all_embeddings = []
        
        for i in range(0, len(self.chunks), batch_size):
            end_idx = min(i + batch_size, len(self.chunks))
            batch = self.chunks[i:end_idx]
            batch_embeddings = self.embedding_model.encode(batch, show_progress_bar=False)
            all_embeddings.append(batch_embeddings)
            gc.collect()  # Force garbage collection
            
        # Concatenate all batches
        embeddings_np = np.vstack(all_embeddings)
        
        # Create FAISS index
        print("Building FAISS index...")
        self.dimension = embeddings_np.shape[1]
        self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(embeddings_np)
        
        # Clear embeddings from memory
        del all_embeddings
        gc.collect()
        
    def preprocess_query(self, query: str) -> str:
        """Clean and preprocess the query."""
        # Remove multiple spaces and normalize whitespace
        query = re.sub(r'\s+', ' ', query).strip()
        
        # Add question mark if it's likely a question but doesn't have one
        if (query.lower().startswith("what") or
            query.lower().startswith("who") or
            query.lower().startswith("when") or
            query.lower().startswith("where") or
            query.lower().startswith("why") or
            query.lower().startswith("how")) and not query.endswith("?"):
            query += "?"
            
        return query
    
    def retrieve_relevant_chunks(self, query: str, k: int = 3) -> List[Tuple[str, float]]:
        """
        Retrieve the k most relevant chunks for the given query.
        
        Args:
            query: The preprocessed query
            k: Number of chunks to retrieve
            
        Returns:
            List of (chunk_text, relevance_score) tuples
        """
        # Encode the query
        query_embedding = self.embedding_model.encode(query)
        query_vector = np.array([query_embedding]).astype('float32')
        
        # Retrieve top k chunks
        distances, indices = self.index.search(query_vector, k=k)
        
        # Convert distances to similarity scores (higher is better)
        similarity_scores = [1.0 / (1.0 + float(dist)) for dist in distances[0]]
        
        # Get chunks with their scores
        retrieved_chunks = [(self.chunks[int(idx)], score) 
                          for idx, score in zip(indices[0], similarity_scores)]
        
        return retrieved_chunks
    
    def keyword_reranking(self, query: str, chunks: List[Tuple[str, float]]) -> List[Tuple[str, float]]:
        """
        Rerank chunks based on keyword matching.
        
        Args:
            query: The query string
            chunks: List of (chunk_text, score) tuples
            
        Returns:
            Reranked list of chunks
        """
        # Extract keywords from query (simple approach)
        query_terms = set(query.lower().split())
        query_terms = {term for term in query_terms 
                     if term not in {"what", "where", "when", "why", "how", "is", "are", "the", "a", "an"}}
        
        # Rerank based on keyword presence
        reranked_chunks = []
        for chunk, score in chunks:
            chunk_lower = chunk.lower()
            
            # Count exact matches
            exact_matches = sum(term in chunk_lower for term in query_terms)
            
            # Check for presence of adjacent terms (bi-grams)
            bigram_matches = 0
            if len(query_terms) > 1:
                query_text = query.lower()
                for i in range(len(query_text) - 1):
                    bigram = query_text[i:i+2]
                    if len(bigram.strip()) > 1 and bigram in chunk_lower:
                        bigram_matches += 1
            
            # Combine original score with keyword matching
            adjusted_score = score + (exact_matches * 0.05) + (bigram_matches * 0.03)
            reranked_chunks.append((chunk, adjusted_score))
        
        # Sort by adjusted score
        reranked_chunks.sort(key=lambda x: x[1], reverse=True)
        return reranked_chunks
    
    def expand_to_sentence(self, text: str, start: int, end: int) -> str:
        """
        Expand answer span to full sentences for better context.
        
        Args:
            text: Source text
            start: Start position of answer
            end: End position of answer
            
        Returns:
            Expanded answer text
        """
        # Find sentence boundaries
        sentence_start = max(0, text.rfind('.', 0, start) + 1)
        sentence_end = text.find('.', end)
        
        if sentence_end == -1:
            sentence_end = len(text)
        else:
            sentence_end += 1
        
        # Clean up the expanded text
        expanded = text[sentence_start:sentence_end].strip()
        
        # Handle cases where expansion doesn't result in complete sentences
        if not expanded.endswith('.'):
            expanded += '.'
            
        return expanded
    
    def extract_answer(self, query: str, chunks: List[Tuple[str, float]]) -> Dict[str, Any]:
        """
        Extract the best answer from the retrieved chunks.
        
        Args:
            query: The question
            chunks: List of (chunk_text, score) tuples
            
        Returns:
            Dictionary with answer and metadata
        """
        best_answer = None
        best_score = -1
        best_chunk = None
        best_chunk_score = 0
        best_start, best_end = None, None
        
        # Process chunks with QA model
        for chunk, chunk_score in chunks:
            # Skip empty chunks
            if not chunk.strip():
                continue
                
            # Truncate long chunks to prevent issues
            if len(chunk) > 1000:
                chunk = chunk[:1000]
                
            try:
                # Apply QA model
                result = self.qa_pipeline(question=query, context=chunk)
                
                # Calculate combined score (weight QA confidence more)
                combined_score = (0.3 * chunk_score) + (0.7 * result["score"])
                
                if combined_score > best_score:
                    best_score = combined_score
                    best_answer = result["answer"]
                    best_chunk = chunk
                    best_chunk_score = chunk_score
                    best_start = result["start"]
                    best_end = result["end"]
                    
            except Exception as e:
                print(f"Error in QA pipeline: {e}")
                continue
                
        # Return result
        if best_answer is None:
            return {
                "answer": "Sorry, I couldn't find relevant information to answer that question.",
                "score": 0,
                "context": "",
                "chunk_score": 0
            }
        
        # Expand to full sentence(s)
        expanded_answer = self.expand_to_sentence(best_chunk, best_start, best_end)
        
        return {
            "answer": expanded_answer,
            "original_answer": best_answer,
            "score": best_score,
            "context": best_chunk,
            "chunk_score": best_chunk_score
        }
    
    def answer_question(self, query: str, k: int = 3, use_reranking: bool = True) -> Dict[str, Any]:
        """
        End-to-end pipeline to answer a question.
        
        Args:
            query: The question to answer
            k: Number of chunks to retrieve initially
            use_reranking: Whether to use keyword-based reranking
            
        Returns:
            Dict with answer and metadata
        """
        # Preprocess the query
        clean_query = self.preprocess_query(query)
        
        # Retrieve relevant chunks
        chunks = self.retrieve_relevant_chunks(clean_query, k=k)
        
        # Apply reranking if enabled
        if use_reranking and len(chunks) > 1:
            chunks = self.keyword_reranking(clean_query, chunks)
        
        # Extract the best answer
        result = self.extract_answer(clean_query, chunks)
        
        return result

# Example usage
if __name__ == "__main__":
    import time
    start_time = time.time()
    
    # Initialize the RAG system
    rag = ImprovedJsonRAG(json_file_path="gen_wiki.json")
    
    # Example query
    query = "What is Generate's values?"
    print("\n" + "="*80)
    print(f"QUERY: {query}")
    print("="*80)
    
    # Get answer
    result = rag.answer_question(query, k=3, use_reranking=True)
    
    # Print results
    print(f"ANSWER: {result['answer']}")
    print(f"CONFIDENCE: {result['score']:.4f}")
    print(f"CHUNK RELEVANCE: {result['chunk_score']:.4f}")
    print("-"*40)
    print(f"CONTEXT SNIPPET:\n{result['context'][:300]}...")
    
    # Print timing information
    print("\nProcessing time: {:.2f} seconds".format(time.time() - start_time))
    
    # Clean up
    del rag
    gc.collect()