from typing import Dict
from data.omelas.worker import get_omelas_results
from data_sources.search_scraper import get_search_and_scrape

def tool_executor(function_name: str, function_args: Dict) -> str:
    if function_name == 'get_omelas_results':
        query = function_args.get('query')
        print("Calling Omelas function")
        return str(get_omelas_results(query))
    if function_name == 'get_search_and_scrape':
        search_query = function_args.get('search_query')
        search_engine = function_args.get('search_engine')
        print(f"Calling {search_engine} with query: {search_query}")
        return str(get_search_and_scrape(search_engine=search_engine, search_query=search_query))
    raise ValueError(f"Unknown function: {function_name}, avaliable functions are: {', '.join([f['name'] for f in functions])}")


functions = [
    {
        "name": "get_omelas_results",
        "description": "Retrieve data from Database",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The question to ask of the data"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "get_search_and_scrape",
        "description": "Retrieve data from Database",
        "input_schema": {
            "type": "object",
            "properties": {
                "search_query": {
                    "type": "string",
                    "description": "The question to ask of the data"
                },
                "search_engine": {
                    "type": "string",
                    "description": "The search engine to use--Yandex for Russian and Google for Ukrainian"
                }
            },
            "required": ["search_query", "search_engine"]
        }
    },
]