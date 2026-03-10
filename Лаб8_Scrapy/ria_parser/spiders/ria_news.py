import scrapy
from datetime import datetime

class RiaNewsSpider(scrapy.Spider):
    name = "ria_news"
    allowed_domains = ["ria.ru"]
    start_urls = ["https://ria.ru/"]

    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'DOWNLOAD_DELAY': 1.5,           
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,  
        'ROBOTSTXT_OBEY': False,          
        'COOKIES_ENABLED': False,
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 3,
    }

    def parse(self, response):
        """Парсим главную страницу ria.ru"""
        self.logger.info(f"Парсим страницу: {response.url}")

        news_items = response.css('a.list-item__title')  

        if not news_items:

            news_items = response.css('a[href*="/"]:has(strong), h3 a, .cell-list__item a')

        self.logger.info(f"Найдено элементов: {len(news_items)}")

        for item in news_items:
            title = item.css('::text').get()
            link = item.css('::attr(href)').get()

            if title and link and len(title.strip()) > 10: 
                yield {
                    'title': title.strip(),
                    'url': response.urljoin(link),
                    'timestamp': datetime.now().isoformat(),
                }
