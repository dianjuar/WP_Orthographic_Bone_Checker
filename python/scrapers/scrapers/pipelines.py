# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
from enchant.checker import SpellChecker 
import pdb

#- Items
from scrapers.items import item_numberOfPages
from scrapers.items import item_stringToAnalize
#- Items


class ScrapersPipeline(object):
    def process_item(self, item, spider):
        return item

class checkStringPipeline(object):

    def __init__(self):
        pass

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        pass

    def spider_closed(self, spider):
        pass

    def process_item(self, item, spider):
        '''
        Using enchant to do spell checking
        '''
        # Number of pages
        if( type( item ) is item_numberOfPages ):
            self.process_item_numberOfPages( item, spider )
        # strings
        elif( type( item ) is item_stringToAnalize ):
            validItem = self.process_item_stringToAnalize( item, spider )

            if( validItem ):
                return item

        # return item

    def process_item_numberOfPages(self, item, spider):
        pass

    def process_item_stringToAnalize(self, item, spider):
        '''
        @brief process the item stringToAnalize

        @return True 
                    if the item has errors
                False
                    if the item has no errors, so needs to be rejected    
        '''
        s = SpellChecker('en_US')
        s.set_text( item['string'] )

        return self.has_errors( s )
    
    def has_errors(self, spellChecker ):
        '''
        @brief Verify if the spellchekr object has spelling errors
        '''
        hasIt = False

        for err in spellChecker:
            hasIt = True
            break;

        return hasIt
