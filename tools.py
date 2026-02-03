import json
import os
import subprocess


forbidden = [
    "agent.py",
    "config.json",
    "llm.py",
    "README.md",
    "tools.json",
    "tools.py",
    ".gitignore",
    ".git",
    "system_prompt.txt",
    "requirements.txt"
]

# Load memory file
memory = {}
try:
    with open("memory.json", "r", encoding="utf-8") as f:
        memory = json.load(f)
except Exception as e:
    memory = {}

def getItemsInPath(path: str) -> str:
    try:
        items = os.listdir(path)
        return "\n".join(items)
    except Exception as e:
        return "Error occured. " + str(e)

def createFile(file: str) -> str:
    if file in forbidden:
        return "You are not allowed to create these files."
    try:
        with open(file, "w", encoding="utf-8") as f:
            pass
        return "File created successfully."
    except Exception as e:
        return "Error occured: " + str(e)

def writeIntoFile(file: str, content: str) -> str:
    if file in forbidden:
        return "You are not allowed to modify these files."
    try:
        with open(file, "w", encoding="utf-8") as f:
            f.write(content)
        return "Wrote content into file successfully."
    except Exception as e:
        return "Error occured: " + str(e)
    
def readFile(file: str) -> str:
    try:
        with open(file, "r", encoding="utf-8") as f:
            output = f.read()
        return "content:\n" + output    
    except Exception as e:
        return "Error occured. " + str(e)

def delete(file: str) -> str:  
    if file in forbidden:
        return "You are not allowed to delete these files."
    try:
        os.remove(file)
        return "File deleted successfully."
    except Exception as e:
        return "Error occured: " + str(e)

def createDirectory(directory: str) -> str:
    try:
        os.makedirs(directory, exist_ok=True)
        return "Directory created successfully."
    except Exception as e:
        return "Error occured: " + str(e)

def deleteDirectory(directory: str) -> str:
    if directory in forbidden:
        return "You are not allowed to delete these directories."
    try:
        os.rmdir(directory)
        return "Directory deleted successfully."
    except Exception as e:
        return "Error occured: " + str(e)

def moveFile(source: str, destination: str) -> str:
    if source in forbidden or destination in forbidden:
        return "You are not allowed to move these files."
    try:
        os.rename(source, destination)
        return "File moved successfully."
    except Exception as e:
        return "Error occured: " + str(e)

def copyFile(source: str, destination: str) -> str:
    if source in forbidden or destination in forbidden:
        return "You are not allowed to copy these files."
    try:
        import shutil
        shutil.copy2(source, destination)
        return "File copied successfully."
    except Exception as e:
        return "Error occured: " + str(e)
    
def getCurrentDirectory() -> str:
    try:
        cwd = os.getcwd()
        return cwd
    except Exception as e:
        return "Error occured. " + str(e)

def runCommand(command: str) -> str:
    userInput = input("Are you sure you want to run this command? (y/n): ")
    if userInput.lower().strip() != "y":
        return "Command execution cancelled by user."
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        output = result.stdout
        return output
    except Exception as e:
        return "Error occured. " + str(e)

def fileExists(file: str) -> str:
    try:
        return ("Yes, " + file + " exists.") if os.path.exists(file) else ("No, " + file + " does not exist.")
    except Exception as e:
        return "Error occured: " + str(e)

def getFileSize(file: str) -> str:
    try:
        size = os.path.getsize(file)
        return f"Size of {file} is {size} bytes."
    except Exception as e:
        return "Error occured: " + str(e)

def readPDF(path: str) -> str:
    try:
        from PyPDF2 import PdfReader
        reader = PdfReader(path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return "content:\n" + text
    except Exception as e:
        return "Error occured: " + str(e)
    
def renameFile(source: str, new_name: str) -> str:
    if source in forbidden or new_name in forbidden:
        return "You are not allowed to rename these files."
    try:
        os.rename(source, new_name)
        return "File renamed successfully."
    except Exception as e:
        return "Error occured: " + str(e)
    
def rememberFact(key: str, fact: str) -> str:
    memory[key] = fact
    try:
        with open("memory.json", "w", encoding="utf-8") as f:
            json.dump(memory, f, indent=4)
        return "Fact remembered successfully."
    except Exception as e:
        return "Error occured: " + str(e)

def recallFact(key: str) -> str:
    try:
        fact = memory.get(key, "No fact found for the given key.")
        return fact
    except Exception as e:
        return "Error occured: " + str(e)

def forgetFact(key: str) -> str:
    try:
        if key in memory:
            del memory[key]
            with open("memory.json", "w", encoding="utf-8") as f:
                json.dump(memory, f, indent=4)
            return "Fact forgotten successfully."
        else:
            return "No fact found for the given key."
    except Exception as e:
        return "Error occured: " + str(e)
    
def listMemories() -> str:
    try:
        if memory:
            facts = "\n".join([f"{k}: {v}" for k, v in memory.items()])
            return facts
        else:
            return "No memories stored."
    except Exception as e:
        return "Error occured: " + str(e)

