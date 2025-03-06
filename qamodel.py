from transformers import pipeline

# Load DistilBERT model for question answering
qa_pipeline = pipeline("question-answering", model="twmkn9/distilbert-base-uncased-squad2")


# Define context
context = """
Generate is under the Sherman Center, whose values must align with three core values—being developmental, inclusive, and intentional.
In addition, Generate members are innovative, driven, empathetic, spirited, and growth-oriented.
"""

# Ask a question
question = "What are the values of Generate?"

# Get the answer
result = qa_pipeline(question=question, context=context)

# Print the answer
print(f"Answer: {result['answer']}")
