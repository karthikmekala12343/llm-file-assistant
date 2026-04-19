# Overview

# Part A: Core File System Tools

> Created fs_tools.py with the following functions:
- read_file(filepath): Reads TXT, PDF, and DOCX files. Extracts content and returns it alongside metadata. Gracefully handles missing dependencies or unsupported types.
- list_files(directory, extension): Lists all files in a given directory, optionally filtered by extension. Returns metadata (name, size, modified_date).
- write_file(filepath, content): Writes content to a file, creating any required directories along the path.
- search_in_file(filepath, keyword): Searches for a keyword inside a file (using read_file under the hood) and returns matched lines with surrounding context.

# Part B: LLM Integration

- Created llm_file_assistant.py, an interactive command-line app connecting OpenAI's API to the file system tools via function calling. The AI is fully equipped to parse user intent and execute actions like listing resumes or extracting information.
Additional Submissions
- Dummy Data: Included a generate_resumes.py script. Running it generates 5 sample resumes into a resumes/ folder to test the tool.
- Requirements: Updated requirements.txt with necessary dependencies, including pypdf and python-docx.
- Documentation: Provided a detailed README.md outlining setup instructions, feature list, and example queries to get started quickly.