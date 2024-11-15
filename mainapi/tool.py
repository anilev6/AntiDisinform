import json
import ast
import requests
from typing import Optional, Dict, Any
import os
# from dotenv import load_dotenv
from utils import tool_executor, functions
from data.omelas.worker import get_omelas_results
from data_sources.search_scraper import get_search_and_scrape
from mainapi.instructions import INSTRUCTIONS

def _get_omelas_results(query):
    return get_omelas_results(query)

def _get_search_results(search_engine, search_query):
    return get_search_and_scrape(search_engine=search_engine, search_query=search_query)

# Define the function schemas
json_validator = {
    "name": "validate_json",
    "description": "Validates if a string is valid JSON. Use this when you need to check if a string is valid JSON format.",
    "parameters": {
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


def load_json(json_str: str) -> Any:
    try:
        return json.loads(json_str)
    except json.JSONDecodeError as json_error:
        try:
            return ast.literal_eval(json_str)
        except (ValueError, SyntaxError) as ast_error:
            raise ValueError(f"json.loads failed with error: {json_error}. ast.literal_eval failed with error: {ast_error}")

def enhanced_tool_executor(tool_name: str, tool_input: Dict[str, Any]) -> str:
    try:
        if tool_name == "validate_json":
            result = load_json(tool_input["json_str"])
            return json.dumps({"success": True, "result": result})
        elif tool_name in ("get_omelas_results", "get_search_results"):
            result = tool_executor(tool_name, tool_input)  
            return json.dumps({"data": result})
        else:
            return json.dumps({"error": f"Unknown tool: {tool_name}"})
    except Exception as e:
        return json.dumps({"error": str(e)})

class LLMHandler:
    def _get_llm_response(
        self,
        prompt: str,
        system_instructions: str = INSTRUCTIONS,
        model: Optional[str] = None,
        functions: Optional[list] = None
    ) -> Dict[str, Any]:
        """
        Gets a response from the LLM API, with automatic tool selection.
        """
        model = model or "neuralmagic/Meta-Llama-3.1-70B-Instruct-FP8"
        url = "https://hackathon.niprgpt.mil/llama/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {os.getenv('YOUR_API_KEY')}",
            "Content-Type": "application/json"
        }
        
        try:
            messages = []
            if system_instructions:
                messages.append({
                    "role": "system", 
                    "content": system_instructions + " You have access to tools for checking weather and validating JSON. Select and use the appropriate tool when needed."
                })
            messages.append({"role": "user", "content": prompt})

            # Base request data
            data = {
                "model": model,
                "messages": messages,
                "temperature": 0.7,
                "max_tokens": 1000,
                "stream": False
            }

            # Add tools if provided
            if functions:
                data["tools"] = [{"type": "function", "function": f} for f in functions]
                # Let the model choose which tool to use
                data["tool_choice"] = "auto"

            # Print the request payload for debugging
            # print("\nRequest payload:", json.dumps(data, indent=2))

            # Make the API call
            response = requests.post(url, headers=headers, json=data)
            
            # Print raw response for debugging
            print("\nResponse status code:", response.status_code)
            print("Raw response:", response.text)

            # If the response is not JSON, return an error
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                return {
                    'error': f'Invalid JSON response from API. Status code: {response.status_code}',
                    'raw_response': response.text
                }

            # Handle different response formats
            if 'error' in response_data:
                return {'error': response_data['error']}

            # Handle both tool calls and regular responses
            if 'choices' in response_data and len(response_data['choices']) > 0:
                message = response_data['choices'][0].get('message', {})
                tool_calls = message.get('tool_calls', [])

                if tool_calls:
                    results = []
                    for tool_call in tool_calls:
                        function_name = tool_call['function']['name']
                        try:
                            function_args = json.loads(tool_call['function']['arguments'])
                            function_response = enhanced_tool_executor(function_name, function_args)
                            
                            # Add the tool response to messages for context
                            messages.append({
                                "role": "assistant",
                                "content": None,
                                "tool_calls": [tool_call]
                            })
                            messages.append({
                                "role": "tool",
                                "tool_call_id": tool_call['id'],
                                "content": function_response
                            })
                            
                            results.append({
                                'function_name': function_name,
                                'function_response': function_response
                            })
                        except Exception as e:
                            results.append({
                                'function_name': function_name,
                                'error': str(e)
                            })
                    
                    # Get final response after tool usage
                    final_data = {
                        "model": model,
                        "messages": messages,
                        "temperature": 0.7,
                        "max_tokens": 1000,
                        "stream": False
                    }
                    final_response = requests.post(url, headers=headers, json=final_data)
                    final_response_data = final_response.json()
                    
                    if 'choices' in final_response_data:
                        final_message = final_response_data['choices'][0].get('message', {}).get('content', '')
                        return {
                            'tool_results': results,
                            'final_response': final_message,
                            'model': model
                        }
                    
                    return {
                        'tool_results': results,
                        'model': model
                    }
                else:
                    return {
                        'message': message.get('content', '').strip(),
                        'model': model
                    }
            
            return {
                'error': 'Unexpected API response format',
                'raw_response': response_data
            }

        except requests.exceptions.RequestException as e:
            raise e
        except Exception as e:
            raise e

def test_llm_tools():
    llm_handler = LLMHandler()
    
    # Define available tools

    # Test cases with different queries
    test_cases = [
        {
            "prompt": 'What are the biggest threats on the battlefield in Ukraine?',
        },
    ]

    available_tools = [_get_omelas_results, _get_search_results]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest case {i}:")
        print(f"Prompt: {test_case['prompt']}")
        response = llm_handler._get_llm_response(
            prompt=test_case['prompt'],
            functions = functions
        )
        print(f"Final Response: {response.get('final_response', 'No final response available')}")

if __name__ == "__main__":
    test_llm_tools()
