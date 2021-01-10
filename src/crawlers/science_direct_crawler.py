from crawlers.email_crawler import EmailCrawler


class ScienceDirectCrawler(EmailCrawler):
    def __init__(self, options):
        super().__init__(options)
        self.set_patterns(['/science/article/pii/'])
        # self.set_skip_patterns([r'\.pdf$'])

