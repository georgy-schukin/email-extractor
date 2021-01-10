from crawlers.email_crawler import EmailCrawler


class SpringerCrawler(EmailCrawler):
    def __init__(self, options):
        super().__init__(options)
        self.add_pattern(r'springer\.com\w*/chapter/')
        self.add_pattern(r'springer\.com\w*/book/')
        self.add_pattern(r'springer\.com\w*/article/[\d\.]+/[\d\w\-]+/?$')
        self.add_skip_pattern(r'/fulltext\.html$')

