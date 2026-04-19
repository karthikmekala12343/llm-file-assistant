import os
import datetime
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError:
    PdfReader = None

try:
    from docx import Document
except ImportError:
    Document = None

def read_file(filepath: str) -> dict:
    """Reads PDF, DOCX, or TXT files and returns content and metadata."""
    path = Path(filepath)
    if not path.exists() or not path.is_file():
        return {"status": "error", "message": f"File '{filepath}' not found."}
    
    try:
        stat = path.stat()
        metadata = {
            "name": path.name,
            "size_bytes": stat.st_size,
            "modified_date": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat(),
            "extension": path.suffix.lower()
        }
        
        ext = path.suffix.lower()
        content = ""
        
        if ext == '.txt':
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        elif ext == '.pdf':
            if PdfReader is None:
                return {"status": "error", "message": "pypdf is not installed. Please install it with 'pip install pypdf'."}
            reader = PdfReader(filepath)
            content = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())
        elif ext == '.docx':
            if Document is None:
                return {"status": "error", "message": "python-docx is not installed. Please install it with 'pip install python-docx'."}
            doc = Document(filepath)
            content = "\n".join(para.text for para in doc.paragraphs)
        else:
            return {"status": "error", "message": f"Unsupported file extension: {ext}. Only .txt, .pdf, and .docx are supported."}
            
        return {
            "status": "success",
            "content": content,
            "metadata": metadata
        }
    except Exception as e:
        return {"status": "error", "message": f"Error reading file: {str(e)}"}

def list_files(directory: str, extension: str = None) -> list:
    """Lists all files in a directory, optionally filtered by extension."""
    path = Path(directory)
    if not path.exists() or not path.is_dir():
        return [{"status": "error", "message": f"Directory '{directory}' not found."}]
    
    results = []
    try:
        for p in path.iterdir():
            if p.is_file():
                if extension:
                    # Handle cases where extension is provided with or without the dot
                    ext_to_check = extension.lower() if extension.startswith('.') else f".{extension.lower()}"
                    if p.suffix.lower() != ext_to_check:
                        continue
                
                stat = p.stat()
                results.append({
                    "name": p.name,
                    "size_bytes": stat.st_size,
                    "modified_date": datetime.datetime.fromtimestamp(stat.st_mtime).isoformat()
                })
        return results
    except Exception as e:
        return [{"status": "error", "message": f"Error listing files: {str(e)}"}]

def write_file(filepath: str, content: str) -> dict:
    """Writes content to a file, creating directories if necessary."""
    path = Path(filepath)
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return {"status": "success", "message": f"Successfully wrote to {filepath}"}
    except Exception as e:
        return {"status": "error", "message": f"Error writing to file: {str(e)}"}

def search_in_file(filepath: str, keyword: str) -> dict:
    """Searches for a keyword in a file and returns matches with surrounding context."""
    read_result = read_file(filepath)
    if read_result.get("status") != "success":
        return read_result
        
    content = read_result.get("content", "")
    lines = content.split('\n')
    matches = []
    
    keyword_lower = keyword.lower()
    
    for i, line in enumerate(lines):
        if keyword_lower in line.lower():
            # Get a bit of context (previous and next line if available)
            start = max(0, i - 1)
            end = min(len(lines), i + 2)
            context = "\n".join(lines[start:end]).strip()
            matches.append({
                "line_number": i + 1,
                "matched_text": line.strip(),
                "context": context
            })
            
    return {
        "status": "success",
        "keyword": keyword,
        "matches_found": len(matches),
        "matches": matches
    }