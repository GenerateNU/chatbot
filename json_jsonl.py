'''
json_to_jsonl.py
Convert a JSON file with Questions array to JSONL format (one JSON object per line)
'''

import os
import json
import sys

def convert_json_to_jsonl(input_file, output_file=None, ignore_keys=None):
    """
    Convert a JSON file to JSONL format with one dictionary per line.
    
    Parameters:
    input_file (str): Path to the input JSON file
    output_file (str, optional): Path to the output JSONL file. If not provided,
                                will use the same name as input_file but with .jsonl extension
    ignore_keys (list, optional): List of keys to ignore when processing the JSON objects
    """
    # Set default for ignore_keys if not provided
    if ignore_keys is None:
        ignore_keys = []
    
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
            count = 0
            
            # Process based on data structure
            if isinstance(data, list):
                # Handle list of dictionaries - each dictionary will be one line
                for item in data:
                    if isinstance(item, dict):
                        # Remove any keys to ignore
                        for key in ignore_keys:
                            if key in item:
                                del item[key]
                        
                        # Write the full dictionary as a line
                        f.write(json.dumps(item, ensure_ascii=False) + '\n')
                        count += 1
                
            elif isinstance(data, dict):
                # Special case for a dictionary with "Questions" as a list
                if 'Questions' in data and isinstance(data['Questions'], list):
                    for item in data['Questions']:
                        if isinstance(item, dict):
                            # Remove any keys to ignore
                            for key in ignore_keys:
                                if key in item:
                                    del item[key]
                            
                            # Write the full dictionary as a line
                            f.write(json.dumps(item, ensure_ascii=False) + '\n')
                            count += 1
                
                # Special case for a dictionary with "value" as a list of items with "id"
                elif 'key' in data and 'value' in data and isinstance(data['value'], list):
                    for item in data['value']:
                        if isinstance(item, dict):
                            # Remove any keys to ignore
                            for key in ignore_keys:
                                if key in item:
                                    del item[key]
                            
                            # Write the dictionary as a line
                            f.write(json.dumps(item, ensure_ascii=False) + '\n')
                            count += 1
                
                # Check if there's a 'pages' key in the dictionary
                elif 'pages' in data and isinstance(data['pages'], list):
                    # Process the 'pages' structure
                    for page in data['pages']:
                        if isinstance(page, dict):
                            # Each item in page dict becomes its own entry
                            for title, details in page.items():
                                if isinstance(details, dict):
                                    # Create a new object combining title and details
                                    jsonl_object = {
                                        'title': title,
                                        **details
                                    }
                                    
                                    # Remove any keys to ignore
                                    for key in ignore_keys:
                                        if key in jsonl_object:
                                            del jsonl_object[key]
                                    
                                    # Write the object
                                    f.write(json.dumps(jsonl_object, ensure_ascii=False) + '\n')
                                    count += 1
                else:
                    # Handle flat dictionary - each key-value pair becomes one line
                    for key, value in data.items():
                        if key.lower() in [k.lower() for k in ignore_keys]:
                            continue
                            
                        if isinstance(value, dict):
                            # If value is a dict, include the key as a field
                            jsonl_object = {'id': key, **value}
                            
                            # Remove any keys to ignore
                            for ignore_key in ignore_keys:
                                if ignore_key in jsonl_object:
                                    del jsonl_object[ignore_key]
                                    
                            f.write(json.dumps(jsonl_object, ensure_ascii=False) + '\n')
                            count += 1
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
    # Check command line arguments
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
    else:
        input_file = "training.json"
        output_file = "training.jsonl"

    # Convert with 'questions' key ignored (case insensitive)
    convert_json_to_jsonl(input_file, output_file, ignore_keys=['questions', 'Questions'])

if __name__ == "__main__":
    main()