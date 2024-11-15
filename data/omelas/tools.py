from data.omelas.gcp import call_gbq_function
from typing import Dict


class IncorrectToolUsage(Exception):
    pass


def tool_executor(function_name: str, function_args: Dict) -> str:
    if function_name == 'call_gbq_function':
        query = function_args.get('query')
        print("Calling get call_gbq_function")
        return str(call_gbq_function(query))
    raise ValueError(f"Unknown function: {function_name}, avaliable functions are: {', '.join([f['name'] for f in functions])}")


functions = [
    {
        "name": "call_gbq_function",
        "description": "Retrieve data from Database",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The query to execute."
                }
            },
            "required": ["query"]
        }
    }
]