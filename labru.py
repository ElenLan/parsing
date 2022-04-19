# 1) Создать паукa по сбору данных о книгах с сайтов labirint.ru
# 2) Каждый паук должен собирать:
# * Ссылку на книгу
# * Наименование книги
# * Автор(ы)
# * Основную цену
# * Цену со скидкой
# * Рейтинг книги
# 3) Собранная информация должна складываться в базу данных



import scrapy
from scrapy.http import HtmlResponse
from labirintpars.items import LabirintparsItem

class LabruSpider(scrapy.Spider):
    name = 'labru'
    allowed_domains = ['labirint.ru']
    start_urls = [
        'https://www.labirint.ru/search/%D1%84%D0%B0%D0%BD%D1%82%D0%B0%D1%81%D1%82%D0%B8%D0%BA%D0%B0/?stype=0']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//div[@class='pagination-next']//@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@class='product-title-link']/@href").getall()
        for link in links:
            yield response.follow(link, callback=self.books_parse)

    def books_parse(self, response: HtmlResponse):
        url = response.url
        name = response.xpath("//div[@id='product-title']/h1/text()").get()
        author = response.xpath("//a[@data-event-label='author']//text()").get()
        priceold = response.xpath("//div[@class='buying-priceold-val']/span/text()").get()
        pricenew = response.xpath("//div[@class='buying-pricenew-val']//span/text()").get()
        rating = response.xpath("//div[@id='rate']/text()").get()
        yield LabirintparsItem(url=url, name=name, author=author, priceold=priceold, pricenew=pricenew,
                               rating=rating)
