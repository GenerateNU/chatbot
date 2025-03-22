'''
combine all text files in a folder, into one text file

run in your terminal as "python chatbot/combine_txt.py" to combine txt files
'''

import os

chatbot_folder = "chatbot"
input_folder = os.path.join(chatbot_folder, "wiki_txt")  # Folder containing txt files
output_file = os.path.join(chatbot_folder, "combined.txt")  # Save output in chatbot folder

# Ensure input folder exists
if not os.path.exists(input_folder):
    print(f"Error: Input folder '{input_folder}' does not exist.")
    exit(1)

# Open output file in write mode
with open(output_file, "w", encoding="utf-8") as outfile:
    for filename in sorted(os.listdir(input_folder)):  # Sort files alphabetically
        if filename.endswith(".txt"):
            file_path = os.path.join(input_folder, filename)
            with open(file_path, "r", encoding="utf-8") as infile:
                outfile.write(f"--- {filename} ---\n")  # Add filename as a separator
                outfile.write(infile.read() + "\n\n")  # Append content with spacing

print(f"All .txt files combined into: {output_file}")

