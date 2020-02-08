# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XeroItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()
    
    study_uid = scrapy.Field()
    r_mlo = scrapy.Field()
    l_mlo = scrapy.Field()
    r_cc = scrapy.Field()
    l_cc = scrapy.Field()