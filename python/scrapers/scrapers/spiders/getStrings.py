# -*- coding: utf-8 -*-
import scrapy
import pdb


class GetstringsSpider(scrapy.Spider):
    name = "getStrings"
    allowed_domains = ["translate.wordpress.org"]
    start_urls = []

    debug = True

    def __init__(self, WPTpage=None, *args, **kwargs):
        '''
        @brief the constructor of the spider

        @param  WPTpage 
                the page stract the strings
        @param args
        @param kwargs

        @ref http://stackoverflow.com/questions/15611605/how-to-pass-a-user-defined-argument-in-scrapy-spider
        '''
        # Constructor
        super(GetstringsSpider, self).__init__(*args, **kwargs)

        # load the start_urls received via parameter, if not passed, the url of the WP development project in spanish is set
        if ( WPTpage == None ):
            self.start_urls = ['https://translate.wordpress.org/projects/wp/dev/es/default']
        else:
            self.start_urls = [WPTpage]
        


    # def start_requests(self):
    #     pass        
    
    def parse(self, response):

        if( self.debug ):
            from scrapy.utils.response import open_in_browser
            open_in_browser(response)
