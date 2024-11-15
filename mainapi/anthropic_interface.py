from data.omelas.chatbot import get_anthropic_message_with_tools
from utils import tool_executor, functions
from instructions import INSTRUCTIONS

get_anthropic_message_with_tools(INSTRUCTIONS, "What are the biggest threats in the war in Ukraine?", functions, tool_executor)