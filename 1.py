# Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru,
# yandex-новости. Для парсинга использовать XPath. Структура данных должна содержать:
# название источника;
# наименование новости;
# ссылку на новость;
# дата публикации.
# Сложить собранные новости в БД

from lxml import html
import requests
from pprint import pprint
from fake_headers import Headers
from datetime import date
import json

url = 'https://lenta.ru/'

# header = Headers(headers=True).generate()
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/100.0.4896.75 Safari/537.36'}
response = requests.get(url, headers=header)
dom = html.fromstring(response.text)
topnews = dom.xpath(".//div[contains(@class,'topnews')]/div//a")
news = []
for top in topnews:
    news_dict = {}
    names = top.xpath("//div[@class='topnews']//h3/text()|//div[@class='topnews']//span/text()")
    link = top.xpath("//div[contains(@class, 'topnews__column')]//a/@href")
    link_new = []
    for i in link:
        link_new.append('https://lenta.ru' + i)
    times = top.xpath("//div[contains(@class, 'topnews')]//time/text()")
    date_news = date.today().isoformat()
    time = []
    for t in times:
        time.append(t + ' ' + date_news)
    news_dict['name'] = names
    news_dict['link'] = link_new
    news_dict['time'] = time
    news_dict['source'] = url
    news.append(news_dict)
pprint(news)

with open('news.json', 'w', encoding='UTF-8') as f:
    json.dump(news, f)
# еще не начинала работу с Mongo, поэтому сохранила в json
