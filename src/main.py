import asyncio
import os
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.live import Live
from rich.status import Status
from src.agent import get_agent

console = Console()

async def run_interactive_demo():
    agent = get_agent()
    
    # thread_id is used by MemorySaver to track different conversations
    config = {"configurable": {"thread_id": "robotscan_demo_thread"}}
    
    console.print(Panel.fit(
        "[bold blue]RobotScan Agent[/bold blue] 智能交互演示\n"
        "输入 'exit', 'quit' 或 'q' 退出对话。",
        border_style="cyan"
    ))
    
    while True:
        try:
            user_input = console.input("\n[bold green]User:[/bold green] ")
        except EOFError:
            break
            
        if user_input.lower() in ["exit", "quit", "q", "bye"]:
            console.print("\n[yellow]再见！祝扫描顺利。[/yellow]")
            break
            
        inputs = {"messages": [("user", user_input)]}
        
        final_ai_msg = ""
        # Use Status for the "Thinking" indicator
        with console.status("[bold blue]Agent 正在思考并执行工具...", spinner="dots") as status:
            async for chunk in agent.astream(inputs, config=config, stream_mode="values"):
                if "messages" in chunk:
                    last_msg = chunk["messages"][-1]
                    
                    # Display tool calls
                    if last_msg.type == "ai":
                        # If there is content AND tool_calls, this is the "Thought" process
                        if last_msg.content and last_msg.tool_calls:
                            console.print(Panel(
                                Markdown(last_msg.content), 
                                title="[italic dim]Agent 思考过程[/italic dim]", 
                                border_style="dim"
                            ))
                        
                        if last_msg.tool_calls:
                            for tc in last_msg.tool_calls:
                                console.print(f"  [cyan]▸ 正在调用工具: [bold]{tc['name']}[/bold][/cyan]")
                        
                        # Buffer final AI response (messages without tool calls)
                        elif last_msg.content:
                            final_ai_msg = last_msg.content
                    
                    # Display tool results
                    elif last_msg.type == "tool":
                        console.print(f"  [dim green]✓ 工具 '{last_msg.name}' 返回结果[/dim green]")

        if final_ai_msg:
            console.print(Panel(Markdown(final_ai_msg), title="[bold blue]RobotScan Assistant[/bold blue]", border_style="blue"))

if __name__ == "__main__":
    try:
        asyncio.run(run_interactive_demo())
    except KeyboardInterrupt:
        console.print("\n\n[yellow]会话已中断。[/yellow]")
    except Exception as e:
        console.print(f"\n[bold red]运行失败:[/bold red] {e}")
        console.print("\n[dim]请确保您的 .env 文件中已配置 API Key。[/dim]")
