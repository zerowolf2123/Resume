import requests
import json

URL = 'https://steampay.com/api/search'

# Нужно чтобы сайт думал что мы реальные пользователи
HEADERS = {
    "accept": 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
}


def get_html(url, params=''):
    html = requests.get(url,
                        params=params,
                        headers=HEADERS)
    return html


def get_content(html):
    games = []
    for values in html:
        if values['is_available']:
            games.append(
                {
                    'title': values['title'],
                    'url': values['url'],
                    'image': values['image'],
                    'prices': str(values['prices']['rub']) + ' руб'
                }
            )
    return games


def start(params, title: bool, price: bool = False, url: bool = False, image: bool = False):
    html = get_html(URL, params={'query': f'{params}'})
    html = json.loads(html.text)
    if html['error'] == 0:
        games = get_content(html['products'])
        contents = []
        titles, prices, urls, images = [], [], [], []
        if title:
            for values in games:
                titles.append(values['title'])
            if len(titles) > 0:
                contents.append(titles)
        if url:
            for values in games:
                urls.append(values['url'])
            if len(titles) > 0:
                contents.append(urls)
        if image:
            for values in games:
                images.append(values['image'])
            if len(titles) > 0:
                contents.append(images)
        if price:
            for values in games:
                prices.append(values['prices'])
            if len(titles) > 0:
                contents.append(prices)
        if len(contents) > 0:
            return contents
        else:
            from Pars_Bot_Tg.Parcer import start
            return start(params,
                         catalog=True,
                         price=True,
                         link=True,
                         link_image=True
                         )
    else:
        print('Ошибка запроса')


if __name__ == '__main__':
    start(params='Super',
          title=True)