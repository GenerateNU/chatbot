'''
wiki_json.py
combine all text files in a folder, turns it into a json file
'''

import os
import re
import json

def remove_emojis(text):
    '''function to remove emojis from text'''
    emoji = re.compile(
        "["
        "\U0001F1E6-\U0001F1FF"  # Flags
        "\U0001F300-\U0001F5FF"  # Symbols & pictographs
        "\U0001F600-\U0001F64F"  # Emoticons
        "\U0001F680-\U0001F6FF"  # Transport & map symbols
        "\U0001F700-\U0001F77F"  # Alchemical symbols
        "\U0001F780-\U0001F7FF"  # Geometric shapes extended
        "\U0001F800-\U0001F8FF"  # Supplemental arrows-C
        "\U0001F900-\U0001F9FF"  # Supplemental symbols and pictographs
        "\U0001FA00-\U0001FA6F"  # Chess symbols, etc.
        "\U0001FA70-\U0001FAFF"  # Symbols and pictographs extended-A
        "\U00002700-\U000027BF"  # Dingbats
        "\U00002600-\U000026FF"  # Misc symbols
        "\U000024C2-\U0001F251"
        "]+",
        flags=re.UNICODE,
    )
    return emoji.sub(r'', text)

def remove_markdown(text):
    """Remove markdown formatting"""
    # Remove common markdown patterns
    text = re.sub(r"\*\*\*(.*?)\*\*\*", r"\1", text)  # ***bold italic***
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)      # **bold**
    text = re.sub(r"\*(.*?)\*", r"\1", text)          # *italic*
    text = re.sub(r"\_\_(.*?)\_\_", r"\1", text)      # __underline__
    text = re.sub(r"\_(.*?)\_", r"\1", text)          # _italic_
    text = re.sub(r"\~\~(.*?)\~\~", r"\1", text)      # ~~strikethrough~~
    #text = re.sub(r"\`(.*?)\`", r"\1", text)          # `code`
    
    # Remove markdown links - replace [text](url) with just text
    text = re.sub(r"\[(.*?)\]\(.*?\)", r"\1", text)
    
    # Remove HTML-style tags
    text = re.sub(r"<.*?>", "", text)
    
    return text

def clean_text(text):
    """Apply all text cleaning operations"""
    text = remove_emojis(text)
    text = remove_markdown(text)
    # Remove multiple spaces and newlines
    text = re.sub(r'\n\s*\n', '\n\n', text)
    text = re.sub(r' +', ' ', text)
    return text.strip()

def process_wiki_file(file_path):
    """Process a single wiki text file and extract its information"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    lines = content.split('\n')
    if not lines:
        return None
    
    # First line is the title and should be the key
    title = lines[0].strip()
    if not title:
        return None
    
    # Process metadata and content
    metadata = {}
    content_lines = []
    content_started = False
    
    for i, line in enumerate(lines):
        # Skip the title line
        if i == 0:
            continue
            
        # Check if this is a metadata line (key: value)
        if ':' in line and not content_started:
            parts = line.split(':', 1)
            key = parts[0].strip().lower()
            value = parts[1].strip()
            
            # Clean the value
            value = clean_text(value)
            
            if key and value:
                metadata[key] = value
                
            # If we've processed 'tags' metadata, content might start next
            if key == 'tags':
                content_started = True
        elif line.strip():
            # This is likely content
            content_started = True
            clean_line = clean_text(line)
            if clean_line:
                content_lines.append(clean_line)
    
    # Join content lines
    content_text = '\n'.join(content_lines)
    
    # Combine metadata and content
    result = metadata.copy()
    if content_text:
        result['content'] = content_text
    
    return {title: result}

def main():
    folder = "Wiki_txt"
    output_file = "gen_wiki.json"

    # Check input folder exists
    if not os.path.exists(folder):
        print(f"Error: Folder '{folder}' not found.")
        return

    knowledge_base = {}

    for filename in os.listdir(folder):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder, filename)
            result = process_wiki_file(file_path)
            if result:
                knowledge_base.update(result)
                print(f"Processed: {filename}")
    
    # Save to JSON file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(knowledge_base, f, indent=2, ensure_ascii=False)
    
    print(f"\nSuccess! Combined {len(knowledge_base)} wiki entries into '{output_file}'")

if __name__ == "__main__":
    main()

