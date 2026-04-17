import os
import json
from langchain_core.tools import tool
from src.client import RobotScanClient

# Load config
CONFIG_PATH = os.path.join(os.path.dirname(__file__), "..", "config", "path.json")

def get_config():
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    return {}

client = RobotScanClient()

@tool
def get_robot_status():
    """Reads the latest equipment log from Log_dir to check the current status of the scanning system."""
    config = get_config()
    log_dir = config.get("Log_dir", "")
    
    if not log_dir or not os.path.exists(log_dir):
        return "Error: Log directory not configured or not found. Cannot determine status."
    
    # Identify the target log file
    target_log = None
    if os.path.isdir(log_dir):
        # List all files and find the newest one
        files = [os.path.join(log_dir, f) for f in os.listdir(log_dir)]
        files = [f for f in files if os.path.isfile(f)]
        if not files:
            return f"Error: No log files found in {log_dir}."
        target_log = max(files, key=os.path.getmtime)
    else:
        # Fallback if Log_dir in config actually points to a file
        target_log = log_dir
    
    try:
        # Read the last 10 lines of the identified log
        with open(target_log, "r", encoding="utf-8") as f:
            lines = f.readlines()
            last_lines = lines[-10:]
            return f"Source: {os.path.basename(target_log)}\nLast log entries:\n" + "".join(last_lines)
    except Exception as e:
        return f"Error reading log: {str(e)}"

@tool
def load_scan_template(filename: str):
    """
    Loads a specific scan template (.scanTemplate) into the RC software.
    Args:
        filename: The name of the template file (e.g., 'plc_1_1.scanTemplate').
    """
    config = get_config()
    template_dir = config.get("scanTemplate", "")
    
    # If the user provides a full path, use it. Otherwise, look in the config directory.
    if os.path.isabs(filename):
        full_path = filename
        name = os.path.basename(filename)
        path = os.path.dirname(filename)
    else:
        name = filename
        path = template_dir
        full_path = os.path.join(path, name)
        
    if not os.path.exists(full_path):
        return f"Error: Template file not found at {full_path}"
        
    res = client.send_command("open", params={"filename": name, "path": path})
    if res["success"]:
        return f"Successfully sent command to load template: {name}"
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
    Args:
        query: Optional filename to read (e.g., 'robotscan_communication_protocal.md').
               If omitted or no match, lists all documents.
    """
    manual_dir = os.path.join(os.path.dirname(__file__), "..", "manual")
    if not os.path.exists(manual_dir):
        return "Error: Manual directory not found."
        
    files = [f for f in os.listdir(manual_dir) if f.endswith(".md")]
    
    if query and query in files:
        with open(os.path.join(manual_dir, query), "r", encoding="utf-8") as f:
            return f"Content of {query}:\n\n" + f.read()
            
    return "Available manuals:\n- " + "\n- ".join(files) + "\n\nUse this tool with a filename to read its content."

def get_tools():
    return [get_robot_status, load_scan_template, control_scanner, search_manual]
