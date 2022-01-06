import scrapy
from scrapy.http.request import Request


class CategoriesOfalsuper_com_mx(scrapy.Spider):
    name = "categories_of_alsuper_com_mx"

    start_urls = ['https://alsuper.com/']
    use_selenium = False
    def parse(self, response):

        # f=open("links.txt",'w+b')
        # links=response.xpath('//div[@id="categories"]/ul/li/ul/li/a/@href').extract()
        links = response.xpath('//ul[@class="menu-subcategories"]/li/ul/li/a/@href').extract()
        final_links_list = []
        for l in links:
            try:
                # f.write(l.strip()+"\n")
                final_links_list.append(l.strip())
            except:
                pass

        yield {'links': final_links_list}
