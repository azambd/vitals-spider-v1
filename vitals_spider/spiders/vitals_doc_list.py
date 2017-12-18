# -*- coding: utf-8 -*-
import scrapy
import json
from urlparse import urljoin #to join parse url to root url
from scrapy import Request
#import requests
from pprint import pprint

from ..items import VitalsSpiderItem

class UchcSpider(scrapy.Spider):
	name = 'vitals_doc_list'
	allowed_domains = ['592dc5anbt-2.algolianet.com']
	start_urls = ['http://592dc5anbt-2.algolianet.com']
	

	def start_requests(self):
		api_url = 'http://592dc5anbt-2.algolianet.com/1/indexes/*/queries?x-algolia-application-id=592DC5ANBT&x-algolia-api-key=3abbd60cc696b3a9d83ee2fcae88e351'
		headers={'Content-Type':'application/json; charset=UTF-8'}

		#url = "http://592dc5anbt-dsn.algolia.net/1/indexes/*/queries?x-algolia-application-id=592DC5ANBT&x-algolia-api-key=3abbd60cc696b3a9d83ee2fcae88e351"
		payload = {'requests': [{'indexName': 'vitals_instant_search','params': 'query=*&hitsPerPage=40&page=20'}]}

		request_body = json.dumps(payload)

    		yield Request(api_url, method="POST",body=request_body,headers=headers, )

		

	def parse(self, response):
		print response.body
		rooturl = 'http://www.vitals.com'

		item = VitalsSpiderItem()

		raw_data = response.body
		raw_data = ''.join(raw_data)
		json_data = json.loads(raw_data)
		data_point = []
		data_point = json_data['results'][0]['hits']
		for i in range(len(data_point)):

			item['name'] = data_point[i]['display_name']
			item['speciality_list'] =', '.join(data_point[i]['specialty'])
			item['street_address'] = data_point[i]['address1']
			item['city'] = data_point[i]['city']
			item['state'] = data_point[i]['state']
			item['zip_code'] = data_point[i]['zip']
			link_got = data_point[i]['url']
			item['link'] = urljoin(rooturl, link_got)
			
			try:
				item['gender'] = data_point[i]['gender']
			except:
				item['gender'] = ''
			try:
				item['phone'] = data_point[i]['phone']
			except:
				item['phone'] = ''
			try:
				item['responseCount'] = data_point[i]['number_of_ratings']
			except:
				item['responseCount'] = ''
			try: 
				item['reviewCount'] = data_point[i]['number_of_reviews'] 
			except:
				item['reviewCount'] = ''
			try:
				item['average_score'] = data_point[i]['overall_rating']
			except:
				item['average_score'] = ''
			try:
				item['practice_name'] = ', '.join(data_point[i]['expertise'])
			except:
				item['practice_name'] = ''
			try:
				item['location_name'] = data_point[i]['name']
			except:
				item['location_name'] = ''

			yield item
		


	

   
