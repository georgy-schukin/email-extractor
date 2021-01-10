from crawlers.email_crawler import EmailCrawler


class ScienceDirectCrawler(EmailCrawler):
    def __init__(self, options):
        super().__init__(options)
        self.add_pattern(r'/science/article/.*pii/')

