import scrapy


class PeterParker(scrapy.Spider):
    # name of the Spider
    name = "parker"

    def start_requests(self):
        sources = ['https://www.eureporter.co/feed/',
                  'https://www.aljazeera.com/xml/rss/all.xml',
                  'http://feeds.feedburner.com/euronews/en/home/',
                  'http://feeds.bbci.co.uk/news/world/rss.xml',
                   'https://www.politico.eu/feed/',
                   'https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/section/world/rss.xml']
        for source in sources:
            yield scrapy.Request(url=source, callback=self.parse)

    def parse(self, response):
        # for each source, scrape it and return the result in an .html file
        page = response.url.split('/')[-3]
        filename = f'../../Results/news_{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
            self.log(f'Saved file {filename}')
