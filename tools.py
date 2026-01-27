import os
import subprocess

forbidden = [
    "agent.py",
    "config.json",
    "llm.py",
    "README.MD",
    "tools.json",
    "tools.py"
]

def getItemsInPath(path):
    return os.listdir(path)

def writeIntoFile(file, content):
    if file in forbidden:
        return "You are not allowed to modify these files."
    with open(file, "w") as f:
        f.write(content)
    return "Wrote content into file successfully."
    
def readFile(file):
    with open(file, "r") as f:
        output = f.read()
    return output

def runPythonFile(file):
    subprocess.run("python " + file)

