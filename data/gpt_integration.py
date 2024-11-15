import json, ast


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


def _get_chatgpt_response(self, system_instructions, prompt, model=None, functions=None, function_call="auto",
                          tool_executor=None):
    """
    Gets a response from the OpenAI ChatGPT API, with optional tool usage, using the latest OpenAI SDK.
    """
    model = self.model or "gpt-4o-mini"
    client = self.openai_client
    messages = []
    if system_instructions:
        messages.append({"role": "system", "content": system_instructions})
    messages.append({"role": "user", "content": prompt})

    if functions:
        function_call_info = True
        functions.append(json_validator)

        while function_call_info:
            response = client.chat.completions.create(
                model=model,
                response_format={"type": "json_object"},
                messages=messages,
                functions=functions,
                function_call=function_call
            )
            message = response.choices[0].message
            content = message.content
            function_call_info = message.function_call

            if function_call_info and tool_executor:
                function_name = function_call_info.name
                function_args = json.loads(function_call_info.arguments)
                try:
                    function_response = enhanced_tool_executor(function_name, function_args, tool_executor)
                    if function_name in ('json_validator', 'validator'):
                        return {
                            'message': function_response,
                            'input_tokens': response.usage.prompt_tokens,
                            'output_tokens': response.usage.completion_tokens,
                            'model': model
                        }
                except Exception as e:
                    function_response = str(e)

                # Append the assistant's function call to messages
                messages.append(message)

                # Append the function's response to messages
                messages.append({
                    "role": "function",
                    "name": function_name,
                    "content": json.dumps(function_response)
                })
            else:
                # No function call, return the assistant's response
                return {
                    'message': content.strip(),
                    'input_tokens': response.usage.prompt_tokens,
                    'output_tokens': response.usage.completion_tokens,
                    'model': model
                }
    else:
        # Regular completion without functions
        response = client.chat.completions.create(
            model=model,
            messages=messages
        )
        message = response.choices[0].message
        content = message.content
        return {
            'message': content.strip(),
            'input_tokens': response['usage']['prompt_tokens'],
            'output_tokens': response['usage']['completion_tokens'],
            'model': model
        }