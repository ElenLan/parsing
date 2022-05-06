import scrapy
from scrapy.http import HtmlResponse
from casparser.items import CasparserItem
from scrapy.loader import ItemLoader

class CastoruSpider(scrapy.Spider):
    name = 'castoru'
    allowed_domains = ['castorama.ru']


    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.start_urls = [f"https://www.castorama.ru/building-materials/lumber-and-wood-panels/wood-panels"]
    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@class='next i-next']/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        links = response.xpath("//a[@class='product-card__name ga-product-card-name']")
        for link in links:
            yield response.follow(link, callback=self.goods_parse)


    def goods_parse(self, response: HtmlResponse):
        loader = ItemLoader(item=CasparserItem(), response=response)
        loader.add_xpath('name', "//h1[@itemprop='name']/text()")
        loader.add_xpath('price', "//span[@class='price']//text()")
        loader.add_xpath('photos', "//div[contains(@class, 'product-media__top')]//@data-src")
        loader.add_value('url', response.url)
        yield loader.load_item()

