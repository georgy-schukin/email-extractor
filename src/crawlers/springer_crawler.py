from crawlers.email_crawler import EmailCrawler


class SpringerCrawler(EmailCrawler):
    def __init__(self, options):
        super().__init__(options)
        self.set_patterns([r'springer\.com\w*/chapter/',
                           r'springer\.com\w*/article/',
                           r'springer\.com\w*/book/'
                           ])
        self.set_skip_patterns([r'/fulltext\.html$'])

