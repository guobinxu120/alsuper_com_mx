# -*- coding: utf-8 -*-
import scrapy
from scrapy.exceptions import CloseSpider
from scrapy.selector import Selector
from scrapy.http.request import Request
from scrapy.selector import HtmlXPathSelector
from urlparse import urlparse
from scrapy.utils.response import open_in_browser
# import json
from json import loads
from urlparse import urlparse, parse_qsl
from datetime import date
import time
import datetime

# import msvcrt

class alsuper_com_mx_spider(scrapy.Spider):
    name = "alsuper_com_mx_spider"

    use_selenium = False

    ###########################################################

    def __init__(self, categories=None, *args, **kwargs):
        super(alsuper_com_mx_spider, self).__init__(*args, **kwargs)

        if not categories:
            raise CloseSpider('Received no categories!')
        else:
            self.categories = categories

        self.start_urls = loads(self.categories).keys()

    # f=open("links.txt",'r+b')
    # self.start_urls=f.readlines()

    # self.start_urls=["catalog.pl?id=98"]

    # def start_requests(self):
    # 	for url in self.start_urls:
    # 		yield scrapy.Request("http://alsuper.com/alsuperencasa/"+url.strip(),meta={'CatURL':url})

    # def parse(self, response):
    # 	sel=Selector(response)
    # 	# f=open("page_source.html",'w+b')
    # 	# f.write(response.body)

    # 	products = sel.xpath('//div[@class="col-md-3 txtc article-item"]')
    # 	if not products: return

    # 	for p in products:
    # 		item = {}
    # 		item['Vendedor'] = '66'
    # 		item['ID'] ="".join(p.xpath('form/input[@name="id"]/@value').extract()).strip()
    # 		item['Title'] = "".join(p.xpath('form/div[@class="article-item-bg"]/p[@class="uc"]/text()').extract()).strip()
    # 		item['Price'] = "".join(p.xpath('form/div[@class="article-item-bg"]/p/span/b/text()').extract()).replace('$','').strip().replace(',','.').strip()
    # 		item['Category URL'] =response.meta['CatURL']
    # 		item['Details URL'] ="".join(p.xpath('h2[@class="product-name"]/a/@href').extract()).strip()
    # 		item['Date'] = date.today()
    # 		yield item
    # 		#break

    # 	next_page=response.xpath('//a[contains(text(),"Siguiente")]/@href').extract()

    # 	if len(next_page)>0:
    # 		yield Request("http://alsuper.com/alsuperencasa/"+next_page[0],meta={'CatURL':response.meta['CatURL']},callback=self.parse)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request("https://alsuper.com/" + url.strip(), meta={'CatURL': url})

    def parse(self, response):
        sel = Selector(response)
        # f=open("page_source.html",'w+b')
        # f.write(response.body)
        offset = response.meta.get('offset', 0)
        cat_url = response.meta.get('CatURL', '')
        if offset == 0:
            products = sel.xpath('//ul[@class="row list-unstyled products--list"]/li')

        else:
            products = sel.xpath('//li')

        if not products:
            return

        for p in products:
            item = {}
            item['Vendedor'] = '66'
            item['ID'] = p.xpath('.//form/input[@name="id"]/@value').extract_first(default='').strip()
            item['Title'] = ' '.join(
                p.xpath('.//div[@class="product-item--desc"]/p/text()').extract_first(default='').split())
            item['Price'] = p.xpath('.//h4[@class="product-item--price"]/span/b/text()').extract_first(
                default='').replace(
                '$', '').strip().replace(',', '.').strip()
            item['Category URL'] = cat_url
            item['Details URL'] = "".join(p.xpath('.//h2[@class="product-name"]/a/@href').extract()).strip()
            item['Date'] = date.today()
            item['timestamp'] = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            item['image_url'] = response.urljoin(p.xpath('.//form/img/@data-src').extract_first())

            yield item

        url = 'https://alsuper.com' + cat_url
        parse_url = urlparse(url)
        data = dict(parse_qsl(parse_url.query))
        data['offset'] = '%s' % offset
        data['action'] = 'add_products_to_list'

        yield scrapy.FormRequest(
            url='https://alsuper.com/funciones_ajax.pl',
            formdata=data,
            callback=self.parse,
            meta={'offset': offset + 25, 'CatURL': cat_url}
        )
