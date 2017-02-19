# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


# The scrapy item of used in the spider GetnumberpagesSpider
class item_numberOfPages(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # Number of pages to scrap
    numberOfPages = scrapy.Field()
    pass


class item_stringToAnalize(scrapy.Item):
    '''
    @brief scrapy item to store the strings scraped
    '''

    # The param itself
    string = scrapy.Field()

    # The url where the string is located
    url = scrapy.Field()

    # define the fields for your item here like:
    # name = scrapy.Field()
