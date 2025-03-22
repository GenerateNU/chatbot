import os
from markdown import markdown
from bs4 import BeautifulSoup
import urllib.parse

# create string of file names
# rename files through a number, make a counter to loop
# make a df, or list
# start with 5 files first
# try irelevant questions as well


def extract_page(wiki_file):
    """
    Extracts Notion page names and its Markdown filenames from the Wiki markdown file.
    Returns a dictionary {Notion page name: Markdown filename}.
    """
    with open(wiki_file, "r", encoding="utf-8") as file:
        md_content = file.read()

    # Convert Markdown to HTML
    html_content = markdown(md_content)

    # Parse HTML and extract links
    soup = BeautifulSoup(html_content, "html.parser")
    links = soup.find_all("a")

    notion_pages = {}

    # Create a dictionary to store {Notion Page Name: Notion Page Link}
    for link in links:
        page_name = link.text.strip()
        file_path = link.get("href")

        if file_path:
            decoded_filename = urllib.parse.unquote(os.path.basename(file_path))
            notion_pages[page_name] = decoded_filename

    return notion_pages

def extract_text(notion_folder, notion_page):
    """
    Reads a Notion-exported markdown file, converts it to plain text,
    and returns the cleaned content.
    """
    notion_file = os.path.join(notion_folder, notion_page)

    if not os.path.exists(notion_file):
        return f"⚠️ Error: '{notion_page}' not found."

    with open(notion_file, "r", encoding="utf-8") as file:
        notion_content = file.read()

    # Convert Markdown to HTML, then HTML to text
    html_content = markdown(notion_content)
    text = BeautifulSoup(html_content, "html.parser").get_text()

    return text

def extract_wiki(wiki_file, notion_folder):
    """
    Extracts Notion page names and their corresponding filenames from the Wiki markdown file,
    fetches the text from corresponding Notion markdown files, and organizes the content in a dictionary.
    """
    notion_pages = extract_page(wiki_file)
    
    wiki_content = {}
    
    # Extract and organize the content for each page
    for page_name, notion_filename in notion_pages.items():
        notion_text = extract_text(notion_folder, notion_filename)
        wiki_content[page_name] = notion_text
        
    return wiki_content

# Example usage (for testing purposes):
if __name__ == "__main__":
    wiki_file = "Wiki ab5f3792da934cca84cadb5381b1baec.md"  # Path to your exported wiki markdown file
    notion_folder = "Wiki Export"  # Folder containing the Notion markdown files

    # Extract the wiki data
    wiki_data = extract_wiki(wiki_file, notion_folder)

    # Print the extracted data (for testing purposes)
    for page_name, content in wiki_data.items():
        print(f"\n=== {page_name} ===\n")
        print(content)
        print("\n" + "=" * 50)