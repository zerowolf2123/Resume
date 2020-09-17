import requests
from bs4 import BeautifulSoup
import csv


CSV = 'cards.csv'
# Сайт который мы будем парсить
HOST = 'https://minfin.com.ua/'
# Страница которую мы будем парсить
URL = 'https://minfin.com.ua/cards/'
HEADERS = {
    "accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
}


def get_html(url, params=''):
    r = requests.get(url,
                     headers=HEADERS,
                     params=params,)
    return r


def get_content(html):
    # Объявляем парсер
    soup = BeautifulSoup(html, 'html.parser')
    # Парсим заданный контент
    contents = soup.find_all('div', class_='product-item')
    cards = []
    for i in range(1, 11):
        cards.append(
            {
                # Берем название карты strip - Убирает все пробелы и '\n'
                'title': contents[i].find('div', class_='title').get_text(strip=True),
                # Ищем внутри div ссылку и берем с помощью get('href') саму ссылку
                'link_prod': HOST + contents[i].find('div', class_='title').find('a').get('href'),
                'brand': contents[i].find('div', class_='brand').get_text(strip=True),
                # HOST + ... - создание ссылки
                'image': HOST + contents[i].find('div', class_='image').find('img').get('src')
            }
        )
    return cards


def save_doc(cards, file):
    with open(file, 'w', newline='') as f:
        # Создает csv файл delimiter - это разделитель
        writer = csv.writer(f, delimiter=';')
        # создаем таблицу
        writer.writerow(['Название карты', 'Ссылка на продукт', 'Название компании', 'Фото продукта'])
        for i in cards:
            print(i)
            writer.writerow([
                i['title'],
                i['link_prod'],
                i['brand'],
                i['image']
            ])


def start(pagenation=1):
    html = get_html(URL)
    if html.ok:
        cards = []
        for i in range(pagenation):
            html = get_html(URL, params={'page': i})
            cards.extend(get_content(html.text))
            save_doc(cards, CSV)
        # return cards
    else:
        print('Ошибка в запросе сайта')


if __name__ == '__main__':
    start(3)
