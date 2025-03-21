'''
convert md files to txt files in a folder

run in your terminal as "python md_to_txt.py" to convert md files to txt files
'''
import os
import markdown
from bs4 import BeautifulSoup

folder_path = "Wiki Export"

# Create new output folder, folder will be created within the folder path (Wiki Export)
output_folder = os.path.join(folder_path, "Wiki_txt")
os.makedirs(output_folder, exist_ok=True)

# Convert each .md file to .txt
for filename in os.listdir(folder_path):
    if filename.endswith(".md"):
        md_path = os.path.join(folder_path, filename)
        txt_path = os.path.join(output_folder, filename.replace(".md", ".txt"))

        # Read md file
        with open(md_path, "r", encoding="utf-8") as md_file:
            md_content = md_file.read()

        # Convert md to HTML, then extract text
        html_content = markdown.markdown(md_content)
        soup = BeautifulSoup(html_content, "html.parser")
        plain_text = soup.get_text(separator="\n")  # Preserve newlines

        # Write to a new .txt file
        with open(txt_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(plain_text)

print("Conversion completed! Check the 'Wiki_txt' folder.")
