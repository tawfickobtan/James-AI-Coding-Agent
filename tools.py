import os
import subprocess

forbidden = [
    "agent.py",
    "config.json",
    "llm.py",
    "README.MD",
    "tools.json",
    "tools.py",
    ".gitignore",
    "system_prompt.txt"
]

def getItemsInPath(path):
    return os.listdir(path)

def createFile(file):
    open(file, "w").close()

def writeIntoFile(file, content):
    if file in forbidden:
        return "You are not allowed to modify these files."
    try:
        with open(file, "w", encoding="utf-8") as f:
            f.write(content)
        return "Wrote content into file successfully."
    except Exception as e:
        return "Error occured: " + str(e)
    
def readFile(file):
    try:
        with open(file, "r") as f:
            output = f.read()
        return "content:\n" + output    
    except Exception:
        return "Error occured."

def runPythonFile(file):
    if file in forbidden:
        return "Cannot run this file."
    try:
        result = subprocess.run(
            "python " + file,
            shell=True,
            capture_output=True,
            text=True
        )

        output = result.stdout
        return output
    except Exception:
        return "Error occured."
