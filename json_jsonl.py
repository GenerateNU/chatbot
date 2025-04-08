'''
json_to_jsonl.py
Convert a JSON file with pages array to JSONL format (one JSON object per line)
'''

import os
import json
import sys

def convert_json_to_jsonl(input_file, output_file=None):
    """
    Convert a JSON file to JSONL format.
    
    Parameters:
    input_file (str): Path to the input JSON file
    output_file (str, optional): Path to the output JSONL file. If not provided,
                                will use the same name as input_file but with .jsonl extension
    """
    # Determine output file path
    if not output_file:
        # Get the input file directory and base name
        input_dir = os.path.dirname(os.path.abspath(input_file))
        input_basename = os.path.basename(input_file)
        
        # Replace extension with .jsonl or add .jsonl if no extension
        base, ext = os.path.splitext(input_basename)
        output_basename = f"{base}.jsonl"
        
        # Construct full output path in the same directory as input
        output_file = os.path.join(input_dir, output_basename)
    
    try:
        print(f"Reading from: {input_file}")
        print(f"Writing to: {output_file}")
        
        # Ensure output directory exists
        output_dir = os.path.dirname(os.path.abspath(output_file))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Read the input JSON file
        with open(input_file, 'r', encoding='utf-8') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON in {input_file}: {e}")
                return False
        
        # Open the output file for writing
        with open(output_file, 'w', encoding='utf-8') as f:
            # Check if there's a 'pages' key in the JSON structure
            if 'pages' in data:
                # Process each page in the JSON
                count = 0
                for page in data['pages']:
                    for title, details in page.items():
                        # Create a new object combining title and details
                        jsonl_object = {
                            'title': title,
                            **details
                        }
                        
                        # Write each object as a separate line in JSONL format
                        f.write(json.dumps(jsonl_object, ensure_ascii=False) + '\n')
                        count += 1
                print(f"Converted {count} page entries to JSONL format")
            else:
                # If there's no 'pages' key, assume it's a different structure
                # Convert top-level objects as needed
                print("Warning: No 'pages' array found in JSON. Using alternative processing.")
                count = 0
                if isinstance(data, list):
                    # Handle array of objects
                    for item in data:
                        f.write(json.dumps(item, ensure_ascii=False) + '\n')
                        count += 1
                elif isinstance(data, dict):
                    # Handle dictionary of objects
                    for key, value in data.items():
                        if isinstance(value, dict):
                            # If value is a dict, include the key as a field
                            jsonl_object = {'id': key, **value}
                        else:
                            # Otherwise create a simple key-value pair
                            jsonl_object = {'key': key, 'value': value}
                        f.write(json.dumps(jsonl_object, ensure_ascii=False) + '\n')
                        count += 1
                print(f"Converted {count} entries to JSONL format")
        
        print(f"Successfully created JSONL file: {output_file}")
        return True
        
    except FileNotFoundError:
        print(f"Error: File not found: {input_file}")
    except PermissionError:
        print(f"Error: Permission denied when accessing {output_file}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    
    return False

def main():
    input_file = "training.json"
    output_file = "training.jsonl"

    # Check input file exists
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found.")
        return

    # Read the JSON file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {input_file}: {e}")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Process the data
    count = 0
    
    # Open the output file for writing
    with open(output_file, 'w', encoding='utf-8') as f:
        # Check if there's a 'pages' key in the JSON structure
        if 'pages' in data:
            # Process each page in the JSON
            for page in data['pages']:
                for title, details in page.items():
                    # Create a new object combining title and details
                    jsonl_object = {
                        'title': title,
                        **details
                    }
                    
                    # Write each object as a separate line in JSONL format
                    f.write(json.dumps(jsonl_object, ensure_ascii=False) + '\n')
                    count += 1
                    print(f"Processed: {title}")
        else:
            # If there's no 'pages' key, process the top-level elements
            print("Warning: No 'pages' array found in JSON. Using alternative processing.")
            
            if isinstance(data, list):
                # Handle array of objects
                for item in data:
                    f.write(json.dumps(item, ensure_ascii=False) + '\n')
                    count += 1
            elif isinstance(data, dict):
                # Handle dictionary of objects
                for key, value in data.items():
                    if isinstance(value, dict):
                        # If value is a dict, include the key as a field
                        jsonl_object = {'id': key, **value}
                    else:
                        # Otherwise create a simple key-value pair
                        jsonl_object = {'key': key, 'value': value}
                    f.write(json.dumps(jsonl_object, ensure_ascii=False) + '\n')
                    count += 1
    
    print(f"\nSuccess! Converted {count} entries from '{input_file}' to '{output_file}'")

if __name__ == "__main__":
    main()