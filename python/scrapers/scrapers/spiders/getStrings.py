# -*- coding: utf-8 -*-
import pdb
import scrapy

# -items
# Import the item right. For test purposes this spider will call in several ways
# Using this try I catch all possibilities
# String to analize
try:
    from scrapers.scrapers.items import item_stringToAnalize
except ImportError:
    from scrapers.items import item_stringToAnalize
# number of pages
try:
    from scrapers.scrapers.items import item_numberOfPages
except ImportError:
    from scrapers.items import item_numberOfPages
# -items


class GetstringsSpider(scrapy.Spider):
    name = "getStrings"
    allowed_domains = ["translate.wordpress.org"]
    start_urls = []

    '''
    Activate several events if is set True for debugging or test proposes
    '''
    debug = False
    # debug = True

    def __init__(self, WPTpage=None, *args, **kwargs):
        '''
        @brief the constructor of the spider

        @param  WPTpage
                the page stract the strings
        @param args
        @param kwargs
        '''
        # Constructor
        super(GetstringsSpider, self).__init__(*args, **kwargs)

        # Load the start_urls received via parameter, if not passed, the url of
        # the WP development project in spanish is set
        if (WPTpage is None):
            url = 'https://translate.wordpress.org/projects/wp/dev/es/default'
            self.start_urls = [url]
        else:
            self.start_urls = [WPTpage]

        '''
        @brief N pages to scrap
        '''
        self.nPages = -1

    def parse(self, response):

        # ---------------- Get the number of pages to scrap ON
        hxs = scrapy.Selector(response)
        nPagesToScrap = hxs.xpath('''//div[@class="gp-content"]//
                                        div[@class="paging"]/
                                            *[@class="next"]/
                                            preceding::a[1]/
                                                text()''')

        # If debug is set, nPages = 5
        nPagesToScrap = int(nPagesToScrap.extract_first())
        self.nPages = nPagesToScrap if self.debug is False else 5

        item_npages = item_numberOfPages()
        item_npages['numberOfPages'] = self.nPages

        yield item_npages
        # ---------------- Get the number of pages to scrap OFF
        # ---------------- Construct all the urls ON
        stringsUrl = list()
        # Create all the url to scrap
        for npage in range(2, self.nPages):
            # 'filters[status]=current&' search by status current only
            stringsUrl.append(self.start_urls[0] +
                              '?filters[status]=current' +
                              '&sort[by]=priority&sort[how]=desc&sorts=Sort' +
                              '&page='+str(npage))

        # ---------------- Construct all the urls OFF

        # Visit all the urls
        for url in stringsUrl:
            yield scrapy.Request(url=url,
                                 callback=self.getStrings)

        pass

    def getStrings(self, response):
        '''
        Get all the strings needed to analyse, if they have an error.
        '''
        hxs = scrapy.Selector(response)

        # With this we get all the table's rows in the page visited
        translatedRows = hxs.xpath('''
                                   //table[@id="translations"]/
                                        tr[contains(@class, "status-current")]/
                                            td[contains(@class, "foreign-text")]
                                   ''')
        # Iterate each row
        for rows in translatedRows:
            # Get the string
            stringToAnalize = rows.xpath('./text()').extract_first()

            # Scrapy Item
            string_to_analize_item = item_stringToAnalize()
            # Set the item values
            # Strip is used to delete all white spaces, tabs and break lines
            string_to_analize_item['string'] = stringToAnalize.strip()
            string_to_analize_item['url'] = response.url

            # release the string scraped
            yield string_to_analize_item
