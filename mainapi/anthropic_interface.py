from data.omelas.chatbot import get_anthropic_message_with_tools
from utils import tool_executor, functions
from instructions import INSTRUCTIONS

def call_system(prompt):
    res = get_anthropic_message_with_tools(INSTRUCTIONS, prompt, functions, tool_executor)
    return "#" + res.split("#", maxsplit=1)[-1]

if __name__ == "__main__":
    print(call_system("What are the biggest threats in the war in Ukraine?"))