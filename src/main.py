import asyncio
from src.agent import get_agent

async def run_demo():
    agent = get_agent()
    
    # Define the demo interaction
    inputs = {
        "messages": [
            ("user", "帮我看看扫描仪准备好了没有？如果准备好了，请加载 data/Project_Example 下的 plc_1_1.scanTemplate 模板，然后开始扫描。")
        ]
    }
    
    print("--- Starting RobotScan Agent Demo ---")
    
    # We use stream to see the reasoning steps
    async for chunk in agent.astream(inputs, stream_mode="values"):
        if "messages" in chunk:
            last_msg = chunk["messages"][-1]
            if last_msg.type == "human":
                print(f"\nUser: {last_msg.content}")
            elif last_msg.type == "ai":
                if last_msg.content:
                    print(f"\nAgent: {last_msg.content}")
                if last_msg.tool_calls:
                    for tc in last_msg.tool_calls:
                        print(f"  [Tool Call]: {tc['name']}({tc['args']})")
            elif last_msg.type == "tool":
                print(f"  [Tool Result]: {last_msg.content}")

if __name__ == "__main__":
    try:
        asyncio.run(run_demo())
    except Exception as e:
        print(f"\nExecution failed: {e}")
        print("\nNote: This demo requires OPENAI_API_KEY and OPENAI_API_BASE to be set in your environment.")
