# -*- coding: utf-8 -*-
import scrapy

# Import the item right. For test purposes this spider will call in several ways
# Using this try I catch all possibilities   
try:
    from scrapers.scrapers.items import item_numberOfPages
except ImportError:
    from scrapers.items import item_numberOfPages

class GetnumberpagesSpider(scrapy.Spider):
    """
    Spider to get the number of pages needed to scrap
    """
    name = "getNumberPages"
    allowed_domains = ["translate.wordpress.org"]
    start_urls = ['https://translate.wordpress.org/projects/wp/dev/es/default']

    def __init__(self, *args, **kwargs):
        '''
        @brief the constructor of the spider
        '''
        # Parent's Constructor 
        super(GetnumberpagesSpider, self).__init__(*args, **kwargs)

        # initializate with a non possible value
        self.numberOfPages = -1

    def parse(self, response):

        hxs = scrapy.Selector( response )
        pagesToScrap = hxs.xpath('''//div[@class="gp-content"]//
                                        div[@class="paging"]/
                                            *[@class="next"]/
                                            preceding::a[1]/
                                                text()''')

        self.numberOfPages = pagesToScrap.extract_first()


        item_npages = item_numberOfPages()
        item_npages['numberOfPages'] = self.numberOfPages

        # print("---------------------")
        # print(numberOfPages['numberOfPages'])
        # print("---------------------")
            
        yield item_npages;

        pass
