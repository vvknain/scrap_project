# -*- coding: utf-8 -*-
import scrapy
import pandas as pd
from crawl_spider.items import DirectorItem


class DirectorsSpiderSpider(scrapy.Spider):
	name = 'directors_spider'

	custom_settings = {
	'DEPTH_LIMIT': 2,
	'DEPTH_PRIORITY': 1       # BPO
	}

	allowed_domains = ['zaubacorp.com']
	start_urls = ['https://www.zaubacorp.com/company/DR-REDDY-S-LABORATORIES-LTD/L85195TG1984PLC004507']

	scraped_data = pd.DataFrame(columns=['url', 'din', 'director_name', 'designation', 'appointment_date', 'search_depth'])

	companies_url_crawled = {}
	companies_url_crawled[start_urls[0]] = custom_settings['DEPTH_LIMIT']

	def parse(self, response):
		# default callack to process downloaded response

		companies_url_to_crawl = []

		# temp dataframe
		scraped_data1 = pd.DataFrame(columns=['url', 'din', 'director_name', 'designation', 'appointment_date', 'search_depth'])
		x = 1
		while 1:
			# collecting text info
			arr = response.xpath("//tr[@id='package{}']/td/p/text()".format(x)).extract()

			# collecting text(name) from href
			arr1 = response.xpath("//tr[@id='package{}']/td/p/a/text()".format(x)).extract()
			if len(arr):
				scraped_data1['din'] = arr[0:1]
				scraped_data1['designation'] = arr[1:2]
				scraped_data1['appointment_date'] = arr[2:3]
				scraped_data1['director_name'] = arr1[0:1]
				scraped_data1['url'] = response.xpath("//tr[@id='package{}']/td[2]/p/a/@href".format(x)).extract()[0:1]
				scraped_data1['search_depth'] = [DirectorsSpiderSpider.companies_url_crawled[response.url]]

				DirectorsSpiderSpider.scraped_data = pd.concat([DirectorsSpiderSpider.scraped_data, scraped_data1])

				# collecting urls to crawl
				companies_url_to_crawl.extend(response.xpath("//div[@id='accordion{}']/table[1]/tr/td[1]/p/a/@href".format(x)).extract())
			else:
				break

			x += 1

		if DirectorsSpiderSpider.companies_url_crawled[response.url] != 1:
			companies_url_to_crawl = list(set(companies_url_to_crawl) - (set(companies_url_to_crawl) & set(DirectorsSpiderSpider.companies_url_crawled.keys())))

			for link in companies_url_to_crawl:
				DirectorsSpiderSpider.companies_url_crawled[link] = DirectorsSpiderSpider.companies_url_crawled[response.url] - 1
				yield scrapy.Request(link, callback=self.parse)

		DirectorsSpiderSpider.scraped_data.to_csv('data/directors.csv')
		print(DirectorsSpiderSpider.companies_url_crawled)
