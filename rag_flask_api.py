"""
rag_flask_api.py
Flask API for RAG system with LLM integration
"""

import os
import json
import time
import gc
import psutil
from typing import List, Dict, Any, Optional

# Flask imports
from flask import Flask, request, jsonify

# Import the RAG system
try:
    from rag2 import ImprovedJsonRAG
except ImportError:
    # Fallback assuming JSON handling is part of your other RAG implementation
    from improved_rag import ImprovedRAG

# Importing necessary libraries for the LLM
import torch
import transformers
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

# Set globally to limit memory usage
torch.set_num_threads(4)  # Limit CPU threads
# Disable parallelism in transformers
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Create Flask app
app = Flask(__name__)

# Add memory monitoring functions
def get_memory_usage():
    """Get current memory usage of the process in MB."""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    memory_mb = memory_info.rss / (1024 * 1024 * 1024)  # Convert to GB
    return memory_mb

def print_memory_usage(label=""):
    """Print current memory usage."""
    memory_mb = get_memory_usage()
    app.logger.info(f"Memory usage {label}: {memory_mb:.2f} GB")

class LightweightRAGAssistant:
    def __init__(
        self,
        knowledge_file: str = "gen_wiki.json",
        model_name: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0",  # Smallest model by default
        device: str = "cpu",  # Use CPU by default for Mac stability
        chunk_size: int = 650,
        chunk_overlap: int = 150,
        context_chunks: int = 3,
        max_new_tokens: int = 256,
        temperature: float = 0.7,
    ):
        """
        Initialize the lightweight RAG + LLM assistant.
        
        Args:
            knowledge_file: Path to knowledge base file
            model_name: Name of LLM (use smaller models)
            device: Device to run on (cpu recommended for stability)
            chunk_size: Size of text chunks for RAG
            chunk_overlap: Overlap between chunks
            context_chunks: Number of chunks to retrieve
            max_new_tokens: Maximum tokens in generated response
            temperature: Temperature for text generation
        """
        self.device = device
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature
        self.context_chunks = context_chunks
        
        print_memory_usage("at start")
        
        # Initialize RAG system
        app.logger.info(f"Initializing RAG system with {knowledge_file}")
        try:
            # Try to use JSON-specific RAG if available
            if knowledge_file.endswith('.json'):
                self.rag = ImprovedJsonRAG(
                    json_file_path=knowledge_file,
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap
                )
            else:
                # Fall back to text-based RAG
                self.rag = ImprovedRAG(
                    file_path=knowledge_file,
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap
                )
        except Exception as e:
            app.logger.error(f"Error initializing RAG: {e}")
            raise
            
        print_memory_usage("after RAG init")
        
        # Initialize LLM components
        self._initialize_llm(model_name)
        
        # Conversation history (limited size)
        self.conversation_history = {}
        self.max_history_turns = 3  # Limit history to save memory
        
        print_memory_usage("after initialization")
        
    def _initialize_llm(self, model_name: str):
        """Initialize language model with memory-efficient settings."""
        try:
            app.logger.info(f"Loading language model: {model_name}")
            
            # Extra configurations to reduce memory usage
            config = transformers.AutoConfig.from_pretrained(model_name)
            
            # 8-bit loading if available
            try:
                import bitsandbytes as bnb
                has_8bit = True
            except ImportError:
                has_8bit = False
                
            # Configure tokenizer to avoid warnings and save memory
            tokenizer_kwargs = {
                "padding_side": "left",
                "truncation_side": "left",
            }
            
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name, 
                use_fast=True,
                **tokenizer_kwargs
            )
            
            # Load model with memory optimizations
            app.logger.info("Loading model with optimizations for memory efficiency")
            
            model_kwargs = {
                "device_map": "auto" if self.device == "cuda" else None,
                "low_cpu_mem_usage": True,
            }
            
            # Add quantization if available
            if has_8bit and self.device == "cuda":
                model_kwargs["load_in_8bit"] = True
            
            self.model = AutoModelForCausalLM.from_pretrained(
                model_name,
                config=config,
                **model_kwargs
            )
            
            # Move to CPU if specified
            if self.device == "cpu":
                self.model = self.model.to("cpu")
                
            # Set up text generation pipeline
            self.text_generation = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=-1 if self.device == "cpu" else 0
            )
            
            # Set up model-specific tokens
            if "llama" in model_name.lower():
                self.system_prefix = "<s>[INST] "
                self.prompt_prefix = "[INST] "
                self.response_prefix = " [/INST]"
                self.suffix = "</s>"
            elif "mistral" in model_name.lower():
                self.system_prefix = "<s>[INST] "
                self.prompt_prefix = "[INST] "
                self.response_prefix = " [/INST]"
                self.suffix = "</s>"
            elif "gemma" in model_name.lower():
                self.system_prefix = "<start_of_turn>user\n"
                self.prompt_prefix = "<start_of_turn>user\n"
                self.response_prefix = "<end_of_turn>\n<start_of_turn>model\n"
                self.suffix = "<end_of_turn>"
            else:
                # Generic tokens
                self.system_prefix = "### System:\n"
                self.prompt_prefix = "### User:\n"
                self.response_prefix = "\n### Assistant:\n"
                self.suffix = ""
                
            app.logger.info(f"Model loaded successfully on {self.device}")
            
        except Exception as e:
            app.logger.error(f"Error loading language model: {e}")
            import traceback
            traceback.print_exc()
            raise
            
        # Force garbage collection
        gc.collect()
        print_memory_usage("after LLM loading")
        
    def format_prompt(self, query: str, context: str, session_id: str = "default") -> str:
        """Format the prompt for the LLM with system instructions and context."""
        # System instruction
        system_instruction = f"""
        You are an expert LLM chatbot named Genny, designed to help answer questions about a club at Northeastern University called Generate. For each inquiry, you will be given a snippet of relevant context to answer the question. Use the context and any previous knowledge to answer the inquiry as accurate as possible. 
        """
        
        # Format conversation history if available
        history_text = ""
        if session_id in self.conversation_history and self.conversation_history[session_id]:
            # Keep only recent history to save context length
            recent_history = self.conversation_history[session_id][-self.max_history_turns:]
            for turn in recent_history:
                history_text += f"User asked: {turn['user']}\nYou answered: {turn['assistant']}\n\n"
        
        # Construct the full prompt
        full_prompt = (
            f"{system_instruction}\n\n"
            f"{history_text}"
            f"Here is some relevant context information:\n{context}\n\n"
            f"Please answer this question based on the context: {query}"
        )
        
        return full_prompt
        
    def generate_response(self, prompt: str) -> str:
        """Generate a response from the LLM using the formatted prompt."""
        try:
            # Format for the specific model
            formatted_prompt = f"{self.prompt_prefix}{prompt}{self.response_prefix}"
            
            # Generate text with minimal parameters to save memory
            response = self.text_generation(
                formatted_prompt,
                max_new_tokens=self.max_new_tokens,
                temperature=self.temperature,
                do_sample=True,
                num_return_sequences=1,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            # Extract generated text
            generated_text = response[0]['generated_text']
            
            # Extract the response portion
            response_text = generated_text.split(self.response_prefix)[-1]
            
            # Clean up the response
            if self.suffix and self.suffix in response_text:
                response_text = response_text.split(self.suffix)[0]
                
            # Trim any leading/trailing whitespace
            response_text = response_text.strip()
            
            return response_text
            
        except Exception as e:
            app.logger.error(f"Error in text generation: {e}")
            return "I'm sorry, I encountered an error while generating a response."
        finally:
            # Force garbage collection after generation
            gc.collect()
            
    def answer_question(self, query: str, session_id: str = "default") -> Dict[str, Any]:
        """
        Process a user query through RAG and LLM to generate an answer.
        
        Args:
            query: User's question
            session_id: Unique identifier for the conversation session
            
        Returns:
            Dictionary with answer and metadata
        """
        start_time = time.time()
        print_memory_usage("before processing query")
        
        try:
            # Step 1: Get relevant context using RAG
            app.logger.info(f"Retrieving context for: {query}")
            if hasattr(self.rag, 'answer_question'):
                # Use the RAG's answer_question method if available
                rag_result = self.rag.answer_question(query, k=self.context_chunks)
                context = rag_result.get('context', '')
            else:
                # Fall back to find_context_window
                contexts = self.rag.find_context_window(query, top_k=self.context_chunks)
                context = " ".join([ctx for ctx, _ in contexts])
            
            app.logger.info(f"Retrieved {len(context)} characters of context")
            print_memory_usage("after RAG retrieval")
            
            # Step 2: Format the prompt with the context
            prompt = self.format_prompt(query, context, session_id)
            
            # Step 3: Generate response with the LLM
            app.logger.info("Generating response from LLM...")
            response = self.generate_response(prompt)
            print_memory_usage("after LLM generation")
            
            # Step 4: Update conversation history
            if session_id not in self.conversation_history:
                self.conversation_history[session_id] = []
                
            self.conversation_history[session_id].append({
                "user": query,
                "assistant": response
            })
            
            # Limit history size to control memory usage
            if len(self.conversation_history[session_id]) > self.max_history_turns:
                self.conversation_history[session_id] = self.conversation_history[session_id][-self.max_history_turns:]
            
            # Calculate processing time
            processing_time = time.time() - start_time
            
            return {
                "answer": response,
                "context_snippet": context[:200] + "..." if len(context) > 200 else context,
                "processing_time": processing_time
            }
            
        except Exception as e:
            app.logger.error(f"Error processing query: {e}")
            import traceback
            traceback.print_exc()
            
            return {
                "answer": "I'm sorry, I encountered an error while processing your question.",
                "error": str(e),
                "processing_time": time.time() - start_time
            }
        finally:
            # Force garbage collection
            gc.collect()
            print_memory_usage("after query processing")
    
    def reset_conversation(self, session_id: str = "default"):
        """Reset the conversation history to free memory."""
        if session_id in self.conversation_history:
            self.conversation_history[session_id] = []
        gc.collect()
        app.logger.info(f"Conversation history has been reset for session {session_id}")
        print_memory_usage("after reset")

# Initialize the RAG assistant as a global variable
# This will be loaded when the server starts
assistant = None

def init_assistant(knowledge_file="gen_wiki.json", model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
    """Initialize the RAG assistant."""
    global assistant
    try:
        assistant = LightweightRAGAssistant(
            knowledge_file=knowledge_file,
            model_name=model_name
        )
        return True
    except Exception as e:
        app.logger.error(f"Error initializing assistant: {e}")
        return False

# API Routes
@app.route("/ask", methods=["GET", "POST"])
def ask_question():
    """
    API endpoint that takes a query as input and returns the answer.
    """
    global assistant
    
    # Ensure assistant is initialized
    if assistant is None:
        return jsonify({"error": "RAG assistant not initialized"}), 500
    
    # Get the query from request
    if request.method == "GET":
        query = request.args.get("query")
        session_id = request.args.get("session_id", "default")
    elif request.method == "POST":
        data = request.get_json()
        query = data.get("query")
        session_id = data.get("session_id", "default")
    else:
        return jsonify({"error": "Method not allowed"}), 405

    if not query:
        return jsonify({"error": "No query provided"}), 400

    # Process the query
    app.logger.info(f"Processing query for session {session_id}: {query}")
    result = assistant.answer_question(query, session_id)
    
    # Return the answer
    return jsonify({
        "query": query,
        "answer": result["answer"],
        "context_snippet": result.get("context_snippet", ""),
        "processing_time": result.get("processing_time", 0)
    })

@app.route("/reset", methods=["POST"])
def reset_session():
    """
    Reset the conversation history for a session.
    """
    global assistant
    
    # Ensure assistant is initialized
    if assistant is None:
        return jsonify({"error": "RAG assistant not initialized"}), 500
    
    # Get session ID
    data = request.get_json() or {}
    session_id = data.get("session_id", "default")
    
    # Reset the conversation
    assistant.reset_conversation(session_id)
    
    return jsonify({
        "success": True,
        "message": f"Conversation history reset for session {session_id}"
    })

@app.route("/test", methods=["GET"])
def test():
    """Test endpoint to verify the API is working."""
    return jsonify({"out": "Working"})

@app.route("/memory", methods=["GET"])
def memory():
    """Return current memory usage."""
    mem_usage = get_memory_usage()
    return jsonify({
        "memory_usage_gb": mem_usage,
        "uptime": time.time() - start_time
    })

# Initialize server
if __name__ == "__main__":
    import argparse
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="RAG API Server")
    parser.add_argument("--knowledge", default="gen_wiki.json", help="Path to knowledge base file")
    parser.add_argument("--model", default="TinyLlama/TinyLlama-1.1B-Chat-v1.0", 
                        help="Model to use (default: TinyLlama-1.1B-Chat)")
    parser.add_argument("--port", type=int, default=6000, help="Port to run the server on")
    parser.add_argument("--host", default="0.0.0.0", help="Host to run the server on")
    parser.add_argument("--debug", action="store_true", help="Run in debug mode")
    args = parser.parse_args()
    
    # Print system information
    print(f"Python version: {os.sys.version}")
    print(f"PyTorch version: {torch.__version__}")
    print(f"Transformers version: {transformers.__version__}")
    print(f"CPU count: {os.cpu_count()}")
    print(f"Torch threads: {torch.get_num_threads()}")
    
    try:
        # Import psutil for memory monitoring
        import psutil
        total_memory = psutil.virtual_memory().total / (1024 * 1024 * 1024)  # GB
        print(f"System memory: {total_memory:.1f} GB")
    except:
        print("Psutil not available, memory monitoring limited")
    
    # Track server start time
    start_time = time.time()
    
    # Initialize the assistant
    print(f"Initializing assistant with model: {args.model}")
    success = init_assistant(args.knowledge, args.model)
    
    if success:
        print(f"Starting server on {args.host}:{args.port}, debug={args.debug}")
        app.run(host=args.host, port=args.port, debug=args.debug)
    else:
        print("Failed to initialize assistant. Exiting.")