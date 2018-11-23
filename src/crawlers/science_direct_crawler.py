from crawlers.email_crawler import EmailCrawler


class ScienceDirectCrawler(EmailCrawler):
    def __init__(self, options):
        super().__init__(options)
        self.set_patterns(['/science/article/pii/S07437315', '/science/article/pii/S01678191'])

