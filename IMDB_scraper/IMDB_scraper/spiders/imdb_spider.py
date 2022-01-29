# to run 
# scrapy crawl imdb_spider -o movies.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    start_urls = ['https://www.imdb.com/title/tt11032374/']
   
    def parse(self,response):
        cast_url = response.urljoin("fullcredits")
        yield scrapy.Request(cast_url, callback = self.parse_full_credits)
    
    def parse_full_credits(self,response):

        for actor in [a.attrib["href"] for a in response.css("td.primary_photo a")]:
            actor_url = response.urljoin(actor)
            yield scrapy.Request(actor_url, callback = self.parse_actor_page)
 
    def parse_actor_page(self,response):
        actor_name = response.css("span.itemprop::text").get()
        movie_list = response.css("b a::text").getall()
        #experimented with the suggested css selectors.
        for movie in movie_list:
            yield{
                "Actor Name" : actor_name,
                "Movie" : movie
            }
