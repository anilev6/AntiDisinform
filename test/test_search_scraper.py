# Run: ```PYTHONPATH=. pytest````
import pytest
from data_sources.search_scraper import get_search_results_serp, scrape_links_firecrawl

@pytest.fixture(scope="module")
def setup_environment():
    from dotenv import load_dotenv
    load_dotenv()

def test_google_search(setup_environment):
    search_engine = "google"
    search_query = "trump prez 2024"
    results = get_search_results_serp(search_engine, search_query)
    assert isinstance(results, list)
    assert len(results) > 0
    assert 'link' in results[0]

def test_baidu_search(setup_environment):
    search_engine = "baidu"
    search_query = "trump prez 2024"
    results = get_search_results_serp(search_engine, search_query)
    assert isinstance(results, list)
    assert len(results) > 0
    assert 'link' in results[0]

def test_yandex_search(setup_environment):
    search_engine = "yandex"
    search_query = "trump prez 2024"
    results = get_search_results_serp(search_engine, search_query)
    assert isinstance(results, list)
    assert len(results) > 0
    assert 'link' in results[0]

def test_scrape_links_firecrawl(setup_environment):
    search_engine = "google"
    search_query = "trump prez 2024"
    search_results = get_search_results_serp(search_engine, search_query)
    scraped_results = scrape_links_firecrawl(search_results)
    assert isinstance(scraped_results, list)
    assert 'scraped_content' in scraped_results[0]
