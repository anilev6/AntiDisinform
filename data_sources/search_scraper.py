#%%
import os
import time

from serpapi import GoogleSearch, BaiduSearch, YandexSearch
from firecrawl.firecrawl import FirecrawlApp
from dotenv import load_dotenv
from pprint import pprint

# Load environment variables from .env file
load_dotenv()

def get_search_results_serp(search_engine, search_query):
    """
    Fetches organic search results from the specified search engine using SerpAPI.

    Parameters:
    - search_engine (str): 'google', 'baidu', or 'yandex'
    - search_query (str): The search query string.

    Returns:
    - List[dict]: List of organic search results.
    """
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise EnvironmentError("SERPAPI_API_KEY not found in environment variables.")

    params = {"api_key": api_key}

    search_engine = search_engine.lower()
    if search_engine == 'google':
        params["q"] = search_query
        params['location'] = 'Ukraine'
        params['google_domain'] = 'google.com.ua'
        search = GoogleSearch(params)
    elif search_engine == 'baidu':
        params["q"] = search_query
        search = BaiduSearch(params)
    elif search_engine == 'yandex':
        params["text"] = search_query
        params['lr'] = 1
        params['yandex_domain'] = 'yandex.ru'
        params['lang'] = 'ru'
        search = YandexSearch(params)
    else:
        raise ValueError("Unsupported search engine. Choose from 'google', 'baidu', or 'yandex'.")

    try:
        results = search.get_dict()
    except Exception as e:
        raise Exception(f"Failed to fetch search results: {e}")

    if "error" in results:
        raise Exception(f"Error from SerpAPI: {results['error']}")
    
    # return results

    organic_results = results.get('organic_results', [])
    if not organic_results:
        print("No organic results found.")

    fields_to_keep = ["link", "position", "snippet", "title", "source", "date"]
    filtered_results = []
    for result in organic_results:
        filtered_result = {field: result.get(field, None) for field in fields_to_keep}
        filtered_results.append(filtered_result)

    return filtered_results

def scrape_links_firecrawl(search_results):
    """
    Scrapes the content of each URL in the search results using Firecrawl.

    Parameters:
    - search_results (list): List of search result dictionaries containing 'link'.

    Returns:
    - list: Updated list with 'scraped_content' added to each result.
    """
    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        raise EnvironmentError("FIRECRAWL_API_KEY not found in environment variables.")

    app = FirecrawlApp(api_key=api_key)

    for result in search_results:
        url = result.get("link")
        if not url:
            continue  # Skip if no URL is present
        try:
            scrape_result = app.scrape_url(url, params={'formats': ['markdown']})
            result["scraped_content"] = scrape_result.get("markdown", "No content found")
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            result["scraped_content"] = "Error during scraping"

        # Optional: Add a delay to prevent rate-limiting
        time.sleep(1)

    return search_results

def get_search_and_scrape(search_engine, search_query):
    """
    Combines fetching search results and scraping their content.

    Parameters:
    - search_engine (str): 'google', 'baidu', or 'yandex'
    - search_query (str): The search query string.

    Returns:
    - list: List of search results with scraped content.
    """
    search_results = get_search_results_serp(search_engine, search_query)
    scraped_results = scrape_links_firecrawl(search_results)
    return scraped_results

def print_results(results):
    """
    Pretty prints the search results.

    Parameters:
    - results (list): List of search result dictionaries.
    """
    for result in results:
        pprint(result)
        print("\n" + "-"*80 + "\n")

#%%

def main():
    search_engine = "google"  # Options: 'google', 'baidu', 'yandex'
    search_query = "trump prez 2024"

    try:
        results = get_search_and_scrape(search_engine, search_query)
        print_results(results)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

# %%
