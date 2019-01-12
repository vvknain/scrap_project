# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QuoteItem(scrapy.Item):
	author = scrapy.Field()
	quote = scrapy.Field()


class DirectorItem(scrapy.Item):
	url = scrapy.Field()
	din = scrapy.Field()
	director_name = scrapy.Field()
	designation = scrapy.Field()
	appointment_date = scrapy.Field()
	search_depth = scrapy.Field()


class CrawlSpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
		