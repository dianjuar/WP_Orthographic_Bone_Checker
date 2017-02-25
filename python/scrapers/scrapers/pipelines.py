# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# - PyEnchat SpellChecker
from enchant.checker import SpellChecker
# - enchant filters
from enchant.tokenize import EmailFilter, URLFilter
# - Items
from scrapers.items import item_numberOfPages
from scrapers.items import item_stringToAnalize
# - Scrapy stuff
from scrapy import signals
from scrapy.exceptions import DropItem
# - Custom enchant filters
from spellchecker.custom_enchant_filters import HtmlEntitiesFilter
# - Debugger
import pdb

class ScrapersPipeline(object):
    def process_item(self, item, spider):
        return item

class checkStringPipeline(object):

    def __init__(self):

        '''
        To accomplish https://github.com/dianjuar/WP_Orthographic_Bone_Checker/issues/2

        Several strings are "false positives", like URL, plugin, WordPress, IDs, facebook, youtube.

        A custom database will be created by hand. The wrong words will be stored in this list and selected by hand.
        '''
        self.wrongWords = list()
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
        print( "Errors detected ----------------------------- ")
        print(self.wrongWords)
        print( "Errors detected ----------------------------- ")
        # pdb.set_trace()
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

            if( detectErrors is False):
                raise DropItem("No error detected on %s" % item)
                return

            # If there is erros return the detected ones
            item['errors'] = detectErrors
            return item

    def process_item_numberOfPages(self, item, spider):
        pass


    def detectErrors(self, string ):
        '''
        @brief get all errors given a string
        @return False
                Doesn't have errors.

                Dict()
                Dict With the errors
        '''
        spellChecker = SpellChecker('es', filters=[EmailFilter,URLFilter,HtmlEntitiesFilter])
        spellChecker_en = SpellChecker('en_US' )

        spellChecker.set_text( string )

        errors = False

        for err in spellChecker:

            # Verify if the word is ok on English
            # Several words are on English so they are marked as error
            if ( spellChecker_en.check( err.word ) is True ):
                continue

            # convert only once errors to a dictionary
            if type(errors) is not dict() :
                errors = {}
                errors['errorWord'] = list()

            errors['errorWord'].append( err.word )

            # Add the bad word to the list
            self.addNewBadWord( err.word )

        # value_is_true if condition else value_is_false
        # "fat" if is_fat else "not fat"
        return errors

    def addNewBadWord(self, string):
        '''
        store in self.wrongWords the string given via parameter.errors
        A simple verify process applied, just not to be a repeated word
        '''
        if string not in self.wrongWords:
            self.wrongWords.append( string )

        pass
