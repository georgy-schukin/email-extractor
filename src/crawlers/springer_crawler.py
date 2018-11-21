from crawlers.email_crawler import EmailCrawler


class SpringerCrawler(EmailCrawler):
    def __init__(self):
        super().__init__()
        self.set_patterns([r'springer\.com\w*/chapter/', r'springer\.com\w*/article/', r'springer\.com\w*/book/'])

