from crawlers.email_crawler import EmailCrawler


class ScienceDirectCrawler(EmailCrawler):
    def __init__(self):
        super().__init__()
        self.set_patterns(['/science/article/pii/'])

