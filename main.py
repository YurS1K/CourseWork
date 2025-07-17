from Parsers.ria_sport_parser import parse_ria_sport
from Parsers.championat_parser import parse_championat
from Parsers.match_parser import parse_match
import pandas as pd

ria_urls = ["https://rsport.ria.ru/hockey/", "https://rsport.ria.ru/football/",
            "https://rsport.ria.ru/figure_skating/", "https://rsport.ria.ru/tennis/",
            "https://rsport.ria.ru/fights/", "https://rsport.ria.ru/lyzhnye-gonki/",
            "https://rsport.ria.ru/biathlon/", "https://rsport.ria.ru/category_formula_1/"]
champion_url = "https://www.championat.com/news/1.html"
match_url = "https://matchtv.ru/news"

data = []

for url in ria_urls:
    for i in parse_ria_sport(url):
        data.append(i)

for i in parse_championat(champion_url):
    data.append(i)

for i in parse_match(match_url):
    data.append(i)

parsed = pd.DataFrame(data)
parsed.to_csv('parsed_data.csv')
