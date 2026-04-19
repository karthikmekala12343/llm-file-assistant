# LLM-Powered File System Assistant
The llm file assistant integrates core file tools with an LLM for user-driven data tasks. It reads, searches, and summarizes files per user queries, like listing resumes or finding specific skills in them. The LLM calls relevant tools, streamlining file operations through natural language interaction.

This project is an LLM-powered assistant designed to interact with your local file system, primarily focused on reading, parsing, and searching through resume files (PDF, DOCX, TXT).

## Features

- **Read Files**: Extract text and metadata from PDF, DOCX, and TXT files.
- **List Files**: View files in a directory, with optional extension filtering.
- **Search Files**: Find specific keywords within documents, returning context-aware matches.
- **Write Files**: Create new files or overwrite existing ones.
- **LLM Integration**: Chat with an AI assistant that uses these tools autonomously based on your requests.

## Setup

1.  **Clone the repository or download the files.**
2.  **Install dependencies**:
    Ensure you have Python 3.8+ installed, then run:
    ```bash
    pip install -r requirements.txt
    ```
    This will install `openai`, `python-dotenv`, `pydantic`, `pypdf`, and `python-docx`.
3.  **Environment Variables**:
    Create a `.env` file in the root directory and add your OpenAI API key:
    For OpenAI:
    ```env
    AI_PROVIDER=openai
    OPENAI_API_KEY=your_openai_api_key
    ```

    For Claude:

    ```env
    AI_PROVIDER=claude
    CLAUDE_API_KEY=your_claude_api_key
    CLAUDE_MODEL=claude-2.1


    ```

    If `AI_PROVIDER` is omitted, the assistant defaults to OpenAI.

    You can also override the provider from the command line:

    ```powershell
    python llm_file_assistant.py --provider claude
    ```

    Or specify a model explicitly:

    ```powershell
    python llm_file_assistant.py --provider claude --model claude-2.1
    ```

    Note: Claude support uses the Anthropic completion endpoint and currently does not support OpenAI-style tool calls in this codebase.


## Usage

1.  **Generate Sample Data (Optional)**:
    If you need dummy resumes to test with, run the provided generation script:
    ```bash
    python generate_resumes.py
    ```
    This will create a `resumes` directory with 5 text-based dummy resumes.

2.  **Run the Assistant**:
    Start the interactive chat session by running:
    ```bash
    python llm_file_assistant.py
    ```

3.  **Example Queries**:
    Once the assistant is running, try asking:
    - *"List all resumes in the resumes folder"*
    - *"Find resumes mentioning Python experience"*
    - *"Read the resume for Alice Johnson"*
    - *"Create a summary file for Alice's resume and save it as summary.txt"*

## File Structure

- `llm_file_assistant.py`: The main entry point, integrating OpenAI with local file system tools.
- `fs_tools.py`: The core implementation of the file system tools (`read_file`, `list_files`, `write_file`, `search_in_file`).
- `generate_resumes.py`: A helper script to create dummy resume data for testing.
- `requirements.txt`: The Python dependencies.