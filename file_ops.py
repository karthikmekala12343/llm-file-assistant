import os
import json
from pathlib import Path
from typing import List, Dict, Any, Union

def list_files(directory: str = ".", recursive: bool = False) -> List[str]:
    """Lists files in the given directory."""
    path = Path(directory)
    if not path.exists() or not path.is_dir():
        return [f"Error: Directory '{directory}' does not exist or is not a directory."]
    
    files = []
    try:
        if recursive:
            for p in path.rglob("*"):
                if p.is_file():
                    files.append(str(p))
        else:
            for p in path.glob("*"):
                if p.is_file():
                    files.append(str(p))
        return files
    except Exception as e:
        return [f"Error listing files: {str(e)}"]

def read_file(filepath: str) -> str:
    """Reads the content of a file."""
    path = Path(filepath)
    if not path.exists() or not path.is_file():
        return f"Error: File '{filepath}' does not exist or is not a file."
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except UnicodeDecodeError:
        return f"Error: File '{filepath}' is not a text file or cannot be decoded."
    except Exception as e:
        return f"Error reading file: {str(e)}"

def write_file(filepath: str, content: str) -> str:
    """Writes content to a file, creating directories if necessary."""
    path = Path(filepath)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully wrote to {filepath}"
    except Exception as e:
        return f"Error writing to file: {str(e)}"

def parse_json_file(filepath: str) -> Union[Dict[Any, Any], List[Any], str]:
    """Parses a JSON file and returns its content."""
    content = read_file(filepath)
    if content.startswith("Error:"):
        return content
    
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        return f"Error parsing JSON: {str(e)}"

def get_file_info(filepath: str) -> Dict[str, Any]:
    """Gets metadata about a file."""
    path = Path(filepath)
    if not path.exists() or not path.is_file():
        return {"error": f"File '{filepath}' does not exist or is not a file."}
    
    try:
        stat = path.stat()
        return {
            "name": path.name,
            "size_bytes": stat.st_size,
            "modified_time": stat.st_mtime,
            "extension": path.suffix
        }
    except Exception as e:
        return {"error": f"Error getting file info: {str(e)}"}