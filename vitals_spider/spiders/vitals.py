# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy import Request
import re
from ..items import VitalsSpiderItem


class VitalsSpider(CrawlSpider):
    name = 'vitals'
    handle_httpstatus_list = [404, 400, 302, 301]
    allowed_domains = ['vitals.com']
    start_urls = [
            'https://www.vitals.com/directory/a',
            'https://www.vitals.com/directory/b',
            'https://www.vitals.com/directory/c',
            'https://www.vitals.com/directory/d',
            'https://www.vitals.com/directory/e',
            'https://www.vitals.com/directory/f',
            'https://www.vitals.com/directory/g',
            'https://www.vitals.com/directory/h',
            'https://www.vitals.com/directory/i',
            'https://www.vitals.com/directory/j',
            'https://www.vitals.com/directory/k',
            'https://www.vitals.com/directory/l',
            'https://www.vitals.com/directory/m',
            'https://www.vitals.com/directory/n',
            'https://www.vitals.com/directory/o',
            'https://www.vitals.com/directory/p',
            'https://www.vitals.com/directory/q',
            'https://www.vitals.com/directory/r',
            'https://www.vitals.com/directory/s',
            'https://www.vitals.com/directory/t',
            'https://www.vitals.com/directory/u',
            'https://www.vitals.com/directory/v',
            'https://www.vitals.com/directory/w',
            'https://www.vitals.com/directory/x',
            'https://www.vitals.com/directory/y',
            'https://www.vitals.com/directory/z',
            ]

    rules = (
        Rule(
            LinkExtractor(allow = (), restrict_xpaths = ('//ul[@class="pagination"]/li/a',),unique=True,),
                callback="parse_links", 
                follow = True),)
    
    def parse_links(self, response):
        rows = response.xpath('//a[@class="name"]')
        for row in rows:
            # temp_link = row.xpath('@href').extract()
            # link = response.urljoin(''.join(temp_link))
            temp_link = row.xpath('@href').extract_first()
            link = response.urljoin(temp_link)
            yield Request(link, callback=self.parse_item)
            print link

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
        
        try:
            street_address = response.xpath('//span[@itemprop="streetAddress"]/text()').extract_first()
            street_address = street_address.strip()
            item['street_address'] = street_address
        except:
            item['street_address'] = ''

        try:
            city = response.xpath('//span[@itemprop="addressLocality"]/text()').extract_first()
            city = city.strip()
            item['city'] = city
        except:
            item['city'] = ''
        try:
            state = response.xpath('//span[@itemprop="addressRegion"]/text()').extract_first()
            state = state.strip()
            item['state'] = state
        except:
            item['state'] = ''
        try:
            zip_code = response.xpath('//span[@itemprop="postalCode"]/text()').extract_first()
            zip_code = zip_code.strip()
            item['zip_code'] = zip_code
        except:
            item['zip_code'] = ''
        try:      
            item['responseCount'] = response.xpath('//meta[@itemprop="ratingCount"]/@content').extract_first()
        except:
            item['responseCount'] = ''
        try:
            average_score = response.xpath('//span[@itemprop="ratingValue"]/text()').extract_first()
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
