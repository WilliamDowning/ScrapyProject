import scrapy
import re

class KsuSpider(scrapy.Spider):
    name = "CS4422-IRbot"
    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': 500, 
        'CONCURRENT_REQUEST': 3,
        'DEPTH_PRIORITY' : 3,
        'SCHEDULER_DISK_QUEUE' : 'scrapy.squeues.PickleFifoDiskQueue',
        'SCHEDULER_MEMORY_QUEUE': 'scrapy.squeues.FifoMemoryQueue',
    }
    def start_requests(self):
        start_urls = [
            'https://ccse.kennesaw.edu/',
            'https://www.kennesaw.edu/' ,


        ]
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f'IRbot-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}')
        yield {
            'pageid': response.css('link::attr(href)').re('https.*php$'),
            'url': response.url,
            'title': response.css('title::text').get(),
            'email': response.css('a::text').re('^\w+@[a-zA-Z]+?.[a-zA-Z]{2,3}$'),
        }
        #making a list of all the https on the current crawling website 
        next_page = response.css('li a::attr(href)').re("https://www.kennesaw\.edu.*") # all kennesaw.edu domains
        #next_page = response.css('li a::attr(href)').getall() #returns every href on page
        #next_page = response.css('li a::attr(href)').get() #only returns https://www.kennesaw.edu/apply.php'
        #this doesn't iterate through next_page
        #if next_page is not None:
        #    yield response.follow(next_page, callback=self.parse)
        #code that is supposed iterate through list of links from next_page and follow onto the next links:
        for next_page in next_page:
            yield response.follow(next_page, callback=self.parse)