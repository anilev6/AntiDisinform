from openai import OpenAI
import json, ast, os


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


def get_anthropic_message_with_tools(system_instructions, prompt, functions=None, tool_executor=None):
    import anthropic

    model = "claude-3-5-sonnet-latest"
    max_tokens = 8192
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"], max_retries=3)
    if functions:
        functions = [*functions, json_validator]
    else:
        functions = [json_validator]

    messages = []
    if system_instructions:
        messages.append({"role": "user", "content": [
            {"type": "text", "text": f"<system_instructions>{system_instructions}</system_instructions>"}]})
    messages.append({"role": "user", "content": [{"type": "text", "text": prompt}]})

    while True:
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            tools=functions,
            messages=messages,
        )

        content_blocks = response.content
        found_tool_use = False

        for block in content_blocks:
            if block.type == 'tool_use':
                found_tool_use = True
                tool_use_id = block.id
                tool_name = block.name
                tool_input = block.input

                try:
                    tool_result = enhanced_tool_executor(tool_name, tool_input, tool_executor)
                    if tool_name == "call_gbq_function":
                        if not tool_result.startswith("ERROR") and len(tool_result) > 2:
                            return tool_result
                    is_error = True

                    if tool_name in ("validator", "validate_json"):
                        validation_result = load_json(tool_result)
                        if "success" in validation_result:
                            # Only return if we have a valid JSON and it's from the validator
                            return validation_result["response"]
                except Exception as e:
                    tool_result = str(e)
                    is_error = True

                messages.append({"role": "assistant", "content": content_blocks})
                messages.append({
                    "role": "user",
                    "content": [{
                        "type": "tool_result",
                        "tool_use_id": tool_use_id,
                        "content": [{"type": "text", "text": tool_result}],
                        "is_error": is_error
                    }]
                })
                break

        if not found_tool_use:
            print("No function call found")
            messages.append({
                "role": "user",
                "content": [{
                    "type": "text",
                    "text": "Please validate your response is properly formatted JSON. Respond only with a json or the function will fail."
                }]
            })