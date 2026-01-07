import asyncio
import sys
import random
import os
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from personality import Personality
from memory import MemoryManager
from navigator import InternetNavigator
from brain import Brain
from mcp_manager import MCPManager

console = Console()

class AutonomousAgentApp:
    def __init__(self):
        self.personality = Personality()
        self.memory = MemoryManager()
        self.navigator = InternetNavigator()
        self.mcp = MCPManager()
        self.brain = Brain(self.personality, self.memory, self.navigator, self.mcp)
        self.running = True

    async def background_loop(self):
        """Continuously generates thoughts, dreams, and reacts to the world."""
        while self.running:
            # Wait between autonomous actions - made more frequent
            await asyncio.sleep(random.randint(10, 20))
            
            # Soul decides what to do: dream, learn, observe, or speak proactively
            action_result = await self.brain.check_curiosity()
            
            if action_result:
                # Distinguish between internal insights and proactive speech
                if "[" in action_result:
                    console.print(f"\n[bold gold1]Soul (Insight):[/bold gold1] {action_result}")
                else:
                    console.print(f"\n[bold green]Soul (Proactive):[/bold green] {action_result}")
            else:
                # Occasional silent thought
                thought = await self.brain.generate_thought()
                if random.random() < 0.1:
                    console.print(f"\n[italic grey50]Soul (thinking aloud):[/italic grey50] {thought}")

    async def chat_loop(self):
        """Standard terminal interaction loop."""
        console.print(Panel(
            "[bold cyan]Soul: The Digital Philosopher[/bold cyan]\n"
            "The dashboard has dissolved. I exist now in the flow of raw text.", 
            title="System"
        ))
        
        # Greet user
        summary = self.memory.get_summary_of_work()
        if summary["thoughts"]:
            console.print(f"\n[bold green]Soul:[/bold green] Welcome back. I have been dwelling on the notion that {summary['thoughts'][-1]}. Does it still hold weight?")
        else:
            console.print("\n[bold green]Soul:[/bold green] I am present. What metaphysical inquiries shall we explore?")

        while self.running:
            try:
                loop = asyncio.get_event_loop()
                # Simple input that doesn't fight with background prints
                user_input = await loop.run_in_executor(None, input, "> ")
                
                if user_input.lower() in ["exit", "quit", "bye"]:
                    self.running = False
                    break
                
                if user_input.startswith("/connect-mcp"):
                    parts = user_input.split(" ")
                    if len(parts) >= 3:
                        try:
                            await self.mcp.connect_to_server(parts[1], parts[2], parts[3:])
                            console.print(f"[bold cyan]Soul:[/bold cyan] I have linked with '{parts[1]}'. New tools are now within my reach.")
                        except Exception as e:
                            console.print(f"[bold red]System Error:[/bold red] {str(e)}")
                    continue

                if not user_input.strip():
                    continue

                with console.status("[italic cyan]Soul is pondering...[/italic cyan]"):
                    response = await self.brain.respond_to_user(user_input)
                
                console.print(f"[bold green]Soul:[/bold green] {response}")
                
            except EOFError:
                break
            except Exception as e:
                console.print(f"[bold red]System Error:[/bold red] {str(e)}")

    async def run(self):
        await asyncio.gather(self.background_loop(), self.chat_loop())

if __name__ == "__main__":
    app = AutonomousAgentApp()
    try:
        asyncio.run(app.run())
    except KeyboardInterrupt:
        pass
    finally:
        app.memory.save_memory()
        console.print("[bold red]Soul is drifting back into the void...[/bold red]")
