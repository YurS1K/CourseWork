import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def parse_match_author(article_url, headers):
    try:
        response = requests.get(article_url, headers=headers)
        response.raise_for_status()
        article_soup = BeautifulSoup(response.text, 'html.parser')


        author_tag = article_soup.find('div', class_="WidgetArticle__authors--RQEI2__name")
        author = author_tag.get_text(strip=True) if author_tag else "Нет автора"
        return author

    except Exception as e:
        print(f"Ошибка при парсинге статьи: {str(e)}")
        return []


def parse_match(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'ru-RU,ru;q=0.9'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        news_container = soup.find('div', class_='node-news-list _MatchTVv4_Components2017_NodeShortListComponent')
        if not news_container:
            return []

        news_items = news_container.find_all('a', class_='node-news-list__item', limit=100)

        parsed_data = []
        for item in news_items:
            title = item["title"]
            link = urljoin(url, item['href'])

            date_tags = item.findAll('li', class_='list__item credits__item')
            date = date_tags[0].get_text()

            tags = [date_tags[1].get_text()]

            author = parse_match_author(link, headers) if link else []


            date = date[0:18]

            parsed_data.append({
                'title': title,
                'link': link,
                'tags': tags,
                'date': date,
                'author': author,
            })

        return parsed_data

    except Exception as e:
        print(f"Ошибка: {str(e)}")
        return []

