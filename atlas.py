import asyncio
import json
import os
from datetime import datetime
from pathlib import Path

from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Vertical
from textual.widgets import Footer, Header, Input, OptionList, RichLog

from agent.agent import Agent
import agent.tools as tools

# ── Bootstrap ──────────────────────────────────────────────────────────────────

baseDir = Path(__file__).resolve().parent

config: dict = json.loads((baseDir / "configuration/config.json").read_text())
systemPrompt: str = (baseDir / "configuration/AGENT.md").read_text()
tooling: list = json.loads((baseDir / "agent/tools.json").read_text())

api_key = os.environ.get("GROQ_API_KEY", "")
model = config.get("model", "moonshotai/Kimi-K2-Instruct-0905")

FUNCTION_REGISTRY = {
    "getItemsInPath":     tools.getItemsInPath,
    "readFile":           tools.readFile,
    "readPdfPages":       tools.readPdfPages,
    "readFileLines":      tools.readFileLines,
    "createFile":         tools.createFile,
    "deleteFiles":        tools.deleteFiles,
    "createDirectory":    tools.createDirectory,
    "deleteDirectory":    tools.deleteDirectory,
    "moveFiles":          tools.moveFiles,
    "copyFiles":          tools.copyFiles,
    "getCurrentDirectory":tools.getCurrentDirectory,
    "fileExists":         tools.fileExists,
    "getFileSize":        tools.getFileSize,
    "renameFile":         tools.renameFile,
    "rememberFact":       tools.rememberFact,
    "recallFact":         tools.recallFact,
    "forgetFact":         tools.forgetFact,
    "listMemories":       tools.listMemories,
    "searchWeb":          tools.searchWeb,
    "extractTextFromUrl": tools.extractTextFromUrl,
}

agent = Agent(
    base_url=config.get("base_url", "https://api.groq.com/openai/v1"),
    api_key=api_key,
    model=model,
    toolsDesc=tooling,
    function_registry=FUNCTION_REGISTRY,
    system_prompt=(
        systemPrompt
        + f"\nCurrent Directory: {tools.getCurrentDirectory()}"
        + f"\nCurrent Directory Contents: {tools.getItemsInPath(tools.getCurrentDirectory())}"
        + f"\nStored Memories: {tools.listMemories()}"
        + f"\nModel Powering you: {model}"
    ),
)

# ── Help text ──────────────────────────────────────────────────────────────────

HELP_TEXT = """\
[bold yellow]Slash Commands[/]
  [bold white]/clear[/]   Reset conversation history
  [bold white]/memory[/]  Show all stored memories
  [bold white]/save[/]    Save conversation to a Markdown file
  [bold white]/exit[/]    Quit AtlasCLI
  [bold white]/help[/]    Show this message

[bold yellow]Key Bindings[/]
  [bold white]Ctrl+L[/]   Clear chat
  [bold white]Ctrl+S[/]   Save chat
  [bold white]Ctrl+M[/]   Show memory
  [bold white]Ctrl+Q[/]   Quit
"""

# ── Styles ─────────────────────────────────────────────────────────────────────

SLASH_COMMANDS = ["/clear", "/memory", "/save", "/exit", "/help"]

APP_CSS = """
#chat {
    padding: 1 2;
    border: none;
}

#input-area {
    dock: bottom;
    height: auto;
}

#suggestions {
    height: auto;
    max-height: 7;
    margin: 0 2 0 2;
    border: round $accent;
    display: none;
}

Input {
    border: round $accent;
    margin: 0 2 1 2;
    padding: 0 1;
}
"""

# ── Tool icons ────────────────────────────────────────────────────────────────

