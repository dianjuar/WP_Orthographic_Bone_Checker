# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import signals
from enchant.checker import SpellChecker 
from scrapy.exceptions import DropItem
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
            raise DropItem("Number of Pages to scrap %s" % item)

        # strings
        elif( type( item ) is item_stringToAnalize ):
            detectErrors = self.detectErrors( item['string'] )

            if( detectErrors is not False):
                item['errors'] = detectErrors
                return item
            else:
                raise DropItem("No error detected on %s" % item)

        # return item

    def process_item_numberOfPages(self, item, spider):
        pass

    def detectErrors(self, string ):
        '''
        @brief get all errors given a string
        @return False
                Doesn't have errors.

                Dict
                With the erros
        '''
        spellChecker = SpellChecker('es')
        spellChecker.set_text( string )

        errors = False

        for err in spellChecker:
            # convert only once errors to a dictionery
            if type(errors) is not dict() :
                errors = {}
                errors['errorWord'] = list()
            
            errors['errorWord'].append( err.word )

        if ( errors is type(dict()) ):
            print( errors )
            pdb.set_trace()

        # value_is_true if condition else value_is_false
        # "fat" if is_fat else "not fat"
        return errors
