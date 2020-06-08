from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lxml import etree
import os
import webbrowser


def cleanup():
    try:
        os.remove("task1.xml")
        os.remove("task2.xml")
        os.remove("task2.xhtml")
    except OSError:
        pass


def scrap_data():
    process = CrawlerProcess(get_project_settings())
    process.crawl('korrespondent')
    process.crawl('hotline')
    process.start()


def task1():
    root = etree.parse("task1.xml")
    pages = root.xpath("//page")

    for page in pages:
        text_fragments = page.xpath("count(fragment[@type='text'])")
        print("Text fragments in document = %d" % text_fragments)


def task2():
    transform = etree.XSLT(etree.parse("task2.xsl"))
    result = transform(etree.parse("task2.xml"))
    result.write("task2.xhtml", pretty_print=True, encoding="UTF-8")
    webbrowser.open('file://' + os.path.realpath("task2.xhtml"))


if __name__ == '__main__':
    cleanup()
    scrap_data()
    while True:
        print("-" * 50)
        print("Select task:")
        print("1. Number of text fragments")
        print("2. xhtml document")
        print(">> ", end="", flush=True)
        task_num = input()
        if task_num == "1":
            task1()
        elif task_num == "2":
            task2()
        else:
            break