import scrapy
import re

from pep_parse.items import PepParseItem

PATTERN = re.compile(r"^PEP\s(?P<number>\d+)[\s–]+(?P<name>.*)")


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        pep_links = response.css('a.pep::attr("href")').getall()
        for link in pep_links:
            yield response.follow(link, callback=self.parse_pep)

    def parse_pep(self, response):
        pep = response.css("section[id='pep-content']")
        h1_tag = PATTERN.search(pep.css("h1::text").get())
        if h1_tag:
            number, name = h1_tag.group("number", "name")
        data = {
            'number': number,
            'name': name,
            'status': pep.css("abbr::text")[0].get()
        }
        yield PepParseItem(data)
