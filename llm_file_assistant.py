import argparse
import os
import json
import urllib.error
import urllib.request
from dotenv import load_dotenv
from openai import OpenAI
import fs_tools
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv(override=True)


class ReadFileArgs(BaseModel):
    filepath: str = Field(description="The path to the resume file (PDF, TXT, DOCX) to read.")

class ListFilesArgs(BaseModel):
    directory: str = Field(description="The directory to list files in.")
    extension: str = Field(default=None, description="Optional extension to filter by (e.g., '.pdf', '.txt').")

class WriteFileArgs(BaseModel):
    filepath: str = Field(description="The path to the file to write to.")
    content: str = Field(description="The content to write to the file.")

class SearchInFileArgs(BaseModel):
    filepath: str = Field(description="The path to the file to search in.")
    keyword: str = Field(description="The keyword to search for.")


# Tool Definitions
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Reads resume files (PDF, TXT, DOCX), extracts text content, and returns a structured response with content and metadata.",
            "parameters": ReadFileArgs.model_json_schema()
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "Lists all files in a directory, optionally filtered by extension.",
            "parameters": ListFilesArgs.model_json_schema()
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Writes content to a file, creating directories if needed.",
            "parameters": WriteFileArgs.model_json_schema()
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_in_file",
            "description": "Searches for keywords in a file's content and returns matches with context.",
            "parameters": SearchInFileArgs.model_json_schema()
        }
    }
]

class FileAssistant:
    def __init__(self, provider: str = None, model: str = None):
        self.provider = provider.strip().lower() if provider else os.getenv("AI_PROVIDER", "openai").strip().lower()
        if self.provider == "openai":
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                print("Error: OPENAI_API_KEY not found in environment variables.")
                print("Please create a .env file and add your OpenAI API key.")
                exit(1)
            self.client = OpenAI(api_key=api_key)
            self.model = model if model else os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        elif self.provider in ("claude", "anthropic"):
            api_key = os.getenv("CLAUDE_API_KEY")
            if not api_key:
                print("Error: CLAUDE_API_KEY not found in environment variables.")
                print("Please create a .env file and add your Claude API key.")
                exit(1)
            self.client = None
            self.claude_api_key = api_key
            self.model = model if model else os.getenv("CLAUDE_MODEL", "claude-2.1")
        else:
            print(f"Error: Unsupported AI_PROVIDER '{self.provider}'. Use 'openai' or 'claude'.")
            exit(1)

        self.messages = [
            {
                "role": "system", 
                "content": "You are a helpful LLM-Powered File System Assistant specializing in reading and analyzing resumes. You have access to tools that can read files (PDF, DOCX, TXT), list directories, write to files, and search for keywords within files. Always use the appropriate tool when asked to perform a file operation. Present data clearly and answer user queries effectively."
            }
        ]

    def execute_tool(self, tool_call) -> dict:
        """Executes the corresponding function in fs_tools based on the tool call."""
        name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)

        try:
            if name == "read_file":
                return fs_tools.read_file(**args)
            elif name == "list_files":
                return fs_tools.list_files(**args)
            elif name == "write_file":
                return fs_tools.write_file(**args)
            elif name == "search_in_file":
                return fs_tools.search_in_file(**args)
            else:
                return {"status": "error", "message": f"Tool '{name}' not found."}
        except Exception as e:
            return {"status": "error", "message": f"Error executing tool: {str(e)}"}

    def build_anthropic_prompt(self) -> str:
        prompt_lines = []
        for message in self.messages:
            role = message["role"]
            if role == "system":
                prompt_lines.append(f"System: {message['content']}")
            elif role == "user":
                prompt_lines.append(f"Human: {message['content']}")
            else:
                prompt_lines.append(f"Assistant: {message['content']}")
        prompt_lines.append("Assistant:")
        return "\n\n".join(prompt_lines)

    def call_claude(self, prompt: str) -> str:
        url = "https://api.anthropic.com/v1/complete"
        data = json.dumps({
            "model": self.model,
            "prompt": prompt,
            "max_tokens_to_sample": 1000,
            "temperature": 0.7,
            "stop_sequences": ["\n\nHuman:"]
        }).encode("utf-8")

        request = urllib.request.Request(
            url,
            data=data,
            headers={
                "Content-Type": "application/json",
                "X-API-Key": self.claude_api_key
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result.get("completion", "")
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"Claude API request failed: {e.code} {e.reason}: {e.read().decode('utf-8')}")
        except Exception as e:
            raise RuntimeError(f"Claude request error: {str(e)}")

    def chat(self, user_input: str) -> str:
        """Sends the user input to the LLM and handles any required tool calls."""
        self.messages.append({"role": "user", "content": user_input})

        while True:
            try:
                if self.provider == "openai":
                    response = self.client.chat.completions.create(
                        model=self.model,
                        messages=self.messages,
                        tools=TOOLS,
                        tool_choice="auto"
                    )
                    response_message = response.choices[0].message
                    self.messages.append(response_message)

                    if response_message.tool_calls:
                        for tool_call in response_message.tool_calls:
                            print(f"  [Executing Tool]: {tool_call.function.name}")
                            tool_result = self.execute_tool(tool_call)

                            self.messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call.id,
                                "name": tool_call.function.name,
                                "content": json.dumps(tool_result)
                            })
                        # Loop back to let the LLM generate a response based on the tool results
                        continue
                    else:
                        return response_message.content

                else:
                    prompt = self.build_anthropic_prompt()
                    assistant_text = self.call_claude(prompt)
                    response_message = {
                        "role": "assistant",
                        "content": assistant_text
                    }
                    self.messages.append(response_message)
                    return assistant_text

            except Exception as e:
                return f"Error communicating with the LLM: {str(e)}"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LLM File System Assistant")
    parser.add_argument("--provider", choices=["openai", "claude", "anthropic"], help="Select the AI provider to use.")
    parser.add_argument("--model", help="Optional model name to override the default provider model.")
    args = parser.parse_args()

    print("Welcome to the LLM File System Assistant!")
    print("Example commands:")
    print(" - 'List all resumes in the resumes folder'")
    print(" - 'Read resumes/resume_john_doe.txt'")
    print(" - 'Search for Python in resumes/resume_jane_smith.txt'")
    print("Type 'exit' or 'quit' to exit.\n")
    
    assistant = FileAssistant(provider=args.provider, model=args.model)
    
    while True:
        try:
            user_input = input("\nYou: ")
            if user_input.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
                
            print("Assistant: Thinking...")
            response = assistant.chat(user_input)
            print(f"\nAssistant: {response}")
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")