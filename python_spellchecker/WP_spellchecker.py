# -*- coding: utf-8 -*-

from custom_enchant_filters import HtmlEntitiesFilter
from custom_enchant_filters import sprintfParametersFilter
from enchant.checker import SpellChecker
from enchant.tokenize import EmailFilter, URLFilter
from strings_downloader import strings_downloader
import enchant
import os
import pdb
import re


class WP_spell_chekcer():

    def __init__(self, URL=None):
        str_dwl = strings_downloader(URL)

        str_dwl.donwload_strings()
        str_dwl.load_donwloaded_strings()
        str_dwl.delete_file()

        # Dict with all the strings with the following structure
        # [s_original] = s_translated
        #   s_original   is the original string on english
        #   s_translated is the translated string
        self.strings = str_dwl.get_strings()

        # Objetive language to check, the translated one or s_translated
        self.lang_to_check = str(self.strings['html_lang_attribute'])

        # Objetive language avaliable. Venezuelan spanish are not avaliable but
        # spanish is
        # If contains es load the espanish dictionary
        if(re.search('es', self.lang_to_check) is not None):
            self.lang_to_check_avalible = 'es'

        self._load_PWL_dics()
        self._load_spellchecker()

    def _load_PWL_dics(self):
        '''Load all PWL and dics needed'''

        # Spellchecker of english. Some words still used on any lengauge. We
        # need to verify the words on english too. Also is loaded some personal
        # word list to improve the spellchecking
        self.en_PWL = enchant.DictWithPWL('en_US',
                                          pwl=self._path_PWL('en_US')
                                          )

        self.langToCheck_PWL = enchant.request_pwl_dict(
            self._path_PWL(self.lang_to_check_avalible))

    def _load_spellchecker(self):
        '''Init all the speellcheckers needed'''
        self.spellChecker = SpellChecker(self.lang_to_check_avalible,
                                         filters=[EmailFilter,
                                                  URLFilter,
                                                  HtmlEntitiesFilter,
                                                  sprintfParametersFilter])

    def _path_PWL(self, language):
            '''
            Return the path of the custom dictionary stored on
            spellchecker.personal_word_list

            @param  file_name
                    File name of the custom dict
            '''
            path = os.path.join(os.getcwd(),
                                'personal_word_list',
                                language+'_PWL.txt')
            return path

    def initiate_spellchecking(self):
        '''
        Run the spellcheking, print the errors founded
        '''
        for s_original, s_translated in self.strings.items():
            s_translated = s_translated[0]
            self.spellChecker.set_text(s_translated)

            for err in self.spellChecker:
                # Verify if the word is ok on English
                # Several words are on English so they are marked as error
                if (self.en_PWL.check(err.word) is True):
                    continue

                # Verify if the word is ok on lang to check PWL
                if (self.langToCheck_PWL.check(err.word) is True):
                    continue

                # After the filters print
                print(err.word)

if (__name__ == "__main__"):
    WPspckr = WP_spell_chekcer()
    WPspckr.initiate_spellchecking()
