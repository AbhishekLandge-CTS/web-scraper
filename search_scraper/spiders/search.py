import scrapy
import re
from result_store import store_result

class SearchSpider(scrapy.Spider):
    name = "search_spider"

    def __init__(self, search_url, query, **kwargs):
        self.start_urls = [f"{search_url}?q={query.replace(' ', '+')}"]
        super().__init__(**kwargs)

    def parse(self, response):
        phone_pattern = re.compile(r'(\+?\d[\d\s\-().]{7,}\d)')
        text_blocks = response.xpath('//body//text()').getall()
        matches = []

        for text in text_blocks:
            phones = phone_pattern.findall(text)
            matches.extend([p.strip() for p in phones])

        store_result({
            "query": response.url.split("?q=")[-1],
            "phone_numbers": list(set(matches)) or ["Not found"]
        })





# import scrapy
# from result_store import store_result
# from urllib.parse import urlencode

# class SearchSpider(scrapy.Spider):
#     name = "search_spider"

#     def __init__(self, search_url=None, query=None, **kwargs):
#         super().__init__(**kwargs)
#         self.search_url = search_url
#         self.query = query

#     def start_requests(self):
#         url = f"{self.search_url}?{urlencode({'q': self.query})}"
#         yield scrapy.Request(url=url, callback=self.parse)

#     def parse(self, response):
#         html_content = response.text  # full HTML as string
#         store_result({'html': html_content})
