# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class MeetingItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    address = Field()
    city = Field()
    state = Field()
    zipcode = Field()
    time = Field()
    day = Field()
    info = Field()
