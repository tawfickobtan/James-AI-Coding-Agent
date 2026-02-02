from llm import complete
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from rich.theme import Theme
from agent import Agent
import tools
import json
import os
from pathlib import Path
baseDir = Path(__file__).resolve().parent

# Load config file
config = {}
with open(baseDir / "config.json", "r") as f:
    config = json.load(f)

systemPrompt = ""
with open(baseDir / "system_prompt.txt", "r") as f:
    systemPrompt = f.read()

tooling = []
with open(baseDir / "tools.json") as f:
    tooling = json.load(f)

api_key = os.environ.get("GROQ_API_KEY","")

custom_theme = Theme({
    "markdown.h1": "bold white",
    "markdown.h2": "bold green",
    "markdown.h3": "bold yellow",
})

console = Console(theme=custom_theme)
saveMessages = open(baseDir / "messages.txt", "w",encoding="utf-8")

# Define function registry
functionRegistry = {
    "getItemsInPath": tools.getItemsInPath,
    "writeIntoFile": tools.writeIntoFile,
    "readFile": tools.readFile,
    "createFile": tools.createFile,
    "delete": tools.delete,
    "createDirectory": tools.createDirectory,
    "deleteDirectory": tools.deleteDirectory,
    "moveFile": tools.moveFile,
    "copyFile": tools.copyFile,
    "getCurrentDirectory": tools.getCurrentDirectory,
    "runCommand": tools.runCommand,
    "fileExists": tools.fileExists,
    "getFileSize": tools.getFileSize,
    "readPDF": tools.readPDF
}

# Create welcome message
big_text = Text(""" █████╗ ██╗     ███████╗██████╗ ███████╗██████╗ 
██╔══██╗██║     ██╔════╝██╔══██╗██╔════╝██╔══██╗
███████║██║     █████╗  ██████╔╝█████╗  ██║  ██║
██╔══██║██║     ██╔══╝  ██╔══██╗██╔══╝  ██║  ██║
██║  ██║███████╗██║     ██║  ██║███████╗██████╔╝
╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝  ╚═╝╚══════╝╚═════╝ 
""", style="bold cyan")
welcome_text = Text("Your File Management AI Agent", style="bold cyan")
version_text = Text(f"(Version: {config.get('version', '1.1')})", style="dim white")
welcome_panel = Panel(
    big_text + welcome_text + "\n" + version_text,
    title="🚀 Agent Started",
    border_style="green",
    padding=(0, 10)
)

console.print(welcome_panel)
console.print(Text("Model: ", style="bold yellow") + Text(config.get("model", "openai/gpt-oss-120b"), style="white"))
console.print(Text("Current Directory: ", style="bold yellow") + Text(tools.getCurrentDirectory(), style="white"))

console.print()  # Blank line for spacing


# Initialise Agent
agent = Agent(
    base_url=config.get("base_url", "https://api.groq.com/openai/v1"),
    api_key=api_key,
    model=config.get("model", "openai/gpt-oss-120b"),
    toolsDesc=tooling,
    function_registry=functionRegistry,
    system_prompt=systemPrompt +"\n\n" + "Current Directory: " + tools.getCurrentDirectory() +
                "\n\n" + "Current Items in Directory:\n" + tools.getItemsInPath(tools.getCurrentDirectory())
)


agentPanel = Panel("🤖 Alfred:",
                     border_style="green",
                     expand=False,
                     style="bold blue")

UserPanel = Panel("💭 User:",
                     border_style="green",
                     expand=False,
                     style="bold blue")

toolPanel = Text("🛠️ Executing: ",
                     style="bold red")

response = agent.complete()
console.print(agentPanel)
console.print(Markdown(response[0].content))
console.print(Markdown("---"))

while True:
    console.print(UserPanel)
    userInput = input()
    console.print(Markdown("---"))
    agent.add_message("user", userInput)
    console.print(agentPanel)
    while True:
        try:
            response = agent.complete()
        except Exception as e:
            raise e

        if len(response) > 1:
            print(response[0])
            tool_call = response[0].tool_calls[0]
            id = tool_call.id
            name = tool_call.function.name
            args = tool_call.function.arguments
            if isinstance(args, str):
                args = json.loads(args)
                
            panelText = Text("Tool: ", style="bold blue") + Text(name, style="bold white") + "\n"
            if args:
                for arg in args:
                    panelText += Text(arg + "⤵️\n", style="bold yellow") + Text(args[arg] if len(args[arg]) < 50 else args[arg][:50] + "...", style="white") + "\n"
            panelText += "\n"
            result = response[1]["content"]
            panelText += Text("Result⤵️\n", style="bold blue") + Text(result, style="white")
            toolPanel = Panel(
                panelText,
                border_style="red",
                title="🛠️ Executing Tool: ",
                expand=False,
            )
            console.print(toolPanel)
            print()
        else:
            console.print(Text("Response:", style="bold blue"))
            console.print(Markdown(response[0].content))
            console.print(Markdown("---"))
            break