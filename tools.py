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

def delete(file):  
    if file in forbidden:
        return "You are not allowed to delete these files."
    try:
        os.remove(file)
        return "File deleted successfully."
    except Exception as e:
        return "Error occured: " + str(e)

def createDirectory(directory):
    try:
        os.makedirs(directory, exist_ok=True)
        return "Directory created successfully."
    except Exception as e:
        return "Error occured: " + str(e)

def deleteDirectory(directory):
    if directory in forbidden:
        return "You are not allowed to delete these directories."
    try:
        os.rmdir(directory)
        return "Directory deleted successfully."
    except Exception as e:
        return "Error occured: " + str(e)

def moveFile(source, destination):
    if source in forbidden or destination in forbidden:
        return "You are not allowed to move these files."
    try:
        os.rename(source, destination)
        return "File moved successfully."
    except Exception as e:
        return "Error occured: " + str(e)

def copyFile(source, destination):
    if source in forbidden or destination in forbidden:
        return "You are not allowed to copy these files."
    try:
        import shutil
        shutil.copy2(source, destination)
        return "File copied successfully."
    except Exception as e:
        return "Error occured: " + str(e)
    
def getCurrentDirectory():
    try:
        cwd = os.getcwd()
        return f"Current directory is: {cwd}"
    except Exception:
        return "Error occured."

def runCommand(command):
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True
        )

        output = result.stdout
        return output
    except Exception:
        return "Error occured."

def fileExists(file):
    return os.path.exists(file)

def getFileSize(file):
    try:
        size = os.path.getsize(file)
        return f"Size of {file} is {size} bytes."
    except Exception as e:
        return "Error occured: " + str(e)
