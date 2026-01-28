from llm import complete
import tools
import json

# Load config file
config = {}
with open("config.json", "r") as f:
    config = json.load(f)

systemPrompt = ""
with open("system_prompt.txt", "r") as f:
    systemPrompt = f.read()


# Define function registry
functionRegistry = {
    "getItemsInPath": tools.getItemsInPath,
    "writeIntoFile": tools.writeIntoFile,
    "readFile": tools.readFile,
    "createFile": tools.createFile,
    "delete": tools.delete,
    "createDirectory": tools.createDirectory,
    "deleteDirectory": tools.deleteDirectory,
    "moveFile": tools.moveFile,
    "copyFile": tools.copyFile,
    "getCurrentDirectory": tools.getCurrentDirectory,
    "runCommand": tools.runCommand,
    "fileExists": tools.fileExists,
    "getFileSize": tools.getFileSize,
}

# Initialise messages with system prompt
messages = [
    {"role": "system",
     "content": systemPrompt}
]

response = complete(messages)
messages.append(response)
print("🤖 James:")
print(response.content)
print("_________________")
print()

while True:
    print("👨🏻 User:")
    userInput = input()
    print("_________________")
    print()
    messages.append({
        "role": "user",
        "content": userInput
    })

    while True:
        response = complete(messages)
        messages.append(response)

        if response.tool_calls:
            for tool_call in response.tool_calls:
                id = tool_call.id
                name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                print("🛠️ Executing:")
                print(name)
                for arg in args:
                    print(arg, (args[arg] if len(args[arg]) < 50 else args[arg][:50] + "..."))
                print()
                result = functionRegistry[name](**args)
                print("result:")
                print(result)
                messages.append({
                    "role": "tool",
                    "tool_call_id": id,
                    "content": str(result)
                })
        else:
            print("🤖 James:")
            print(response.content)
            print("_________________")
            print() 
            break