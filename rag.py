from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import faiss
import numpy as np

with open("combined.txt", "r", encoding="utf-8") as file:
    wiki_text = file.read()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=650, chunk_overlap=150)
chunks = text_splitter.split_text(wiki_text)

# client = OpenAI() 
model = SentenceTransformer('all-MiniLM-L6-v2')  # Small, fast, and accurate, embedding tool
embeddings = [model.encode(chunk) for chunk in chunks]
# embeddings = [client.embeddings.create(input=chunk, model="text-embedding-ada-002") for chunk in chunks]

dimension = len(embeddings[0])  # Get embedding size
index = faiss.IndexFlatL2(dimension) # store faiss data?
index.add(np.array(embeddings))


################################ Testing random queries
query = "git commit vs git push"
query_embedding = model.encode(query)
query_vector = np.array([query_embedding])
distances, indices = index.search(query_vector, k=3)  # Retrieve top 3 results
retrieved_texts = [chunks[i] for i in indices[0]]

qa_pipeline = pipeline("question-answering", model="twmkn9/distilbert-base-uncased-squad2")

best_answer = None
best_score = float("-inf")

for context in retrieved_texts:
    result = qa_pipeline(question=query, context=context)

    # Check if this result has the highest confidence score
    if result["score"] > best_score:
        best_score = result["score"]
        best_answer = result["answer"]
    print(result)

print(f"Best Answer: {best_answer} (Confidence: {best_score:.4f})")