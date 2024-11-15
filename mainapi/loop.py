# Implementing Loop Logic

# Ingest initial filtered results of data sources

# Create In-Depth Research based on the result

# Send follow up questions back to initial prompt


import json, ast
import requests


json_validator = {
    "name": "validate_json",
    "description": "Validates if a string is valid JSON",
    "input_schema": {
        "type": "object",
        "properties": {
            "json_str": {
                "type": "string",
                "description": "The JSON string to validate"
            }
        },
        "required": ["json_str"]
    }
}

def enhanced_tool_executor(tool_name, tool_input, tool_executor):
    if tool_name == "validate_json":
        try:
            result = load_json(tool_input["json_str"])
            return json.dumps({"success": True, "result": result})
        except ValueError as e:
            return json.dumps({"error": f"Invalid JSON: {str(e)}"})
    return tool_executor(tool_name, tool_input) if tool_executor else None


def load_json(json_str):
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as json_error:
        try:
            return ast.literal_eval(json_str)
        except (ValueError, SyntaxError) as ast_error:
            raise ValueError(f"json.loads failed with error: {json_error}. ast.literal_eval failed with error: {ast_error}")


# Example class that contains the _get_llm_response method
class LLMHandler:
    def _get_llm_response(self, system_instructions, prompt, model=None, functions=None, function_call="auto",
                          tool_executor=None):
        """
        Gets a response from the new model API, with optional tool usage.
        """
        model = "neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8"
        url = "https://hackathon.niprgpt.mil/llama/v1/chat/completions"
        headers = {
            "Authorization": "Bearer YOUR_API_KEY",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_instructions:
            messages.append({"role": "system", "content": system_instructions})
        messages.append({"role": "user", "content": prompt})

        if functions:
            function_call_info = True
            functions.append(json_validator)

            while function_call_info:
                data = {
                    "model": model,
                    "messages": messages,
                    "temperature": 0.7
                }
                response = requests.post(url, headers=headers, json=data)
                response_data = response.json()
                content = response_data['choices'][0]['message']['content']
                function_call_info = response_data['choices'][0]['message'].get('function_call')

                if function_call_info and tool_executor:
                    function_name = function_call_info['name']
                    function_args = json.loads(function_call_info['arguments'])
                    try:
                        function_response = enhanced_tool_executor(function_name, function_args, tool_executor)
                        if function_name in ('json_validator', 'validator'):
                            return {
                                'message': function_response,
                                'input_tokens': response_data['usage']['prompt_tokens'],
                                'output_tokens': response_data['usage']['completion_tokens'],
                                'model': model
                            }
                    except Exception as e:
                        function_response = str(e)

                    messages.append(response_data['choices'][0]['message'])

                    messages.append({
                        "role": "function",
                        "name": function_name,
                        "content": json.dumps(function_response)
                    })
                else:
                    return {
                        'message': content.strip(),
                        'input_tokens': response_data['usage']['prompt_tokens'],
                        'output_tokens': response_data['usage']['completion_tokens'],
                        'model': model
                    }
        else:
            data = {
                "model": model,
                "messages": messages,
                "temperature": 0.7
            }
            response = requests.post(url, headers=headers, json=data)
            response_data = response.json()
            content = response_data['choices'][0]['message']['content']
            return {
                'message': content.strip(),
                'input_tokens': response_data['usage']['prompt_tokens'],
                'output_tokens': response_data['usage']['completion_tokens'],
                'model': model
            }


def call_llm_response():
    llm_handler = LLMHandler()
    system_instructions = "You are a helpful assistant."
    prompt = """
What is the capital of USA?


"""
    model = "neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8"
    functions = []  # Add any functions you want to use
    response = llm_handler._get_llm_response(system_instructions, prompt, model=model, functions=functions)
    print(response)

call_llm_response()
