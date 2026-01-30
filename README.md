# 🤖 James - Your AI Coding Assistant

A highly intelligent AI-powered coding assistant that helps you create, test, and refine Python programs. James uses advanced language models to generate code, run tests, and iteratively improve programs based on user specifications.

**Status: Work in Progress** 🚧

## Features

- **Intelligent Code Generation**: Creates Python programs from natural language descriptions
- **Automated Testing**: Generates and runs comprehensive unit tests using Python's unittest framework
- **Iterative Refinement**: Analyzes test failures and modifies code until all tests pass
- **File System Tools**: Built-in tools for file operations, directory management, and command execution
- **Interactive Console**: Rich, colorful terminal interface with real-time feedback
- **Safety First**: Restricted file access and user confirmation for potentially dangerous operations

## Prerequisites

- Python 3.8 or higher
- A Groq API key (or compatible OpenAI API endpoint)

## Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
   cd "James - Your AI Coding Assistant"
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your API key:
   - Create a `.env` file in the project root
   - Add your Groq API key: `GROQ_API_KEY=your_api_key_here`
   - Ensure `.env` is added to `.gitignore`

## Configuration

Edit `config.json` to customize:
- `base_url`: API endpoint URL (default: Groq)
- `model`: Language model to use (default: openai/gpt-oss-120b)

## Usage

1. Run the agent:
   ```bash
   python agent.py
   ```

2. Follow the interactive prompts:
   - James will introduce himself and ask what you'd like to create
   - Describe your Python program requirements
   - James will create a `project/` directory and work within it

3. The agent will:
   - Create a detailed plan in `plan.md`
   - Generate tests in `tests.py`
   - Implement the main program in `main.py`
   - Run tests and refine code iteratively

## Project Structure

```
James - Your AI Coding Assistant/
├── agent.py              # Main agent interface
├── llm.py                # Language model integration
├── tools.py              # File system and utility tools
├── config.json           # Configuration settings
├── tools.json            # Tool definitions for LLM
├── system_prompt.txt     # System instructions
├── requirements.txt      # Python dependencies
├── messages.txt          # Conversation log
├── api.txt               # (Deprecated - use .env instead)
└── README.md             # This file
```

## Safety and Restrictions

- Core agent files are protected from modification
- Dangerous commands require user confirmation
- All file operations are restricted to the `project/` directory during development

## Contributing

This project is a work in progress. Contributions are welcome! Please:
- Test thoroughly before submitting changes
- Follow PEP 8 style guidelines
- Add appropriate error handling
- Update documentation as needed

## License

[Add license information here]

## Disclaimer

This tool is for educational and development purposes. Always review generated code before use in production environments.
