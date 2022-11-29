from datetime import datetime
import scrapy


class CandoosmsSpider(scrapy.Spider):
    name = 'candoosms'
    start_urls = ['http://my.candoosms.com/index.php']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': 'eaico', 'password': '09144158862'},
            callback=self.after_login
        )

    def after_login(self, response):
         return  scrapy.Request("http://my.candoosms.com/ms-sendbox", callback=self.parse_homepage,
                                    # errback=self.errback_httpbin,
                                    dont_filter=True,
                                    )

    def parse_homepage(self,response):
        rand = response.css('button.offset2::attr(onclick)').extract()[0]
        rand = rand.replace('DoSearch','').replace('(this);','')
        for i in range(7500,9746):  #9746
            yield scrapy.Request(f'https://my.candoosms.com/ms-sendbox?useajax=true&rand={rand}&fid=&page={i}&order=outbound_message_id:DESC&filter=', 
                callback=self.extractTable,
                                    # errback=self.errback_httpbin,
                                    dont_filter=True,
                                    )
    
    def extractTable(self,response):
        cells = response.css('tr td.tbl-cell')
        statusCells = response.css('tr td.tbl-cell i::attr(title)').extract()
        if len(cells)<70:
            self.logger.error(len(cells))
        self.logger.info(len(cells))
        for i in range(0,len(cells)//10):
            yield {
                'id' : cells[0+i*10].css('::text').get(default=''),
                'sender' : cells[2+i*10].css('::text').get(default=''),
                'construct_at' : cells[4+i*10].css('::text').get(default=''),
                'status' : statusCells[i],
                'crawl_at' : datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

