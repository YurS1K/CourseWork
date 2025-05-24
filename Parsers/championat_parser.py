import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def parse_champion_tags(article_url, headers):
    try:
        response = requests.get(article_url, headers=headers)
        response.raise_for_status()
        article_soup = BeautifulSoup(response.text, 'html.parser')

        tags_container = article_soup.find('div', class_='tags__items js-tags-items')
        if tags_container:
            tags = [tag.get_text(strip=True) for tag in tags_container.find_all('a')]
        else:
            tags = []
        date = article_soup.find('time', class_="article-head__date").get_text(strip=True)
        author_tag = article_soup.find('div', class_="article-head__author-name")
        author = author_tag.get_text(strip=True) if author_tag else "Нет автора"
        return tags[1:], date, author

    except Exception as e:
        print(f"Ошибка при парсинге статьи: {str(e)}")
        return []


def parse_champion(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'ru-RU,ru;q=0.9'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        news_container = soup.find('div', class_='news-items')
        if not news_container:
            return []

        news_items = news_container.find_all('div', class_='news-item', limit=25)
        parsed_data = []

        for item in news_items:
            title_tag = item.find('a', class_='news-item__title')
            title = title_tag.get_text(strip=True) if title_tag else 'Без заголовка'
            link = urljoin(url, title_tag['href']) if title_tag else ''
            tags, date, author = parse_champion_tags(link, headers) if link else []
            tags = list(set(filter(None, tags)))

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
