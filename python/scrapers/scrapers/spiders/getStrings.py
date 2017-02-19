# -*- coding: utf-8 -*-
import scrapy
import pdb

# Import the item right. For test purposes this spider will call in several ways
# Using this try I catch all possibilities   
try:
    from scrapers.scrapers.items import item_stringToAnalize
except ImportError:
    from scrapers.items import item_stringToAnalize


class GetstringsSpider(scrapy.Spider):
    name = "getStrings"
    allowed_domains = ["translate.wordpress.org"]
    start_urls = []

    debug = True

    def __init__(self, WPTpage=None, nPages=-1,*args, **kwargs):
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

        self.nPages = int(nPages)
        
    def start_requests(self):
        '''
        @overwrite
        @brief hepls to manipulate the start_urls to run several times the spider.
        @example 
        
        urls = [
          'http://quotes.toscrape.com/page/1/',
          'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
          yield scrapy.Request(url=url, callback=self.parse)
        '''

        # Create all the url to scrap
        for npage in range(2, self.nPages):
            # 'filters[status]=current&' search by status current only
            self.start_urls.append( self.start_urls[0]+'?filters[status]=current&page='+str(npage) )

        # Visit all the urls
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        '''
        if( self.debug ):
            from scrapy.utils.response import open_in_browser
            open_in_browser(response)
        '''
        hxs = scrapy.Selector( response )

        # With this we get all the table's rows in the page visited
        translatedRows = hxs.xpath('''//table[@id="translations"]/
                                        tr[ contains(@class, "status-current") ]/
                                            td[ contains(@class, "foreign-text")]''')
        # Iterate each row
        for rows in translatedRows:
            # Get the string
            stringToAnalize = rows.xpath('./text()').extract_first()

            # Scrapy Item
            string_to_analize_item = item_stringToAnalize() 
            # Set the item values
            string_to_analize_item['string'] = stringToAnalize.strip() # Strip is used to delete all white spaces, tabs and break lines
            string_to_analize_item['url']    = response.url

            # release the string scraped
            yield string_to_analize_item