from src.tools.robot import get_robot_tools
from src.tools.system import get_system_tools

def get_all_tools():
    """Aggregates all tools from the robot and system sub-modules."""
    return get_robot_tools() + get_system_tools()
