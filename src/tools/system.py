import os
from pathlib import Path
from langchain_core.tools import tool

# Base path of the project for security (two levels up from src/tools/system.py)
ROOT_DIR = Path(__file__).parent.parent.parent.resolve()

@tool
def list_project_files(relative_path: str = "."):
    """
    Lists files and directories within the project workspace.
    Args:
        relative_path: Path relative to project root (e.g., 'data' or '.').
    """
    try:
        target_path = (ROOT_DIR / relative_path).resolve()
        # Security Check: Ensure the path is inside ROOT_DIR
        if not str(target_path).startswith(str(ROOT_DIR)):
            return "Error: Access denied. Path is outside of project root."
        
        if not target_path.exists():
            return f"Error: Path '{relative_path}' does not exist."
            
        items = []
        for i in target_path.iterdir():
            prefix = "[DIR] " if i.is_dir() else "[FILE]"
            items.append(f"{prefix} {i.name}")
            
        return f"Contents of {relative_path}:\n" + "\n".join(items)
    except Exception as e:
        return f"Error listing directory: {str(e)}"

@tool
def read_project_file(relative_path: str, max_chars: int = 20000):
    """
    Reads a file's content from the project workspace with safety limits.
    Args:
        relative_path: Path relative to project root (e.g., 'config/path.json').
        max_chars: Maximum characters to read to avoid context overflow.
    """
    try:
        target_path = (ROOT_DIR / relative_path).resolve()
        # Security Check
        if not str(target_path).startswith(str(ROOT_DIR)):
            return "Error: Access denied. Path outside root."
            
        if not target_path.is_file():
            return f"Error: '{relative_path}' is not a file."
            
        # Size hint for the agent
        size = target_path.stat().st_size
        if size > 1_000_000: # 1MB limit for safety
             return "Error: File too large (>1MB). Please use a dedicated tool or read a slice."

        # Robustness: Read with UTF-8 and fallback replacement for binary/non-utf8 chars
        with open(target_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read(max_chars)
            if len(content) >= max_chars:
                return (f"--- Content of {relative_path} (Truncated at {max_chars} chars) ---\n"
                        f"{content}\n"
                        f"--- End (Truncated) ---\n"
                        f"Note: File has internal lines not shown. Specify a start offset if needed.")
            return f"--- Content of {relative_path} ---\n{content}"
    except Exception as e:
        return f"Error reading file: {str(e)}"

def get_system_tools():
    return [list_project_files, read_project_file]
