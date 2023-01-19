import scrapy
import re
import hashlib
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
#from bs4 import BeautifulSoup
# https://sasweb01.kennesaw.edu:8343/robots.txt


class KsuSpider(scrapy.Spider):
    name = "CS4422-IRbot0.1"

    
    

    custom_settings = {
         'DEPTH_PRIORITY' : 1,
         'SCHEDULER_DISK_QUEUE' : 'scrapy.squeues.PickleFifoDiskQueue',
         'SCHEDULER_MEMORY_QUEUE' : 'scrapy.squeues.FifoMemoryQueue',
         'CLOSESPIDER_PAGECOUNT' : 1700,
         'CONCURRENT_REQUEST': 1,
    }

    rules = (
        #Denies the extraction of this link since we do not have access to this, and will cause a timeout error
        Rule(LinkExtractor(deny=('https://sasweb01.kennesaw.edu:8343/robots.txt', ))),
    )


    def start_requests(self):
        urls = [
            'https://ccse.kennesaw.edu/',
            'https://www.kennesaw.edu/' ,
            'https://owllife.kennesaw.edu/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'CS4422-IRbot0.1-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
        y = response.css('link::attr(href)').re('https.*php$')
        #print(y[0])
        t = hashlib.md5(y[0].encode())
        t = t.hexdigest()

        
        yield {
                'page_id': t,   #response.css('link::attr(href)').re('https.*php$'),
                'url': response.url,
                'title': response.css('title::text').get(),
                'email': response.css('a::text').re('^\w+@[a-zA-Z_]+?.[a-zA-Z]{2,3}$'),
                'body' : response.xpath('//body//text()').re('(\w+)'),
            }

         #making a list of all the https on the current crawling website 
        #next_page = response.css('li a::attr(href)').re('https.*')
        next_page = response.css('li a::attr(href)').re("https://.*[\.]kennesaw.edu.*")
        #code that is supposed to follow onto the next links:
        

        for next_page in next_page:
            yield response.follow(next_page, callback=self.parse)

        #if next_page is not None:
        #    yield response.follow(next_page, callback=self.parse)


