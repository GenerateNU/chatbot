import os
from markdown import markdown
from bs4 import BeautifulSoup
import urllib.parse

def extract_page(wiki_file):
    """
    Extracts Notion page names and it's Markdown filenames from the Wiki markdown file.
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

    # Create dictionary to store {Notion Page Name: Notion Page Link}
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

    # Convert Markdown to HTML, HTML to text
    html_content = markdown(notion_content)
    text = BeautifulSoup(html_content, "html.parser").get_text()

    return text

def extract_wiki(wiki_file, notion_folder):
    """
    Extracts Notion page names and their corresponding filenames from the Wiki markdown file,
    fetches the text from corresponding Notion markdown files, and prints them.
    """
    notion_pages = extract_page(wiki_file)

    for page_name, notion_filename in notion_pages.items():
        print(f"\n=== {page_name} ===\n")
        notion_text = extract_text(notion_folder, notion_filename)
        print(notion_text)
        print("\n" + "=" * 50)

wiki_file = "Wiki ab5f3792da934cca84cadb5381b1baec.md"
notion_folder = "Wiki Export"

wiki = extract_wiki(wiki_file, notion_folder)
