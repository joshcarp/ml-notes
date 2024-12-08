import os
import json

def write_file(file_path, content, mode="w"):
    """
    Write content to a file.
    
    Args:
        file_path (str): Path to the file.
        content (str or dict): Content to write to the file. 
            Automatically handles JSON if content is a dictionary.
        mode (str): File mode, default is 'w' (write).
    """
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, mode, encoding="utf-8") as f:
            if isinstance(content, (dict, list)):
                json.dump(content, f, indent=4)
            else:
                f.write(content)
        print(f"File written: {file_path}")
    except Exception as e:
        print(f"Error writing to file {file_path}: {e}")

def read_file(file_path):
    """
    Read content from a file.
    
    Args:
        file_path (str): Path to the file.
        
    Returns:
        str or dict: File content as a string or dictionary (if JSON).
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            try:
                return json.loads(content)  # Attempt to parse as JSON
            except json.JSONDecodeError:
                return content  # Return as string if not JSON
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return None

def read_dir(dir_path):
    """
    Read contents of a directory.
    
    Args:
        dir_path (str): Path to the directory.
        
    Returns:
        list: List of file names in the directory.
    """
    try:
        return [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f))]
    except Exception as e:
        print(f"Error reading directory {dir_path}: {e}")
        return []
