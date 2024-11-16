from data.omelas.chatbot import get_anthropic_message_with_tools
from utils import tool_executor, functions
from instructions import INSTRUCTIONS

def call_system(prompt):
    res = get_anthropic_message_with_tools(INSTRUCTIONS, prompt, functions, tool_executor)
    return "#" + res.split("#", maxsplit=1)[-1]

if __name__ == "__main__":
    res = call_system("What's going on in the war in Ukraine over the past three days?'")
    print("\n\n")
    print("-"*80)
    print("\n\n")
    print(res)
