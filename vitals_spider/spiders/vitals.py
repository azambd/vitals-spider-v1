# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request
import re
from ..items import VitalsSpiderItem


class VitalsSpider(CrawlSpider):
    name = 'vitals'
    allowed_domains = ['vitals.com']
    start_urls = [
            'https://www.vitals.com/directory/a',
            ]

    rules = (
        Rule(
            LinkExtractor(allow = (), restrict_xpaths = ('//ul[@class="pagination"]/li/a',)),
                callback="parse_links", 
                follow = True),)
    
    def parse_links(self, response):
        rows = response.xpath('//a[@class="name"]')
        for row in rows:
            temp_link = row.xpath('@href').extract()
            link = response.urljoin(''.join(temp_link))
            yield Request(link, callback=self.parse_item)
            #print link

    def parse_item(self, response):
        
        item = VitalsSpiderItem()

        data_in_raw = ''.join(response.xpath('//title/text()').extract_first())
        if '|' in data_in_raw:
            try:
                name_loc_spec = data_in_raw.split('|')
                item['name'] = name_loc_spec[0]
                location = name_loc_spec[1]
                item['speciality'] = name_loc_spec[2]
            except: 
                pass
        item['edu_name'] = response.xpath('//a[@data-label="education"]/text()').extract_first()
        street_address = response.xpath('//span[@itemprop="streetAddress"]/text()').extract_first()
        if street_address:
            try:
                street_address = street_address.strip()
                item['street_address'] = street_address
            except:
                item['street_address'] = ''
        item['city'] = response.xpath('//span[@itemprop="addressLocality"]/text()').extract_first().strip()
        item['state'] = response.xpath('//span[@itemprop="addressRegion"]/text()').extract_first().strip()
        item['zip_code'] = response.xpath('//span[@itemprop="postalCode"]/text()').extract_first().strip()
        item['responseCount'] = response.xpath('//meta[@itemprop="ratingCount"]/@content').extract_first()
        average_score = response.xpath('//span[@itemprop="ratingValue"]/text()').extract_first()
        if average_score:
            try:
                average_score = average_score.strip()
                item['average_score'] = average_score
            except:
                item['average_score'] = ''
        try:
            reviews = response.xpath('//a[@data-label="read_reviews"]/text()')[1].extract().strip()
            item['reviewCount'] = re.findall(r'\d+', reviews)
        except:
            item['reviewCount'] = ''

        item['link'] = response.url
        
        yield item
