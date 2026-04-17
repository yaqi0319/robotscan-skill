import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from src.tools import get_all_tools

# Load environment variables from .env if it exists
load_dotenv()

def get_agent():
    """
    Initializes and returns the LangGraph agent.
    """
    # Configure the base URL and API key for OpenAI-compatible providers
    # These should be set in environment variables or a .env file
    api_key = os.getenv("OPENAI_API_KEY")
    base_url = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4o")

    llm = ChatOpenAI(
        model=model_name,
        openai_api_key=api_key,
        openai_api_base=base_url,
        temperature=0
    )

    # Combine domain-specific and system-wide tools
    tools = get_all_tools()
    
    # Load base knowledge (communication protocol) to inject into system prompt
    protocol_path = os.path.join(os.path.dirname(__file__), "..", "manual", "robotscan_communication_protocal.md")
    protocol_content = ""
    if os.path.exists(protocol_path):
        with open(protocol_path, "r", encoding="utf-8") as f:
            protocol_content = f.read()

    system_message = (
        "You are the RobotScan Assistant. Your goal is to help users control the 3D scanning equipment.\n"
        "You have tools to check status, load templates, control the scanner, and search the manual.\n"
        "Always check the equipment status before starting a scan.\n"
        "If you are unsure about a process, search the manual.\n\n"
        "### Base Knowledge: Communication Protocol\n"
        f"{protocol_content}\n\n"
        "Be concise and professional."
    )

    # Add a memory checkpointer to enable multi-turn conversation
    memory = MemorySaver()
    
    agent = create_react_agent(llm, tools, prompt=system_message, checkpointer=memory)
    return agent

if __name__ == "__main__":
    # Test execution
    agent = get_agent()
    # for chunk in agent.stream({"messages": [("user", "Hello! Are the scanner tools ready?")]}):
    #     print(chunk)
