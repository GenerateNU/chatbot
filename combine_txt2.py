'''
combine all text files in a folder, into one text file

run in your terminal as "python chatbot/combine_txt.py" to combine txt files

everything combine_txt.py does, but with a few more features:
- makes everything lowercase
- remove special characters
- tokenize the text
'''

import os
import re

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

script_dir = os.path.dirname(os.path.abspath(__file__))
input_folder = os.path.join(script_dir, "Wiki_txt") # Folder containing .txt files
output_file = os.path.join(script_dir, "combined4.txt") # Store combined.txt in same folder
#combined.txt - original combined file
#combined2_tokens.txt - new combined file with tokens
#combined3.txt - no tokens
#combined4.txt - no tokens, keep periods

# Ensure input folder exists
if not os.path.exists(input_folder):
    print(f"Error: Input folder '{input_folder}' does not exist.")
    exit(1)

# Count total files
txt_files = [f for f in os.listdir(input_folder) if f.endswith('.txt')]
print(f"Found {len(txt_files)} text files to process")

# Open output file in write mode
with open(output_file, "w", encoding="utf-8") as outfile:
    for filename in sorted(os.listdir(input_folder)):  # Sort files alphabetically
        if filename.endswith(".txt"):
            file_path = os.path.join(input_folder, filename)
            print(f"\nProcessing file: {filename}")  # Debug print
            with open(file_path, "r", encoding="utf-8") as infile:
                clean_lines = []
                line_count = 0
                for line in infile:
                    line_count += 1
                    stripped = line.strip()
                    if not stripped:
                        continue  # Skip empty lines
                    # if stripped.startswith("---"):
                    #     continue  # Skip title lines
                    if stripped.startswith(("Author:", "Hidden:", "Sub-page:", "Parent Page:")):
                        continue  # Skip author and hidden lines
                    
                    # Clean the line
                    # line = re.sub(r"\*\*\*(.*?)\*\*\*", r"\1", line)  # remove ***bold italic***
                    # line = re.sub(r"\*\*(.*?)\*\*", r"\1", line)      # remove **bold**
                    # line = re.sub(r"\*(.*?)\*", r"\1", line)          # remove *italic*
                    line = remove_emojis(line) # remove emojis
                    line = line.lower() # make everything lowercase
                    line = re.sub(r"[^a-zA-Z0-9\s.]", "", line) # remove special characters, keep periods
                    #tokens = word_tokenize(line)
                    clean_lines.append(line)
                
                if clean_lines:  # Only write if we have clean lines
                    outfile.writelines(clean_lines)
                    print(f"Processed {line_count} lines, kept {len(clean_lines)} lines")

print(f"\nAll .txt files combined into: {output_file}")

