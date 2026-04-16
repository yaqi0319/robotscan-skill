import asyncio
import os
from src.agent import get_agent

async def run_interactive_demo():
    agent = get_agent()
    
    # thread_id is used by MemorySaver to track different conversations
    config = {"configurable": {"thread_id": "robotscan_demo_thread"}}
    
    print("--- RobotScan Agent Interactive Demo ---")
    print("Type 'exit', 'quit', or 'bye' to end the conversation.")
    print("------------------------------------------")
    
    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ["exit", "quit", "bye", "q"]:
            print("\nAgent: Goodbye! Have a productive scanning session.")
            break
            
        inputs = {"messages": [("user", user_input)]}
        
        # We use astream to see the reasoning steps in real-time
        async for chunk in agent.astream(inputs, config=config, stream_mode="values"):
            if "messages" in chunk:
                last_msg = chunk["messages"][-1]
                # We only want to print AI responses or Tool results (optionally)
                if last_msg.type == "ai":
                    if last_msg.content:
                        print(f"\nAgent: {last_msg.content}")
                    if last_msg.tool_calls:
                        for tc in last_msg.tool_calls:
                            print(f"  [Action]: Calling tool '{tc['name']}' with args {tc['args']}")
                elif last_msg.type == "tool":
                    print(f"  [System]: Tool '{last_msg.name}' returned: {last_msg.content}")

if __name__ == "__main__":
    try:
        asyncio.run(run_interactive_demo())
    except KeyboardInterrupt:
        print("\n\nAgent: Session interrupted. Goodbye!")
    except Exception as e:
        print(f"\nExecution failed: {e}")
        print("\nNote: Ensure OPENAI_API_KEY and OPENAI_API_BASE are set in your .env file.")