TOOL_ICONS: dict[str, str] = {
    "createFile":          "📄",
    "readFile":            "📖",
    "readFileLines":       "📖",
    "readPdfPages":        "📑",
    "renameFile":          "✏️",
    "fileExists":          "🔍",
    "getFileSize":         "📏",
    "deleteFiles":         "🗑️",
    "deleteDirectory":     "🗑️",
    "createDirectory":     "📁",
    "getItemsInPath":      "📂",
    "getCurrentDirectory": "📍",
    "moveFiles":           "✂️",
    "copyFiles":           "📋",
    "rememberFact":        "💾",
    "recallFact":          "🧠",
    "forgetFact":          "🗑️",
    "listMemories":        "📦",
    "searchWeb":           "🔍",
    "extractTextFromUrl":  "🌐",
}

# ── App ────────────────────────────────────────────────────────────────────────

class AtlasTUI(App):
    """AtlasCLI — A Textual TUI for the Atlas AI agent."""

    TITLE = "AtlasCLI"
    SUB_TITLE = f"v{config.get('version', '1.0')}  ·  {model}"
    CSS = APP_CSS
    _last_was_tool: bool = False

    BINDINGS = [
        Binding("ctrl+q", "quit",        "Quit",   show=True),
        Binding("ctrl+l", "clear_chat",  "Clear",  show=True),
        Binding("ctrl+s", "save_chat",   "Save",   show=True),
        Binding("ctrl+m", "show_memory", "Memory", show=True),
    ]

    # ── Layout ─────────────────────────────────────────────────────────────────

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield RichLog(id="chat", highlight=True, markup=True, wrap=True)
        with Vertical(id="input-area"):
            yield OptionList(*SLASH_COMMANDS, id="suggestions")
            yield Input(placeholder="Message Atlas...  (type / for commands)")
        yield Footer()

    # ── Lifecycle ──────────────────────────────────────────────────────────────

    def on_mount(self) -> None:
        self.query_one(Input).focus()
        self.run_worker(self._boot_atlas(), exclusive=True, name="boot")

    async def _boot_atlas(self) -> None:
        """Get Atlas's opening message on startup."""
        self.sub_title = "Starting up..."
        chat = self.query_one(RichLog)
        chat.write(Text("─" * 60, style="dim white"))
        try:
            response = await asyncio.to_thread(agent.step) 
        except Exception as e:
            chat.write(Text(f"Error during startup: {e}\n\nCheck internet connection and API key environment variable.", style="bold red"))
            return
        self._render_response(response)
        self._reset_subtitle()

    # ── Input handling ─────────────────────────────────────────────────────────

    def on_input_changed(self, event: Input.Changed) -> None:
        suggestions = self.query_one("#suggestions", OptionList)
        value = event.value
        if value.startswith("/"):
            matches = [cmd for cmd in SLASH_COMMANDS if cmd.startswith(value.lower())]
            suggestions.clear_options()
            for match in matches:
                suggestions.add_option(match)
            suggestions.display = len(matches) > 0
        else:
            suggestions.display = False

    def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
        inp = self.query_one(Input)
        inp.value = str(event.option.prompt)
        self.query_one("#suggestions", OptionList).display = False
        inp.focus()
        inp.action_end()  # move cursor to end

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        self.query_one("#suggestions", OptionList).display = False
        user_input = event.value.strip()
        if not user_input:
            return
        self.query_one(Input).clear()

        if user_input.startswith("/"):
            self._handle_slash(user_input.lower())
        else:
            self._write_bubble("You", user_input, label_style="bold cyan")
            agent.add_message("user", user_input)
            self.run_worker(self._run_agent(), exclusive=True, name="agent")

    def _handle_slash(self, cmd: str) -> None:
        chat = self.query_one(RichLog)

        if cmd == "/clear":
            agent.reset_messages()
            chat.clear()
            chat.write(Text("Conversation cleared.", style="dim green"))

        elif cmd == "/memory":
            memories = tools.listMemories()
            chat.write(Text("📦  Stored Memories", style="bold yellow"))
            chat.write(Text(memories if memories else "No memories stored yet.", style="white"))
            chat.write(Text("─" * 60, style="dim white"))

        elif cmd in ("/save", "/s"):
            self.action_save_chat()

        elif cmd in ("/exit", "/quit", "/q"):
            self.exit()

        elif cmd == "/help":
            chat.write(HELP_TEXT)
            chat.write(Text("─" * 60, style="dim white"))

        else:
            chat.write(Text(f"Unknown command: {cmd}  —  type /help to see available commands.", style="red"))

    # ── Agent loop ─────────────────────────────────────────────────────────────

    async def _run_agent(self) -> None:
        """Step through the agent until it produces a final text response."""
        self.sub_title = "Thinking..."
        self._last_was_tool = False
        while True:
            response = await asyncio.to_thread(agent.step)
            self._render_response(response)
            if len(response) == 1:   # no tool call → Atlas is done
                break
        self._last_was_tool = False
        self._reset_subtitle()

    def _render_response(self, response: list) -> None:
        chat = self.query_one(RichLog)

        if len(response) > 1:
            # ── Tool call ───────────────────────────────────────────────────
            tool_call = response[0].tool_calls[0]
            name = tool_call.function.name
            args = tool_call.function.arguments
            if isinstance(args, str):
                args = json.loads(args)
            result = response[1]["content"]

            icon = TOOL_ICONS.get(name, "⚙️")
            self.sub_title = f"{icon} {name}  ·  running..."

            # connector between consecutive tool calls
            if self._last_was_tool:
                chat.write(Text("          │", style="dim white"))
                chat.write(Text("          │", style="dim white"))

            text = Text()
            text.append(f" {icon}  ", style="bold white")
            text.append(name + "\n", style="bold white")
            text.append("  " + "─" * 50 + "\n", style="dim white")

            if args:
                for k, v in args.items():
                    v_str = str(v).replace("\n", " ")
                    truncated = v_str if len(v_str) <= 55 else v_str[:55] + "…"
                    text.append(f"  {k}  ", style="dim white")
                    text.append(truncated + "\n", style="white")
                text.append("  " + "─" * 50 + "\n", style="dim white")

            result_preview = result[:350] + ("…" if len(result) > 350 else "")
            text.append("  ↳  ", style="dim white")
            text.append(result_preview.replace("\n", " "), style="white")

            chat.write(Panel(
                text,
                border_style="dim white",
                expand=False,
                padding=(0, 1),
            ))
            self._last_was_tool = True

        else:
            # ── Text response ───────────────────────────────────────────────
            self._last_was_tool = False
            content = response[0].content
            if content:
                self._write_bubble("Atlas", content, label_style="bold yellow", is_markdown=True)

    # ── Helpers ────────────────────────────────────────────────────────────────

    def _write_bubble(self, label: str, text: str, label_style: str = "bold white", is_markdown: bool = False) -> None:
        chat = self.query_one(RichLog)
        chat.write(Text(label, style=label_style))
        chat.write(Markdown(text) if is_markdown else Text(text, style="white"))
        chat.write(Text("─" * 60, style="dim white"))

    def _reset_subtitle(self) -> None:
        self.sub_title = f"v{config.get('version', '1.0')}  ·  {model}"

    # ── Bound actions ──────────────────────────────────────────────────────────

    def action_clear_chat(self)  -> None: self._handle_slash("/clear")
    def action_show_memory(self) -> None: self._handle_slash("/memory")

    def action_save_chat(self) -> None:
        chat = self.query_one(RichLog)
        filename = f"atlas_chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        lines = ["# Atlas Conversation\n"]
        for msg in agent.messages:
            is_dict = isinstance(msg, dict)
            role    = msg.get("role", "")           if is_dict else getattr(msg, "role", "")
            content = msg.get("content")            if is_dict else getattr(msg, "content", None)
            if role == "user" and content:
                lines.append(f"**You:** {content}\n")
            elif role == "assistant" and content:
                lines.append(f"**Atlas:** {content}\n")
        Path(baseDir / "memory/conversations" / filename).write_text("\n".join(lines), encoding="utf-8")
        chat.write(Text(f"✅  Conversation saved to {filename}", style="bold green"))

# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    AtlasTUI().run()