import os
import json
from langchain_core.tools import tool
from src.client import RobotScanClient

# Base path for relative lookups
ROOT_DIR = os.path.join(os.path.dirname(__file__), "..", "..")

# Load config utility
def get_config():
    config_path = os.path.join(ROOT_DIR, "config", "path.json")
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return json.load(f)
    return {}

client = RobotScanClient()

@tool
def get_robot_status():
    """Reads the latest log from the configured log directory to check the current status of the scanning system."""
    config = get_config()
    # Support both Log_dir and Log_path for compatibility
    log_path_raw = config.get("Log_dir") or config.get("Log_path", "")
    
    if not log_path_raw:
        return "Error: Log directory/path not configured in path.json."
        
    # Robust path resolution (absolute or relative to ROOT_DIR)
    if os.path.isabs(log_path_raw):
        log_dir = log_path_raw
    else:
        log_dir = os.path.join(ROOT_DIR, log_path_raw)
        
    if not os.path.exists(log_dir):
        return f"Error: Log location not found at {log_dir}. Please check your config/path.json."
    
    # Identify the target log file
    target_log = None
    if os.path.isdir(log_dir):
        # List all files and find the newest one
        files = [os.path.join(log_dir, f) for f in os.listdir(log_dir)]
        files = [f for f in files if os.path.isfile(f)]
        if not files:
            return f"Error: No log files found in directory {log_dir}."
        target_log = max(files, key=os.path.getmtime)
    else:
        # Fallback if the path in config directly points to a file
        target_log = log_dir
    
    try:
        # Try multiple encodings for Windows compatibility (GBK/GB18030)
        content = ""
        for enc in ["utf-8", "gbk", "gb18030"]:
            try:
                with open(target_log, "r", encoding=enc) as f:
                    lines = f.readlines()
                    last_lines = lines[-10:]
                    content = "".join(last_lines)
                    break
            except (UnicodeDecodeError, UnicodeError):
                continue
        
        if not content:
            # Fallback for completely unknown formats
            with open(target_log, "r", encoding="utf-8", errors="replace") as f:
                content = "".join(f.readlines()[-10:])

        return f"Source: {os.path.basename(target_log)}\nLast log entries:\n" + content
    except Exception as e:
        return f"Error reading log: {str(e)}"

@tool
def load_scan_template(filename: str):
    """
    Loads a specific scan template (.scanTemplate) into the RC software.
    Args:
        filename: The name of the template file (e.g., '1_default.scanTemplate').
    """
    config = get_config()
    template_config = config.get("scanTemplate", "")
    
    # Resolve the physical path and the logical name/path for the TCP command
    if os.path.isabs(filename):
        # Case 1: AI provided an absolute path directly
        full_path = filename
        name = os.path.basename(filename)
        path = os.path.dirname(filename)
    elif os.path.isfile(template_config):
        # Case 2: Config is a full file path (User's current scenario)
        full_path = template_config
        name = os.path.basename(template_config)
        path = os.path.dirname(template_config)
    else:
        # Case 3: Config is a directory, AI provided a filename
        path = template_config
        name = filename
        full_path = os.path.join(path, name)
        
    if not os.path.exists(full_path):
        return f"Error: Template file not found at {full_path}. Please check your config/path.json 'scanTemplate' value."
        
    # Ensure standard path separators for the hardware
    path = path.replace("\\", "/")
    
    res = client.send_command("open", params={"filename": name, "path": path})
    if res["success"]:
        return f"Successfully sent command to load template: {name} (Path: {path})"
    else:
        return f"Failed to load template: {res['error']}"

@tool
def control_scanner(action: str):
    """
    Sends a control command to the scanner.
    Args:
        action: One of 'start', 'stop', 'suspend', 'resume'.
    """
    if action not in ["start", "stop", "suspend", "resume"]:
        return "Error: Invalid action. Must be 'start', 'stop', 'suspend', or 'resume'."
        
    res = client.send_command(action)
    if res["success"]:
        return f"Successfully sent '{action}' command to the scanner."
    else:
        return f"Failed to send '{action}' command: {res['error']}"

@tool
def search_manual(query: str = None):
    """
    Lists available documentation in the manual or reads a specific file if query matches a filename.
    Used for scanning technical guides and communication protocols.
    Args:
        query: Optional filename to read (e.g., 'robotscan_communication_protocal.md').
    """
    manual_dir = os.path.join(ROOT_DIR, "manual")
    if not os.path.exists(manual_dir):
        return "Error: Manual directory not found."
        
    files = [f for f in os.listdir(manual_dir) if f.endswith(".md")]
    
    if query and query in files:
        with open(os.path.join(manual_dir, query), "r", encoding="utf-8") as f:
            return f"Content of {query}:\n\n" + f.read()
            
    return "Available manuals:\n- " + "\n- ".join(files) + "\n\nUse this tool with a filename to read its content."

def get_robot_tools():
    return [get_robot_status, load_scan_template, control_scanner, search_manual]
