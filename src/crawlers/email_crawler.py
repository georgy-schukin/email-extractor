from walkers.selenium_web_walker import SeleniumWebWalker
from parsers.email_parser import EmailParser

import re


class EmailCrawler(object):
    def __init__(self):
        super().__init__()
        self.patterns = None
        self.skip_patterns = None
        self.logging = False
        self.walker = SeleniumWebWalker(page_load_timeout=30)
        self.parser = EmailParser()

    def set_patterns(self, patterns):
        self.patterns = [re.compile(pattern) for pattern in patterns]

    def set_skip_patterns(self, patterns):
        self.skip_patterns = [re.compile(pattern) for pattern in patterns]

    def set_logging(self, logging):
        self.logging = logging

    def crawl(self, start_url):
        emails = set()
        urls_to_visit = set()
        visited_urls = set()
        urls_to_visit.add(start_url)
        while len(urls_to_visit) > 0:
            url = urls_to_visit.pop()
            print("Processing " + url)
            try:
                self.walker.open(url)
            except Exception as e:
                print("Error: " + str(e))
                continue
            finally:
                visited_urls.add(url)
            found_emails = self._extract_emails()
            print("Emails: " + str(found_emails))
            for email in found_emails:
                emails.add(email)
            for u in self._extract_urls():
                if u not in visited_urls:
                    urls_to_visit.add(u)
        return list(emails)

    def _extract_urls(self):
        urls = self.walker.get_urls()
        urls = [url for url in urls if self._matches_pattern(url) and not self._matches_skip_pattern(url)]
        urls = [url.split('#')[0] for url in urls]  # remove url's part after '#'
        return urls

    def _extract_emails(self):
        return self.parser.get_emails(self.walker.get_current_page_source())

    def _matches_pattern(self, url):
        if not self.patterns:
            return True
        for pattern in self.patterns:
            if pattern.search(url):
                return True
        return False

    def _matches_skip_pattern(self, url):
        if not self.skip_patterns:
            return False
        for pattern in self.skip_patterns:
            if pattern.search(url):
                return True
        return False
