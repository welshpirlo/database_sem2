# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# -*- coding: utf-8 -*-

from lxml import etree


class Lab1Pipeline(object):
    def __init__(self):
        self.root = None

    def open_spider(self, spider):
        self.root = etree.Element("data" if spider.name == "korrespondent" else "shop")

    def close_spider(self, spider):
        with open('task%d.xml' % (1 if spider.name == "korrespondent" else 2), 'wb') as f:
            f.write(etree.tostring(self.root, encoding="UTF-8", pretty_print=True, xml_declaration=True))

    def process_item(self, item, spider):
        if spider.name == "korrespondent":
            page = etree.Element("page", url=item["url"])
            for payload in item["payload"]:
                fragment = etree.Element("fragment", type=payload["type"])
                fragment.text = payload["data"]
                page.append(fragment)
            self.root.append(page)
        else:
            product = etree.Element("product")
            title = etree.Element("title")
            title.text = item["title"]
            img = etree.Element("image")
            img.text = item["image"]
            pr = etree.Element("price")
            pr.text = item["price"]
            product.append(title)
            product.append(img)
            product.append(pr)
            self.root.append(product)
        return item