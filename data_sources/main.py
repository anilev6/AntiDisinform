from search_scraper import get_search_and_scrape, print_results

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