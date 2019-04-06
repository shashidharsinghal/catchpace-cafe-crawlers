# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
import string
import logging

iconToDigitMapping= {
    "dc":"+",
    "fe":"",
    "hg":"",
    "nm":"7",
    "vu":"3",
    "ba":"-",
    "ts":"4",
    "acb":"0",
    "ji":"9",
    "yz":"1",
    "rq":"5",
    "wx":"2",
    "lk":"8",
    "po":"6"
}

def remove_control_characters(value):
    return value.replace(u"\n",'').replace(u"\t",'').split("Votes")[0]

def mapIconToDigit(value):
    icon = value.split(" ")[1].split("-")[1]
    return iconToDigitMapping.get(icon,"none")

def fetchDocIds(value):
    logging.info(value)
    value = value.split(',')
    value = value[len(value)-1].replace(u"'","").replace(u")","").replace(u";","")
    return value
    

class CafeItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    addr = scrapy.Field(
        input_processor = MapCompose(str.strip),
        output_processor = TakeFirst()
    )
    revCount = scrapy.Field(
        input_processor = MapCompose(str.strip,remove_control_characters),
        output_processor = TakeFirst()
    )
    phoneNumber = scrapy.Field(
        input_processor = MapCompose(mapIconToDigit),
        output_processor = Join("")
    ) 
    openhours = scrapy.Field()

    website = scrapy.Field(
        input_processor = MapCompose(str.strip,remove_control_characters),
        output_processor = TakeFirst()
    )
    avgRating = scrapy.Field(
        input_processor = MapCompose(str.strip,remove_control_characters),
        output_processor = TakeFirst()
    )
    totreviews = scrapy.Field(
        input_processor = MapCompose(str.strip,remove_control_characters),
        output_processor = TakeFirst()
    )
    
    detailPgLnk = scrapy.Field()

    docId = scrapy.Field(
        input_processor = MapCompose(str.strip,fetchDocIds),
        output_processor = TakeFirst()
    )

    dtlsdocid = scrapy.Field()

