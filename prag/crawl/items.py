# Define here the models for your scraped items
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
import scrapy


class HideMyAssItem(scrapy.Item):
    source = scrapy.Field()
    scraped_at = scrapy.Field()
    updated_at = scrapy.Field()
    country = scrapy.Field()
    ip_addr = scrapy.Field()
    port = scrapy.Field()
    proto = scrapy.Field()
    anonimity = scrapy.Field()
    speed_qual = scrapy.Field()
    connect_qual = scrapy.Field()
