# app.py (v1)

"""Script to crawl  Posts of digikala
"""

from scrapy.crawler import CrawlerProcess
from digikala.spiders.spi import SpiSpider
from scrapy.utils.project import get_project_settings
import digikala

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())

    process.crawl(SpiSpider)
    process.start() # the script will block here until the crawling is finished