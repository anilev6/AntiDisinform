#%%
from search_scraper import get_search_and_scrape, print_results

def main(search_engine: str, search_query: str):
    try:
        results = get_search_and_scrape(search_engine, search_query)
        print_results(results)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main(search_engine = "baidu", search_query = "美中国际关系")
# %%

# GOOGLE

#  {'link': 'https://en.wikipedia.org/wiki/2024_United_States_presidential_election',
#   'position': 6,
#   'snippet': "The 2024 United States presidential election was the 60th quadrennial presidential election, held on Tuesday, November 5, 2024. The Republican Party's ...",
#   'title': '2024 United States presidential election',
#   'source': 'Wikipedia',
#   'date': None},

# YANDEX

# {'link': 'https://novayagazeta.ru/articles/2023/08/21/bitva-na-istoshchenie',
#   'position': 5,
#   'snippet': 'По мере затягивания военной операции России в Украине, с переходом СВО в состояние, которое в Европе называют войной на истощение...',
#   'title': 'Конец СВО обсуждают всем миром. Обзор публичных...',
#   'source': None,
#   'date': None}

# BAIDU

#  {'link': 'https://m.thepaper.cn/newsDetail_forward_28728643',
#   'position': 9,
#   'snippet': '中美找到正确相处之道,是今后50年国际关系中最重要的事情,也是两国人民和国际社会最大的期待。互尊互信是中美对话的基础,从来没有谁高谁一等;互利互惠是中美合作的本质,从来没有谁...',
#   'title': '驻美大使谢锋:互商互谅是中美共处逻辑,从来没有谁能压垮谁',
#   'source': None,
#   'date': '2024年9月13日'},