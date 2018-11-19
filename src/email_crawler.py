from selenium_web_walker import SeleniumWebWalker
from email_parser import EmailParser
import time


class EmailCrawler(object):
    def __init__(self):
        super().__init__()
        self.patterns = None
        self.logging = False
        self.walker = SeleniumWebWalker(page_load_timeout=30)
        self.parser = EmailParser()

    def set_patterns(self, patterns):
        self.patterns = patterns

    def set_logging(self, logging):
        self.logging = logging

    def crawl(self, start_url):
        emails = set()
        urls_to_visit = set()
        visited_urls = set()
        urls_to_visit.add(start_url)
        while len(urls_to_visit) > 0:
            url = urls_to_visit.pop()
            print("Process " + url)
            try:
                self.walker.open(url)
                time.sleep(5)
            except Exception as e:
                print("Error: " + str(e))
                continue
            finally:
                visited_urls.add(url)
            found_emails = self._extract_emails()
            print("Emails: " + str(found_emails))
            for email in found_emails:
                emails.add(email)
            for u in self.walker.get_urls():
                if self._matches_pattern(u) and u not in visited_urls:
                    urls_to_visit.add(u)
        return list(emails)

    def _extract_emails(self):
        return self.parser.get_emails(self.walker.get_current_page_source())

    def _matches_pattern(self, url):
        if not self.patterns:
            return True
        for pattern in self.patterns:
            if pattern in url:
                return True
        return False
