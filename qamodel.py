from transformers import pipeline

# Load DistilBERT model for question answering
qa_pipeline = pipeline("question-answering", model="twmkn9/distilbert-base-uncased-squad2")

def answer_question(question, wiki_data):
    """
    Given a query and the wiki data (context), fetch the answer using DistilBERT QA model.
    
    Args:
        question (str): The question to be answered.
        wiki_data (dict): A dictionary with Notion page names as keys and their corresponding content as values.
    
    Returns:
        str: The answer to the query based on the wiki data.
    """
    # Iterate over each page in the wiki data to check for a match
    for page_name, context in wiki_data.items():
        print(f"=== Searching in: {page_name} ===")
        
        # Ask the question using the current page's content as context
        result = qa_pipeline(question=question, context=context)  # Change query to question here

        if result['answer']:
            print(f"Answer found in '{page_name}': {result['answer']}")
            return result['answer']  # Return the first match found
    
    # If no answer is found in any of the pages, return a default message
    return "Sorry, I couldn't find an answer in the wiki."

def test_qa_model(wiki_data):
    """
    Function to run a few simple test questions on the QA model and print the answers.
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
        answer = answer_question(question, wiki_data)
        print(f"Answer: {answer}")
        print("="*50)

# Example usage (for testing purposes):
if __name__ == "__main__":
    wiki_file = "Wiki ab5f3792da934cca84cadb5381b1baec.md"  # Path to your exported wiki markdown file
    notion_folder = "Wiki Export"  # Folder containing the Notion markdown files

    # Extract the wiki data
    from parser import extract_wiki
    wiki_data = extract_wiki(wiki_file, notion_folder)

    # Run the tests
    test_qa_model(wiki_data)