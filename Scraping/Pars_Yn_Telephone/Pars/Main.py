import requests
import json
import csv
"""Введите API ключ: 1da3b490-5a42-4024-92dd-3df922215857
Введите запрос: Авто
Введите координаты: 37.624566,55.713384"""


def get_html(url):
    r = requests.get(url)
    return r


def get_content(contents):
    items = []
    for i in range(len(contents['features'])):
        try:
            phone = ''
            for j in range(len(contents['features'][i]['properties']['CompanyMetaData']['Phones'])):
                if j == 0:
                    phone = str(contents['features'][i]['properties']['CompanyMetaData']['Phones'][j]['formatted'])
                else:
                    phone = phone + '\n' + str(contents['features'][i]['properties']['CompanyMetaData']['Phones'][j]['formatted'])
        except:
            phone = 'Номеров нет'
        try:
            items.append({
                'name': contents['features'][i]['properties']['name'],
                'description': contents['features'][i]['properties']['description'],
                'url': contents['features'][i]['properties']['CompanyMetaData']['url'],
                'phone': phone
            })
        except:
            items.append({
                'name': contents['features'][i]['properties']['name'],
                'description': contents['features'][i]['properties']['description'],
                'url': 'Ссылки нет',
                'phone': phone
            })
    for i in items:
        print(i['name'])
        print(i['description'])
        print(i['url'])
        print(i['phone'])
    return items


def save_content(content):
    with open('yandex.csv', 'w', newline='') as f:
        writer = csv.writer(f, delimiter=';')
        writer.writerow(['Название организации', 'Адрес', 'Ссылка на сайт', 'Номера телефонов'])
        for i in content:
            writer.writerow([
                i['name'],
                i['description'],
                i['url'],
                i['phone'].replace('\n', ' ')
            ])
    print('Данные были сохранены в yandex.csv')


def do_start():
    token = input('Введите API ключ: ')
    text = input('Введите запрос: ')
    start = input('Введите центр координат: ')
    end = input('Введите размер области в координатах: ')
    html = get_html(f'https://search-maps.yandex.ru/v1/?apikey={token}&text={text}&ll={start}&spn={end}&lang=ru_RU&results=500')
    if html.ok:
        html = json.loads(html.text)
        content = []
        content.extend(get_content(html))
        save_content(content)
    else:
        print('Ошибка запроса')


if __name__ == '__main__':
    do_start()

