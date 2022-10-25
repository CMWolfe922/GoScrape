import scrapy
from ..items import MeetingItem

class AaMeetingsSpider(scrapy.Spider):
    name = 'aa_meetings'
    allowed_domains = ['www.aa-meetings.com']
    start_urls = ['https://www.aa-meetings.com/aa-meeting/']
    base_url = 'https://www.aa-meetings.com/aa-meeting'

    def start_requests(self):

        urls = self.start_urls

        for url in urls:
            response = scrapy.Request(url=url, callback=self.parse)
            yield response

        for num in range(2, 2800):
            url = self.base_url + '/page/' + str(num) + '/'
            response = scrapy.Request(url, callback=self.parse)
            yield response


    def parse(self, response):
        # get each meeting link on the page. The spider will have to follow
        # each link to aquire the needed information. Once the all the links
        # have been followed, the spider will have to go to the next page.
        page_links = response.xpath('//div[@class="fui-card-body"]//a/@href').getall()
        for link in page_links:
            self.logger.info('Retrieving data from %s', link)
            item = MeetingItem()
            item['link'] = link
            yield scrapy.Request(response.urljoin(link), self.parse_meeting)


    def parse_meeting(self, response):
        self.logger.info('Retrieving item data from %s', response.url)

        # meeting name:
        name = response.css('div.fui-card-body p.weight-300::text').get()

        # get address data:
        address = response.css('div.fui-card-body address.weight-300::text').get()

        try:
            # make sure that all of the card values are scraped and valid
            # to avoid raising a ValueError exception
            card = response.css('div.fui-card-body p.weight-300 a::text').getall()

            if len(card) > 3:
                elements = len(card)

                print(f"This is how the extra elements showup: ")
                print(f"Number of elements --> {elements}")
                print(f"Data to seperate: {card}")

            elif len(card) == 3:
                # Get city, state and zipcode:
                city, state, zipcode = card
            elif len(card) == 2:
                city, state = card
                zipcode = 'zipcode'
            elif len(card) == 1:
                city = card
                state, zipcode = 'state', 'zipcode'
            else:
                city, state, zipcode = 'city', 'state', 'zipcode'
        except ValueError as ve:
            self.logger.error(f'{ve} Exception Raised..')

        try:
            # make sure that all of the table values are scraped and valid
            # to avoid raising a ValueError exception
            table = response.xpath('//*[@class="table fui-table"]//tr//td/text()').getall()
            if len(table) >= 3:
                # I need to check and see if there is more than 3, since the table can
                # have 9 or 12 or 30. Chances are it will be incremests of 3:

                # extract table data day, time and info:
                day, time, info = table
            elif len(table) == 2:
                day, time = table
                info = 'info'
            elif len(table) == 1:
                day = table
                time, info  = 'time', 'info'
            else:
                day, time, info = 'day', 'time', 'info'

        except ValueError as ve:
            self.logger.error(f'{ve} Exception Raised..')

        item = MeetingItem(name=name, address=address, city=city, state=state, zipcode=zipcode, day=day, time=time, info=info)
        yield item
