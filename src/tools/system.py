import os
from pathlib import Path
from langchain_core.tools import tool

# Base path of the project for security (two levels up from src/tools/system.py)
ROOT_DIR = Path(__file__).parent.parent.parent.resolve()

@tool
def list_project_files(path: str = "."):
    """
    Lists files and directories at the given path.
    Args:
        path: Path to list (e.g., '.', 'C:/Logs', or 'data').
    """
    try:
        # Resolve path (supports both relative to project and absolute)
        target_path = Path(path).resolve() if os.path.isabs(path) else (ROOT_DIR / path).resolve()
        
        if not target_path.exists():
            return f"Error: Path '{path}' does not exist."
            
        items = []
        for i in target_path.iterdir():
            prefix = "[DIR] " if i.is_dir() else "[FILE]"
            items.append(f"{prefix} {i.name}")
            
        return f"Contents of {path}:\n" + "\n".join(items)
    except Exception as e:
        return f"Error listing directory: {str(e)}"

@tool
def read_project_file(path: str, max_chars: int = 20000):
    """
    Reads a file's content from the given path with safety limits.
    Args:
        path: Path to read (e.g., 'config/path.json' or an absolute path like 'C:/Temp/log.txt').
        max_chars: Maximum characters to read to avoid context overflow.
    """
    try:
        # Resolve path (supports both relative to project and absolute)
        target_path = Path(path).resolve() if os.path.isabs(path) else (ROOT_DIR / path).resolve()
            
        if not target_path.is_file():
            return f"Error: '{path}' is not a file."
            
        # Size hint for the agent
        size = target_path.stat().st_size
        if size > 1_000_000: # 1MB limit for safety
             return "Error: File too large (>1MB). Please use a dedicated tool or read a slice."

        # Robustness: Read with UTF-8 and fallback replacement for binary/non-utf8 chars
        with open(target_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read(max_chars)
            if len(content) >= max_chars:
                return (f"--- Content of {path} (Truncated at {max_chars} chars) ---\n"
                        f"{content}\n"
                        f"--- End (Truncated) ---\n"
                        f"Note: File has internal lines not shown. Specify a start offset if needed.")
            return f"--- Content of {path} ---\n{content}"
    except Exception as e:
        return f"Error reading file: {str(e)}"

def get_system_tools():
    return [list_project_files, read_project_file]
