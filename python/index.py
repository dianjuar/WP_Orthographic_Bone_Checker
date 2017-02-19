import scrapy

#--the spiders
from scrapers.scrapers.spiders.getNumberPages import GetnumberpagesSpider
#--the spiders


class test(object):
    """docstring for test"""

    def __init__(self):
        self.pagesToScrap = -1
        pass
        

    def slot_pagesToScrap( self, spider ):
        '''
        @brief  Function to catch the signal of finished spider
        @param  spider 
                The spider that launch the signal
        '''
        self.pagesToScrap = numberOfPages
    
    def getNumberOfPages(self):

        from pydispatch import dispatcher
        from scrapy import signals
        from scrapy.crawler import CrawlerProcess
        from pydispatch import dispatcher
        from scrapy.utils.project import get_project_settings

        spider = GetnumberpagesSpider()


        process = CrawlerProcess( get_project_settings() )

        dispatcher.connect( self.hola, signals.item_passed )

        process.crawl( spider )
        process.start()


testobj = test()
testobj.getNumberOfPages()