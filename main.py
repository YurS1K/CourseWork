from Parsers.ria_sport_parser import parse_ria_sport
from Parsers.championat_parser import parse_champion
from Parsers.match_parser import parse_match
import pandas as pd

if __name__ == "__main__":
    ria_urls = ["https://rsport.ria.ru/hockey/", "https://rsport.ria.ru/football/",
                "https://rsport.ria.ru/figure_skating/", "https://rsport.ria.ru/tennis/", "https://rsport.ria.ru/fights/", "https://rsport.ria.ru/lyzhnye-gonki/",
                "https://rsport.ria.ru/biathlon/", "https://rsport.ria.ru/category_formula_1/"]
    champion_url = "https://www.championat.com/news/1.html"
    match_url = "https://matchtv.ru/news"

    data = []
    for url in ria_urls:
        for i in parse_ria_sport(url):
            data.append(i)

    for i in parse_champion(champion_url):
        data.append(i)

    for i in parse_match(match_url):
        data.append(i)

    parsed = pd.DataFrame(data)
    parsed.to_csv('parsed_data.csv')

    for idx, item in enumerate(data, 1):
        print(f"{idx}. {item['title']}")
        print(f"   Ссылка: {item['link']}")
        print(f"   Теги: {', '.join(item['tags']) if item['tags'] else 'Нет тегов'}")
        print(f"   Дата: {item['date'] if item['date'] else 'Нет даты'}")
        print(f"   Автор: {item['author']}")
        print("-" * 80)