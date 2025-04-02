from transformers import pipeline
from rag import get_relevant_context

# (Optional) You can load QA model here if you need to run it separately,
# but our get_relevant_context function already uses qa_pipeline internally.

def answer_question_using_rag(query):
    """
    Uses the RAG retrieval process (from rag.py) to obtain the most relevant context
    and returns that as the answer.
    
    Args:
        query (str): The user's question.
    
    Returns:
        str: The best answer (expanded sentence) from the retrieved context.
    """
    # Retrieve the most relevant context chunk using our rag function
    context = get_relevant_context(query)
    return context

def test_qa_model():
    """
    Runs a series of test questions through the integrated RAG + QA pipeline and prints the answers.
    """
    test_questions = [
        "What factors should you consider when selecting electrical components?",
        "What is the price range for electrical components?",
        "What is bare-metal programming?",
        "What is the difference between a bare MCU and a carrier board?",
        "What is the purpose of the Flexible Spending Pool (FSP)?"
    ]
    
    for question in test_questions:
        print(f"Question: {question}")
        answer = answer_question_using_rag(question)
        print(f"Answer: {answer}")
        print("=" * 50)

if __name__ == "__main__":
    test_qa_model()
