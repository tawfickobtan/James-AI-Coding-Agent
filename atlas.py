from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown
from rich.theme import Theme
from agent.agent import Agent
import agent.tools as tools
import json
import os
from pathlib import Path
from rich.console import Console

baseDir = Path(__file__).resolve().parent

# Load config file
config = {}
with open(baseDir / "configuration/config.json", "r") as f:
    config = json.load(f)

systemPrompt = ""
with open(baseDir / "configuration/AGENT.md", "r") as f:
    systemPrompt = f.read()

tooling = []
with open(baseDir / "agent/tools.json") as f:
    tooling = json.load(f)

api_key = os.environ.get("GROQ_API_KEY","")

custom_theme = Theme({
    "markdown.h1": "Bold yellow",
    "markdown.h2": "bold white",
    "markdown.h3": "white",
})

console = Console(theme=custom_theme)

# Define function registry
functionRegistry = {
    "getItemsInPath": tools.getItemsInPath,
    "writeIntoFile": tools.writeIntoFile,
    "readFile": tools.readFile,
    "readFileLines": tools.readFileLines,
    "createFile": tools.createFile,
    "delete": tools.delete,
    "createDirectory": tools.createDirectory,
    "deleteDirectory": tools.deleteDirectory,
    "moveFile": tools.moveFile,
    "moveMultipleFiles": tools.moveMultipleFiles,
    "copyFile": tools.copyFile,
    "copyMultipleFiles": tools.copyMultipleFiles,
    "getCurrentDirectory": tools.getCurrentDirectory,
    "fileExists": tools.fileExists,
    "getFileSize": tools.getFileSize,
    "renameFile": tools.renameFile,
    "rememberFact": tools.rememberFact,
    "recallFact": tools.recallFact,
    "forgetFact": tools.forgetFact,
    "listMemories": tools.listMemories,
    "getDirectoryTree": tools.getDirectoryTree
}

# Create welcome message
big_text = Text(""" █████╗ ████████╗██╗      █████╗ ███████╗
██╔══██╗╚══██╔══╝██║     ██╔══██╗██╔════╝
███████║   ██║   ██║     ███████║███████╗
██╔══██║   ██║   ██║     ██╔══██║╚════██║
██║  ██║   ██║   ███████╗██║  ██║███████║
╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝


""", style="bold white")
welcome_text = Text("Your Local AI Agent", style="bold white")
version_text = Text(f"(Version: {config.get('version', '1.1')})", style="dim white")
welcome_panel = Panel(
    big_text + welcome_text + "\n" + version_text,
    title="🚀 Agent Started",
    border_style="dim white",
    padding=(0, 10)
)


# Initialise Agent
agent = Agent(
    base_url=config.get("base_url", "https://api.groq.com/openai/v1"),
    api_key=api_key,
    model=config.get("model", "moonshotai/Kimi-K2-Instruct-0905"),
    toolsDesc=tooling,
    function_registry=functionRegistry,
    system_prompt=systemPrompt + "\n" +
    f"Current Directory: {tools.getCurrentDirectory()}\n" +
    f"Current Directory Structure (to a depth of 3): {tools.getDirectoryTree(tools.getCurrentDirectory(), 3)}\n" +
    f"Stored Memories: {tools.listMemories()}\n" +
    f"Model Powering you: {config.get('model', 'llama-3.3-70b-versatile')}"
                )

console.print(welcome_panel)
console.print(Text("Model: ", style="bold yellow") + Text(agent.model, style="white"))
console.print(Text("Current Directory: ", style="bold yellow") + Text(tools.getCurrentDirectory(), style="white"))

console.print()  # Blank line for spacing


with console.status("Loading...", spinner="dots"):
    try:
        response = agent.step()
    except Exception as e:
        raise e
textResponse = response[0].content
console.print(Markdown(textResponse))
console.print(Markdown("---"))

while True:
    print("</> ", end="")
    userInput = input()
    console.print(Markdown("---"))
    agent.add_message("user", userInput)
    while True:
        with console.status("Thinking...", spinner="dots"):
            try:
                response = agent.step()
            except Exception as e:
                raise e
        if len(response) > 1:
            tool_call = response[0].tool_calls[0]
            id = tool_call.id
            name = tool_call.function.name
            args = tool_call.function.arguments
            if isinstance(args, str):
                args = json.loads(args)
                
            panelText = Text("Tool: ", style="bold blue") + Text(name, style="bold white") + "\n"
            if args:
                for arg in args:
                    if not isinstance(args[arg], str):  panelText += Text(arg + "⤵️\n", style="bold yellow") + Text(str(args[arg]), style="white") + "\n"
                    else:   panelText += Text(arg + "⤵️\n", style="bold yellow") + Text(args[arg] if len(args[arg]) < 50 else args[arg][:50] + "...", style="white") + "\n"
            panelText += "\n"
            result = response[1]["content"]
            panelText += Text("Result⤵️\n", style="bold blue") + Text(result, style="white")
            toolPanel = Panel(
                panelText,
                border_style="dim white",
                title="🛠️ Executing Tool: ",
                expand=False,
            )
            console.print(toolPanel)
            print()
        else:
            textResponse = response[0].content
            console.print(Markdown(textResponse))
            console.print(Markdown("---"))
            break