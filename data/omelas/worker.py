from chatbot import get_anthropic_message_with_tools
from instructions import DATA_DICTIONARY, QUERY_GEN
from tools import functions, tool_executor

def get_omelas_results(prompt):
    """
    Returns the results from the Omelas Dabatabse based on prompt
    :param prompt:
    :return:
    """
    return get_anthropic_message_with_tools(system_instructions=f"<instructions>{QUERY_GEN}</instructions><data_dict>{DATA_DICTIONARY}</data_dict>", prompt=prompt, functions=functions, tool_executor=tool_executor)

if __name__ == "__main__":
    print(get_results("What are Russian Telegram channels saying about the war in Ukraine?"))