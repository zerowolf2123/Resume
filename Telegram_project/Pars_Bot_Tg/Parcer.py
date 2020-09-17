import requests
from bs4 import BeautifulSoup
import csv

# https://steampay.com/search?q=Boy+
HOST = 'https://steampay.com/'
URL = 'https://steampay.com/search'
HEADERS = {
    "accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
}
PROXY = {
    "http": 'localhost:8080',
    "https": 'localhost:8080'
}


def get_html(url, params=''):
    r = requests.get(url,
                     headers=HEADERS,
                     params=params,
                     # proxies=PROXY,
                     # verify=False
    )
    return r


def get_content(html):
    # Создаем экземпляр класса BeautifulSoup, чтобы работать с полученными данными
    soup = BeautifulSoup(html, 'html.parser')
    # Из всего кода мы находим все куски кода, class которого является catalog
    # 'a' - это <a class='catalog-item'>...</a>
    contents = soup.find_all('a', class_='catalog-item')
    games = []
    for value in contents:
        # print(value)
        games.append(
            # Обязательно добавляем значения в виде словаря
            {
                # Берем имя игры и убираем все пробелы и '\n'
                # .contents[0] - берем первый найденный элемент
                'catalog-item': value.find('div', class_='catalog-item__name').contents[0].strip(),
                # Берем ссылку и добавляем ее к главной страницу
                'link': HOST + value.get('href') + '?agent=4813c53d-ce39-49ab-9fd0-22cfff05de50',
                # Ищем ссылку на изображение внутри class_='catalog-item__img'
                'link_image': HOST + value.find('div', class_='catalog-item__img').find('img').get('src'),
                # Глубина вложенности не ограничена
                'price': value.find('div', class_='catalog-item__price').find('span', class_='catalog-item__price-span').get_text(strip=True)
            }
        )
    return games


def start(params, catalog: bool, price=False, link=False, link_image=False):
    # Делаем GET запрос
    html = get_html(URL, params={'q': f'{params}'})
    # .ok - проверяет запрос на валидность
    if html.ok:
        # html.text - Передаем только текст запроса, без лишней информации
        games = get_content(html.text)
        catalogs, links, link_images, prices = [], [], [], []
        contents = []
        if catalog:
            for value in games:
                if value['price'] != 'СКОРО' and value['price'] != '—':
                    catalogs.append(value['catalog-item'])
            if len(catalogs) > 0:
                contents.append(catalogs)
        if link:
            for value in games:
                if value['price'] != 'СКОРО' and value['price'] != '—':
                    links.append(value['link'])
            if len(links) > 0:
                contents.append(links)
        if link_image:
            for value in games:
                if value['price'] != 'СКОРО' and value['price'] != '—':
                    link_images.append(value['link_image'])
            if len(link_images) > 0:
                contents.append(link_images)
        if price:
            for value in games:
                if value['price'] != 'СКОРО' and value['price'] != '—':
                    prices.append(value['price'])
            if len(prices) > 0:
                contents.append(prices)
        if len(contents) > 0:
            return contents
        else:
            return 'Ничего не найдено'
    else:
        print('Ошибка в запросе')


if __name__ == '__main__':
    start('PUBG', True, price=True)
