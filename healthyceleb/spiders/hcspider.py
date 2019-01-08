# -*- coding: utf-8 -*-
import scrapy
from decimal import Decimal as dc
from unicodedata import numeric


class HcSpider(scrapy.Spider):
	name = 'hcspider'
	count = 0

	

	def start_requests(self):
		urls = [
		 # 'https://healthyceleb.com/category/statistics/sports-stars/male-sports-stars',
		 'https://healthyceleb.com/category/statistics/sports-stars/female-sports-stars',
		]

		for url in urls:
			self.count=0
			print("=====================>>>>>>>>>>>>>>>>>>")
			yield scrapy.Request(url=url, callback=self.parse)
	
	def parse(self, response):
		
		

		selector = response.css('.td-block-span6 .entry-title>a::attr(href)').extract()
		for i in selector:
			print(i)
			print(response.urljoin(i))
			if self.count>=100:
				break

			yield scrapy.Request(url=i, callback=self.parse_player)
			self.count+=1
		
		next_page_url = response.css('.last+ a::attr(href)').extract_first()

		if next_page_url and self.count<100:
			next_page_url = response.urljoin(next_page_url)
			yield scrapy.Request(url=next_page_url, callback=self.parse)


		self.log("DONE................")
	

	def parse_player(self, response):

		
		try:
			g,h,w = response.css("span:nth-child(5) .entry-crumb , .row-2 .column-2 , .row-3 .column-2").xpath("text()").extract()

			n = response.css('p:nth-child(4)').xpath('text()').extract_first()
			h = h.split()
			w = int(w.split()[0])
		
		except ValueError as v:
			
			g = response.css("span:nth-child(5) .entry-crumb").xpath("text()").extract_first()
			n = response.xpath('//p[preceding-sibling::h3/strong[text()="Born Name"]]/text()').extract_first()
			h = response.xpath('//p[preceding-sibling::h3/strong[text()="Height"]]/text()').extract_first()
			w = response.xpath('//p[preceding-sibling::h3/strong[text()="Weight"]]/text()').extract_first()

			h = h.split('or')[0].split()
			w =  int(w.split('or')[0].split()[0])

		if 'ft' in h:

			hi = dc(int(h[0]))*12
			if 'in' in h:
				if not h[-2][-1].isdigit():
					h[-2]=float(h[-2][:-1]) + numeric(h[-2][-1])

				hi += dc(h[-2])

			h = round(dc(hi)*dc(2.54),2)

		
		
		if 'male' or 'female' in g.lower():
			g = g.split()[0]

		# id of the player
		i = response.url.split('/')[-1]

		# url
		url = response.url

		print("====================>",self.count)

		yield {'id':i,'name':n,'gender':g,'height':h,'weight':w,'url':url}