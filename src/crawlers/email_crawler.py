from walkers.selenium_web_walker import SeleniumWebWalker
from parsers.email_parser import EmailParser

import re


class EmailCrawler(object):
    def __init__(self, options):
        super().__init__()
        self.patterns = []
        self.skip_patterns = []
        self.walker = SeleniumWebWalker(options)
        self.parser = EmailParser()

    def clear_patterns(self):
        self.patterns = []

    def set_patterns(self, patterns, terminal=False):
        self.patterns = [(re.compile(pattern), terminal) for pattern in patterns]

    def add_patterns(self, patterns, terminal=False):
        for pattern in patterns:
            self.add_pattern(pattern, terminal)

    def add_pattern(self, pattern, terminal=False):
        pattern_c = re.compile(pattern)
        if pattern_c not in self.patterns:
            self.patterns.append((pattern_c, terminal))

    def clear_skip_patterns(self):
        self.skip_patterns = []

    def set_skip_patterns(self, skip_patterns):
        self.skip_patterns = [re.compile(skip_pattern) for skip_pattern in skip_patterns]

    def add_skip_patterns(self, skip_patterns):
        for skip_pattern in skip_patterns:
            self.add_skip_pattern(skip_pattern)

    def add_skip_pattern(self, skip_pattern):
        skip_pattern_c = re.compile(skip_pattern)
        if skip_pattern_c not in self.skip_patterns:
            self.skip_patterns.append(skip_pattern_c)

    def set_page_load_timeout(self, page_load_timeout):
        self.walker.set_page_load_timeout(page_load_timeout)

    def crawl(self, start_url, listeners, visited=()):
        emails = set()
        urls_to_visit = [start_url]
        visited_urls = set(visited)
        for listener in listeners:
            listener.notify_start()
        while len(urls_to_visit) > 0:
            url = urls_to_visit.pop()
            if url in visited_urls:
                continue
            for listener in listeners:
                listener.notify_url(url)
            try:
                self.walker.open(url)
                found_emails = self._extract_emails()
                found_urls = self._extract_urls()
                visited_urls.add(url)
            except Exception as e:
                print("Error: " + str(e))
                continue
            for email in found_emails:
                emails.add(email)
                for listener in listeners:
                    listener.notify_email(email)
            for listener in listeners:
                listener.notify_url_end(url)
            if self._is_terminal(self.walker.get_current_page_url()):
                continue
            for u in found_urls:
                if u not in visited_urls:
                    urls_to_visit.append(u)
        for listener in listeners:
            listener.notify_end()
        return list(emails), list(visited_urls)

    def _extract_urls(self):
        urls = self.walker.get_urls()
        urls = [url for url in urls if self._matches_pattern(url) and not self._matches_skip_pattern(url)]
        urls = [url.split('#')[0] for url in urls]  # remove url's part after '#'
        return urls

    def _extract_emails(self):
        return self.parser.get_emails(self.walker.get_current_page_source())

    def _matches_pattern(self, url, check_for_terminal=False):
        if not self.patterns:
            return True
        for pattern in self.patterns:
            if pattern[0].search(url):
                return pattern[1] if check_for_terminal else True
        return False

    def _matches_skip_pattern(self, url):
        if not self.skip_patterns:
            return False
        for pattern in self.skip_patterns:
            if pattern.search(url):
                return True
        return False

    def _is_terminal(self, url):
        return self._matches_pattern(url, check_for_terminal=True)

    def close(self):
        self.walker.close()
