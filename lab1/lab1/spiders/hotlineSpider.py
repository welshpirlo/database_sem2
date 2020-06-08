from scrapy.http.response import Response
import scrapy


class hotlineSpider(scrapy.Spider):
    name = 'hotline'
    allowed_domains = ['hotline.ua']
    start_urls = ['https://hotline.ua/computer/igrovye-pristavki/']

    def parse(self, response: Response):
        products = response.xpath("//li[contains(@class, 'product-item')]")[:20]

        for product in products:
            yield {
                'title': product.xpath(".//a[contains(@class, 'item-img-link')]/@title")[0].get(),
                'image': product.xpath(".//img[contains(@class, 'img-product ')]/@src")[0].get(),
                'price': product.xpath(".//span[contains(@class, 'value')]/text()")[0].get()

            }