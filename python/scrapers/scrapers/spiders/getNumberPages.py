# -*- coding: utf-8 -*-
import scrapy


"""
Spider to get the number of pages needed to scrap
"""
class GetnumberpagesSpider(scrapy.Spider):
    name = "getNumberPages"
    allowed_domains = ["translate.wordpress.org"]
    start_urls = ['https://translate.wordpress.org/projects/wp/dev/es/default']

    def parse(self, response):

        hxs = scrapy.Selector( response )
        pagesToScrap = hxs.xpath('''//div[@class="gp-content"]//
                                        div[@class="paging"]/
                                            *[@class="next"]/
                                            preceding::a[1]/
                                                text()''')

        print("--------------------")
        print( pagesToScrap.extract() )
        print("--------------------")

        pass
