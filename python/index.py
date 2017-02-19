import scrapy


#--run a crawler in a script stuff
from pydispatch             import dispatcher
from scrapy                 import signals
from scrapy.crawler         import CrawlerProcess
from pydispatch             import dispatcher
from scrapy.utils.project   import get_project_settings
#--run a crawler in a script stuff


#--the spiders
from scrapers.scrapers.spiders.getNumberPages   import GetnumberpagesSpider
from scrapers.scrapers.spiders.getStrings       import GetstringsSpider
#--the spiders

def run_a_spider_on_script(spider, signal=signals.item_passed, slot=None): 
    '''
    @brief  A function given a spider run it. If a signal an a slot is given connect it

    @param  spider
            The spider itself
    
    @param  signal
            scrapy signal ( defualt item passed  )
    
    @param  slot
            Function to launch after the signal is triggered
    '''
    # The spider
    spiderObj = spider()

    # The process to execute the spider
    process = CrawlerProcess( get_project_settings() )

    # if the slot is not None...
    if (slot is not None):
        # Connect the signal with the slot
        # When the signal triggers execute the slot
        dispatcher.connect( slot, signal )

    # Set in the process the spider
    process.crawl( spider )
    process.start()

class main(object):
    """
    Main class to storage all the scripts
    """

    def __init__(self):
        self.pagesToScrap = -1

        # a Slot is connected with the signal of finished of the spider 'GetnumberpagesSpider'
        # when the number is gotten the method to get the strings is launch
        self.get_NumberOfPages()
    
    def slot_pagesToScrap( self, spider ):
        '''
        @brief  Function to catch the signal of finished spider
        @param  spider 
                The spider that launch the signal
        '''
        self.pagesToScrap = spider.numberOfPages

        # Now is time to get the strings
        self.get_strings()

    def get_strings(self):
        '''
        @brief method to call after the number of pages are got.
        This method will execute the spider to get the strings to analyze
        '''
        run_a_spider_on_script( spider = GetstringsSpider )
    
    def get_NumberOfPages(self):

        run_a_spider_on_script( spider = GetnumberpagesSpider,
                                slot   = self.slot_pagesToScrap)

main_obj = main()
main_obj.initate()