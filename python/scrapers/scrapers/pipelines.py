# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import enchant
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
from spellchecker.custom_enchant_filters import sprintfParametersFilter
# - Debugger
import pdb
import os


class ScrapersPipeline(object):
    def process_item(self, item, spider):
        return item


class checkStringPipeline(object):
    # Path to the Personal Word List that contains the WP words, like
    # CSS, PHP, WordPress
    enUSWP_PWL_path = ''

    # Path to the Personal Word List that contains the spanish words, like
    # Abr, Ago...
    es_PWL_path = ''

    def __init__(self):
        '''
        To accomplish
        https://github.com/dianjuar/WP_Orthographic_Bone_Checker/issues/2

        Several strings are "false positives", like URL, plugin, WordPress, IDs,
        facebook, youtube.

        A personal word list will be used to do it.
        '''

        # List with spelling erros
        self.wrongWords = list()

        # Path of the PWL of WP. Contains words like CSS, PHP, fopen ...
        self.enUSWP_PWL = self.path_PWL('enUSWP_PWL.txt')
        self.es_PWL_path = self.path_PWL('es_PWL.txt')

        # Spellchecker of english. Some words still used on any lengauge. We
        # need to verify the words on english too.
        self.dict_en_WP_PWL = enchant.DictWithPWL('en_US',
                                                  pwl=self.enUSWP_PWL)

    @classmethod
    def from_crawler(cls, crawler):
        pipeline = cls()
        crawler.signals.connect(pipeline.spider_opened, signals.spider_opened)
        crawler.signals.connect(pipeline.spider_closed, signals.spider_closed)
        return pipeline

    def spider_opened(self, spider):
        pass

    def spider_closed(self, spider):
        print("Errors detected ----------------------------- ")
        print(self.wrongWords)
        print("Errors detected ----------------------------- ")
        # pdb.set_trace()
        pass

    def process_item(self, item, spider):
        '''
        Using enchant to do spell checking
        '''
        # Number of pages
        if(type(item) is item_numberOfPages):
            self.process_item_numberOfPages(item, spider)
            raise DropItem("Number of Pages to scrap %s" % item)

        # strings
        elif(type(item) is item_stringToAnalize):
            detectErrors = self.detectErrors(item['string'])

            if(detectErrors is False):
                raise DropItem("No error detected on %s" % item)
                return

            # If there is erros return the detected ones
            item['errors'] = detectErrors
            return item

    def process_item_numberOfPages(self, item, spider):
        pass

    def detectErrors(self, string):
        '''
        @brief get all errors given a string
        @return False
                Doesn't have errors.

                Dict()
                Dict With the errors
        '''

        spellChecker = SpellChecker('es', filters=[EmailFilter,
                                                   URLFilter,
                                                   HtmlEntitiesFilter,
                                                   sprintfParametersFilter])
        spellChecker.set_text(string)

        PWL_es = enchant.request_pwl_dict(self.es_PWL_path)

        errors = False

        for err in spellChecker:
            # Verify if the word is ok on English
            # Several words are on English so they are marked as error
            if (self.dict_en_WP_PWL.check(err.word) is True):
                continue

            # Verify if the word is ok on Es PWL
            if (PWL_es.check(err.word) is True):
                continue
            # convert only once errors to a dictionary
            if type(errors) is not dict():
                errors = {}
                errors['errorWord'] = list()

            errors['errorWord'].append(err.word)

            # Add the bad word to the list
            self.addNewBadWord(err.word)

        # value_is_true if condition else value_is_false
        # "fat" if is_fat else "not fat"
        return errors

    def addNewBadWord(self, string):
        '''
        store in self.wrongWords the string given via parameter.errors
        A simple verify process applied, just not to be a repeated word
        '''
        if string not in self.wrongWords:
            self.wrongWords.append(string)

        pass

    def path_PWL(self, file_name):
        '''
        Return the path of the custom dictionary stored on
        spellchecker.personal_word_list

        @param  file_name
                File name of the custom dict
        '''
        return os.path.join(os.getcwd(),
                            '..',
                            'spellchecker',
                            'personal_word_list',
                            file_name)
