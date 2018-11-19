from crawlers.email_crawler import EmailCrawler


class SprigerCrawler(EmailCrawler):
    def __init__(self):
        super().__init__()
        self.set_patterns([r'springer\.com/chapter/', r'springer\.com/article/', r'springer\.com/book/'])

