import json
import os
import subprocess
import time
from pathlib import Path
from bs4 import BeautifulSoup

baseDir = Path(__file__).resolve().parent

def normalizePath(path: str) -> str:
    return str(Path(path).expanduser().resolve())

forbidden = [
    str((baseDir / "agent.py").resolve()),
    str((baseDir / "config.json").resolve()),
    str((baseDir / "llm.py").resolve()),
    str((baseDir / "README.md").resolve()),
    str((baseDir / "tools.json").resolve()),
    str((baseDir / "tools.py").resolve()),
    str((baseDir / ".gitignore").resolve()),
    str((baseDir / ".git").resolve()),
    str((baseDir / "system_prompt.txt").resolve()),
    str((baseDir / "requirements.txt").resolve())
]

def isForbidden(path: str) -> bool:
    normalized = normalizePath(path)
    for item in forbidden:
        if normalized.endswith(item):
            return True
    return False

# Load memory file
memory = {}
try:
    with open(os.path.join(baseDir, "..", "memory/memory.json"), "r", encoding="utf-8") as f:
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
    if isForbidden(file):
        return "You are not allowed to create these files."
    try:
        with open(file, "w", encoding="utf-8") as f:
            pass
        return "File created successfully."
    except Exception as e:
        return "Error occured: " + str(e)

def readFile(file: str) -> str:
    try:
        with open(file, "r", encoding="utf-8") as f:
            output = f.read()
        return "content:\n" + output    
    except Exception as e:
        return "Error occured. " + str(e)
    
def readPdfPages(file: str, start_page: int, end_page: int) -> str:
    try:
        import PyPDF2
        start_page = max(start_page - 1, 0)  # Convert to 0-indexed
        end_page = max(end_page - 1, 0)
        with open(file, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages[start_page:end_page + 1]:
                text += page.extract_text() + "\n"
        return "content:\n" + text + "\n\n" + f"[Extracted pages {start_page + 1} to {end_page + 1} out of {len(reader.pages)} pages from {file}]"
    except Exception as e:
        return "Error occured. " + str(e)


def readFileLines(file: str, start_line: int, end_line: int) -> str:
    """Reads specific lines from a file. Line numbers are 1-indexed."""
    try:
        with open(file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # Validate line numbers
        if start_line < 1 or end_line < 1:
            return "Error: Line numbers must be 1 or greater."
        if start_line > len(lines):
            return f"Error: File only has {len(lines)} lines, but you asked for line {start_line}."
        
        # Adjust to 0-indexed and clamp end_line
        start_idx = start_line - 1
        end_idx = min(end_line, len(lines))
        
        selected_lines = lines[start_idx:end_idx]
        content = "".join(selected_lines)
        
        return f"Lines {start_line}-{end_idx} of {file}:\n{content}"
    except Exception as e:
        return "Error occured: " + str(e)

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
    
def moveMultipleFiles(sources: list, destination: str) -> str:
    if destination in forbidden:
        return "You are not allowed to move files to this destination."
    success = []
    failed = []
    for source in sources:
        if source in forbidden:
            failed.append(source)
            continue
        try:
            os.rename(source, os.path.join(destination, os.path.basename(source)))
            success.append(source)
        except Exception as e:
            failed.append(source)

    return "Successfully moved:" + "\n" +  '\n'.join(success) + "\n\n" + "Failed to move:" + "\n" + '\n'.join(failed) + "."
    
def copyMultipleFiles(sources: list, destination: str) -> str:
    if destination in forbidden:
        return "You are not allowed to copy files to this destination."
    success = []
    failed = []
    for source in sources:
        if source in forbidden:
            failed.append(source)
            continue
        try:
            import shutil
            shutil.copy2(source, os.path.join(destination, os.path.basename(source)))
            success.append(source)
        except Exception as e:
            failed.append(source)

    return "Successfully copied:" + "\n" +  '\n'.join(success) + "\n\n" + "Failed to copy:" + "\n" + '\n'.join(failed) + "."
    
def getCurrentDirectory() -> str:
    try:
        cwd = os.getcwd()
        return cwd
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

def renameFile(source: str, new_name: str) -> str:
    if source in forbidden or new_name in forbidden:
        return "You are not allowed to rename these files."
    try:
        os.rename(source, new_name)
        return "File renamed successfully."
    except Exception as e:
        return "Error occured: " + str(e)
    
# Tool functions for memory management 
def rememberFact(key: str, fact: str) -> str:
    memory[key] = fact
    try:
        with open(os.path.join(baseDir, "..", "memory/memory.json"), "w", encoding="utf-8") as f:
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
            with open(os.path.join(baseDir, "..", "memory/memory.json"), "w", encoding="utf-8") as f:
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

## Web browsing tools
def searchWeb(query: str, k: int = 3) -> str:
    try:
        from urllib.parse import quote_plus
        import requests
        
        encoded = quote_plus(query)
        url = f"https://html.duckduckgo.com/html/?q={encoded}"
        
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        with open("temp.txt", "w", encoding="utf-8") as f:
            f.write(response.text)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        for result in soup.find_all('div', class_='result'):
            title = result.find('a', class_='result__a')
            if title:
                results.append(title.get_text() + "\n(Link: " + title.get("href", "None") + ")")
            if len(results) >= k:
                break
        return "\n".join(results) if results else "No results found."
    except Exception as e:
        return "Error occured: " + str(e)
    
def extractTextFromUrl(url: str) -> str:
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        import re
        
        # Setup headless Chrome
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        
        driver = webdriver.Chrome(options=options)
        driver.get(url)
        
        # Wait a bit for JS to load
        import time
        time.sleep(3)
        
        html = driver.page_source
        driver.quit()
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Try to find main content using common patterns (in order of preference)
        content = (
            soup.find('article') or           # Most modern sites use <article>
            soup.find('main') or              # HTML5 semantic tag
            soup.find('div', id='content') or # Common pattern
            soup.find('div', class_='content') or
            soup.find('div', id='main') or
            soup.find('div', class_='main') or
            soup.body                         # Last resort: entire body
        )
        
        if not content:
            return "Could not find main content area."
        
        # Remove unwanted elements (noise)
        unwanted_tags = ['script', 'style', 'nav', 'header', 'footer', 'aside', 'iframe', 'noscript']
        for tag in unwanted_tags:
            for element in content.find_all(tag):
                element.decompose()
        
        # Get all paragraph text (usually the main content)
        paragraphs = content.find_all('p')
        text = '\n\n'.join([p.get_text(' ', strip=True) for p in paragraphs if p.get_text(strip=True)])
        
        # If no paragraphs found, get all text
        if not text:
            text = content.get_text(' ', strip=True)
        
        # Clean up excessive whitespace/newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        text = re.sub(r' {2,}', ' ', text)
        
        # Limit length to prevent overwhelming the LLM
        if len(text) > 2000:
            text = text[:2000] + "\n\n[Content truncated...]"
        
        if text:
            extracted_content = Path(baseDir / "../memory/extracted_content.txt").resolve()
            with extracted_content.open("w", encoding="utf-8") as f:
                f.write(text)
            return "Text content extracted and saved to " + str(extracted_content) + ".\n\nUse readFileLines with the appropriate line numbers to read the content efficiently without wasting context."
        else:
            return "No text content could be extracted from the page."
        
    except Exception as e:
        return f"Error extracting webpage: {str(e)}"
