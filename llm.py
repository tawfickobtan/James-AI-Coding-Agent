from openai import OpenAI
import os
import json
from pathlib import Path
baseDir = Path(__file__).resolve().parent

# Get configuration file
config = {}
with open(baseDir / "config.json", "r") as f:
    config = json.load(f)

# Get tool file
tools = []
with open(baseDir / "tools.json", "r") as f:
    tools = json.load(f)

client = OpenAI(
    api_key=os.environ.get("GROQ_API_KEY"),
    base_url=config["base_url"]
)

def complete(messages):
    return client.chat.completions.create(
        messages=messages,
        model=config["model"],
        tools=tools,
        tool_choice="auto"
    ).choices[0].message
