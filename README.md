<div align="center">

```
 █████╗ ████████╗██╗      █████╗ ███████╗ ██████╗██╗     ██╗
██╔══██╗╚══██╔══╝██║     ██╔══██╗██╔════╝██╔════╝██║     ██║
███████║   ██║   ██║     ███████║███████╗██║     ██║     ██║
██╔══██║   ██║   ██║     ██╔══██║╚════██║██║     ██║     ██║
██║  ██║   ██║   ███████╗██║  ██║███████║╚██████╗███████╗██║
╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝╚══════╝╚═╝
```

**AtlasCLI — Your local AI agent for file management, automation, and persistent memory.**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Powered by Groq](https://img.shields.io/badge/Powered%20by-Groq-orange?style=flat)](https://groq.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-green?style=flat)](LICENSE)

</div>

---

## What is AtlasCLI?

AtlasCLI is a fully local AI agent CLI that runs right in your terminal. Talk to it in plain English and it will manage your files, browse the web, remember things you tell it, and get stuff done — all from your own machine, with your data never leaving your computer.

No cloud storage. No subscriptions. No tracking. Just a fast, capable agent that works for you.

---

## Features

### 📁 Full File System Control
- Create, read, write, delete, move, copy, and rename files and directories
- Batch move or copy multiple files at once
- Read specific line ranges from large files
- Visualize folder structures with customizable depth directory trees
- Check file existence and sizes on the fly

### 🧠 Persistent Memory
- Store and recall facts across sessions using a simple key-value memory system
- Atlas remembers your preferences, project names, and important context between conversations
- All memory stored locally in JSON format — you own it completely

### 🌐 Web Access
- Search the web and extract text content from URLs
- Great for quick research or pulling in external information during a session

### 🎨 Full Terminal UI (TUI)
- Built with [Textual](https://github.com/Textualize/textual) — a modern, reactive TUI framework
- Scrollable chat view with a fixed input bar and live clock header
- Slash commands with an **autocomplete dropdown** that appears as you type `/`
- Keyboard shortcuts shown persistently in the footer bar
- Live status updates in the header: `Thinking...`, `Running: readFile...`
- Tool execution panels rendered inline in the chat as Atlas works
- Markdown rendering for all Atlas responses

### 🔒 Private by Design
- Runs 100% locally on your machine
- Your files, conversations, and memory never touch an external server
- Critical system files are protected from accidental modification

---

## Getting Started

### Prerequisites
- Python 3.8+
- A free GROQ API key — grab one at [groq.com](https://groq.com)

### Installation

```bash
git clone https://github.com/tawfickobtan/AtlasCLI
cd Atlas
pip install -r requirements.txt
```

### Set Your API Key

**Windows (PowerShell)**
```powershell
$env:GROQ_API_KEY="your-groq-api-key"
```

**Windows (CMD)**
```cmd
setx GROQ_API_KEY "your-groq-api-key"
```

**Mac / Linux**
```bash
export GROQ_API_KEY="your-groq-api-key"
```

### Run AtlasCLI

```bash
python atlas.py
```

That's it. Start chatting!

---

## Slash Commands & Key Bindings

| Command | What it does |
|---|---|
| `/clear` | Reset the conversation history |
| `/memory` | Show everything Atlas has remembered |
| `/save` | Export the conversation to a timestamped `.md` file |
| `/exit` | Quit AtlasCLI cleanly |
| `/help` | Show all commands and key bindings |

Type `/` and a **dropdown list** of matching commands appears instantly — select with arrow keys or click.

| Shortcut | Action |
|---|---|
| `Ctrl+L` | Clear chat |
| `Ctrl+S` | Save chat |
| `Ctrl+M` | Show memory |
| `Ctrl+Q` | Quit |

---

## Configuration

Edit `configuration/config.json` to switch models or change the base URL:

```json
{
  "base_url": "https://api.groq.com/openai/v1",
  "model": "openai/gpt-oss-120b",
  "version": "1.0.1"
}
```

Want to change Atlas's personality or behavior? Edit `configuration/AGENT.md` — it's the system prompt, written in plain Markdown.

---

## Available Tools

<details>
<summary><strong>File Operations</strong></summary>

| Tool | Description |
|---|---|
| `createFile` | Create a new empty file |
| `readFile` | Read the full contents of a file |
| `readFileLines` | Read specific line ranges from a file |
| `deleteFiles` | Delete one or more files |
| `moveFiles` / `copyFiles` | Move or copy one or more files |
| `renameFile` | Rename a file |
| `fileExists` | Check if a file exists |
| `getFileSize` | Get the size of a file |

</details>

<details>
<summary><strong>Directory Operations</strong></summary>

| Tool | Description |
|---|---|
| `createDirectory` | Create a new directory |
| `deleteDirectory` | Delete a directory |
| `getItemsInPath` | List contents of a directory |
| `getCurrentDirectory` | Get the current working directory |

</details>

<details>
<summary><strong>Memory Management</strong></summary>

| Tool | Description |
|---|---|
| `rememberFact` | Store a key-value fact persistently |
| `recallFact` | Retrieve a stored fact by key |
| `forgetFact` | Delete a specific memory |
| `listMemories` | View all stored facts |

</details>

<details>
<summary><strong>Web & Research</strong></summary>

| Tool | Description |
|---|---|
| `searchWeb` | Search the web from the terminal |
| `extractTextFromUrl` | Extract readable text from any URL |
| `readPdfPages` | Read content from PDF files |

</details>

---

## Project Structure

```
AtlasCLI/
├── atlas.py                  # Textual TUI entry point (run this!)
├── requirements.txt          # Python dependencies
├── agent/
│   ├── agent.py              # Core Agent class with tool-calling loop
│   ├── tools.py              # All tool implementations
│   └── tools.json            # Tool schemas for function calling
├── configuration/
│   ├── config.json           # Model and API settings
│   └── AGENT.md              # System prompt / agent personality
└── memory/
    └── memory.json           # Persistent local memory storage
```

---

## Tech Stack

| Component | Technology |
|---|---|
| LLM API | [Groq](https://groq.com) (OpenAI-compatible) |
| TUI Framework | [Textual](https://github.com/Textualize/textual) |
| Rich Rendering | [Rich](https://github.com/Textualize/rich) |
| HTTP Client | [Requests](https://docs.python-requests.org/) |
| Memory | Local JSON storage |
| Config | JSON + Markdown system prompt |

---

## Contributing

Contributions are welcome and appreciated! Whether it's a bug fix, a new tool idea, or a documentation improvement — feel free to open an issue or submit a pull request.

---

<div align="center">

Made with ❤️ by [Tawfic Kobtan](https://www.linkedin.com/in/tawfic-kobtan)

</div>

