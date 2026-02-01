from openai import OpenAI
from typing import Callable
import json


class Agent:
    def __init__(self, base_url: str, api_key: str, model:str, toolsDesc: list = [], function_registry: dict = {}, system_prompt: str = "You are an AI Agent"):
        # Initialize OpenAI client
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.function_registry = function_registry
        self.tools = toolsDesc
        self.model = model
        self.messages = [{"role": "system", "content": system_prompt}]
        self.system_prompt = system_prompt

    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})

    def complete(self) -> str: 
        response = self.client.chat.completions.create(
            model=self.model,
            messages=self.messages,
            tools=self.tools,
            tool_choice="auto"
        ).choices[0].message
        self.messages.append(response)
        
        if response.tool_calls:
            for tool_call in response.tool_calls:
                tool_result = self.handle_tool_call(tool_call)
                self.messages.append(tool_result)
                return [response, tool_result]
        else:
            return [response]
        
    def handle_tool_call(self, tool_call) -> str:
        name = tool_call.function.name
        args = tool_call.function.arguments
        if isinstance(args, str):
                args = json.loads(args)
        id = tool_call.id
        result = ""
        try:
            result = str(self.function_registry[name](**args))
        except Exception as e:
            result = "Error occured while executing the tool: " + str(e)
        return {"role": "tool", "tool_call_id": id, "content": result}
    
    def prompt(self, user_input: str) -> str:
        self.add_message("user", user_input)
        return self.complete()
    
    def reset_messages(self):
        self.messages = [{"role": "system", "content": self.system_prompt}]

    
    