from datetime import datetime
import sys
import scrapy
from scrapy.crawler import CrawlerProcess


class CandoosmsSpider(scrapy.Spider):
    name = 'candoosms'
    start_urls = ['http://my.candoosms.com/ms-sendbox-o']

    def start_requests(self):
        cookie_value = getattr(self,'cookie','')
        cookies = {'PHPSESSID': cookie_value}
        for url in self.start_urls:
            yield scrapy.Request(url, cookies=cookies, callback=self.parse_homepage)

    def parse_homepage(self,response):
        rand = response.css('button.offset2::attr(onclick)').extract()[0]
        rand = rand.replace('DoSearch','').replace('(this);','')
        start = getattr(self,'s',1)
        end = getattr(self,'e',3)
        for i in range(start,end+1): 
            print(f'Getting page {i}')
            request = scrapy.Request(f'https://my.candoosms.com/ms-sendbox-o?useajax=true&rand={rand}&fid=&page={i}&order=outbound_message_id:DESC&filter=', 
                callback=self.extractTable,
                                    # errback=self.errback_httpbin,
                                    dont_filter=True,
                                    )
            request.meta['p'] = i
            yield request
    
    def extractTable(self,response):
        cells = response.css('tr td.tbl-cell')
        statusCells = response.css('tr td.tbl-cell i::attr(title)').extract()
        # if len(cells)<70:
        #     self.logger.error(f'Page size is {len(cells)}')
        for i in range(0,len(cells)//10):
            yield {
                'id' : cells[0+i*10].css('::text').get(default=''),
                'sender' : cells[2+i*10].css('::text').get(default=''),
                'construct_at' : cells[4+i*10].css('::text').get(default=''),
                'status' : statusCells[i],
                'crawl_at' : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'page': response.meta['p']
            }

    def warn_on_generator_with_return_value_stub(spider, callable):
        pass

    scrapy.utils.misc.warn_on_generator_with_return_value = warn_on_generator_with_return_value_stub
    scrapy.core.scraper.warn_on_generator_with_return_value = warn_on_generator_with_return_value_stub

process = CrawlerProcess(settings={
'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
"FEEDS": {
    'candoosms_%(time)s.csv': {
        'format': 'csv',
        'overwrite': True
        },
},
"LOG_LEVEL" : "ERROR",
})

startPage = 1
endPage = 1
cookie = sys.argv[1]

if (len(sys.argv) == 4 ):
    startPage = int(sys.argv[2])
    endPage = int(sys.argv[3])

print(f'Process to get from page {startPage} to page {endPage}')

process.crawl(CandoosmsSpider, cookie=cookie, s=startPage,e=endPage)
process.start()