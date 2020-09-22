import requests
from bs4 import BeautifulSoup
import csv
from Scrap_Settings.Settings import HOST, HEADERS, CSV, URL, CITY, SECTION


def get_html(url, params=''):
    r = requests.get(url,
                     headers=HEADERS,
                     params=params,)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    contents = soup.find_all('div', class_='snippet')
    items = []
    for i in range(len(contents)):
        items.append({
            'Product Name': contents[i].find('span', class_='snippet-link-name').get_text(strip=True),
            'url': HOST + contents[i].find('a', class_='snippet-link').get('href'),
            'price': ' '.join(contents[i].find('div', class_='snippet-price-row').get_text(strip=True).split()[:-1]),
            'street': contents[i].find('span', class_='item-address__string').get_text(strip=True)
        })
    return items


def do_save_doc(items):
    with open(CSV, 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['Название товара', 'Ссылка на продукт', 'Цена', 'Адресс'])
        for i in items:
            writer.writerow([
                i['Product Name'],
                i['url'],
                i['price'],
                i['street']
            ])


def do_start():
    print('''Вы запустили скрипт. Введите ваш город для начала или введите \'все\', 
чтобы выбрать все товары по России''')
    bool_, host, items = False, URL, []
    city = input().lower()
    if city != 'все':
        for key, values in CITY.items():
            if city == key:
                city = values
                bool_ = True
        if bool_:
            host = HOST + '/' + city
        else:
            print('Такого города не обнаружено в базе данных')
    else:
        bool_ = True
    if bool_:
        section = input('Введите раздел: ')
        if section:
            bool_ = False
            for key, values in SECTION.items():
                if section == key:
                    host = host + '/' + values
                    bool_ = True
            if bool_:
                page = input('Введите количество страниц: ')
                try:
                    page = int(page)
                    if page > 0:
                        html = get_html(url=host)
                        if html.ok:
                            for i in range(1, page+1):
                                print(f'стканица №{i}')
                                html = get_html(url=host, params={'p': i})
                                items.extend(get_content(html=html.text))
                            do_save_doc(items)
                        else:
                            print('Ошибка запроса')
                    else:
                        print('Такой страницы нет')
                except:
                    print('Введите число')
            else:
                print('Такого раздела нет в базе данных')
        else:
            print('Введите раздел')


if __name__ == '__main__':
    do_start()
