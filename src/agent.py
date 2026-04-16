import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from src.tools import get_tools

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

    tools = get_tools()
    
    system_message = (
        "You are the RobotScan Assistant. Your goal is to help users control the 3D scanning equipment.\n"
        "You have tools to check status, load templates, control the scanner, and search the manual.\n"
        "Always check the equipment status before starting a scan.\n"
        "If you are unsure about a process, search the manual.\n"
        "Be concise and professional."
    )

    agent = create_react_agent(llm, tools, prompt=system_message)
    return agent

if __name__ == "__main__":
    # Test execution
    agent = get_agent()
    # for chunk in agent.stream({"messages": [("user", "Hello! Are the scanner tools ready?")]}):
    #     print(chunk)
