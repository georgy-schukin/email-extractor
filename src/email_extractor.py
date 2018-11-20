#!/usr/bin/env python

from crawlers.email_crawler import EmailCrawler
from crawlers.science_direct_crawler import ScienceDirectCrawler
from crawlers.springer_crawler import SprigerCrawler

import os.path


def get_crawler(url):
    if "www.sciencedirect.com" in url:
        return ScienceDirectCrawler()
    elif "springer.com" in url:
        return SprigerCrawler()
    else:
        return EmailCrawler()


def extract_emails(url, logging=False):
    crawler = get_crawler(url)
    crawler.set_logging(logging)
    crawler.set_skip_patterns([r'\.pdf\W*'])
    crawler.set_page_load_timeout(-1)
    emails = crawler.crawl(url)
    crawler.close()
    return emails


def extract_emails_multiple(file_with_urls):
    emails = []
    with open(file_with_urls, "r") as f:
        for url in f.readlines():
            emails = emails + extract_emails(url.strip('\n'))
    return emails


def write_result(emails, filename):
    with open(filename, "w+") as f:
        f.write("\n".join(emails))


def merge_results(input_files, output_file):
    lines = set()
    for input_file in input_files:
        if not os.path.exists(input_file):
            continue
        with open(input_file, "r") as f:
            for line in f.readlines():
                lines.add(line.strip('\n'))
    with open(output_file, "w") as f:
        f.write("\n".join(sorted(lines)))


def main():
    url = input("Input url: ")
    #url = "https://link.springer.com/book/10.1007/978-3-319-67035-5"
    #for page in range(1, 8):
    #    url = "https://link.springer.com/search/page/{0}?facet-content-type=%22Book%22&date-facet-mode=between&previous-end-year=2019&previous-start-year=2015&facet-series=%227899%22&facet-end-year=2018&facet-sub-discipline=%22Information+Systems+Applications+%28incl.+Internet%29%22&facet-discipline=%22Computer+Science%22&facet-start-year=2015".format(page)
    #    emails = extract_emails(url)
    emails = extract_emails(url)
    write_result(emails, "output.txt")
    merge_results(["output.txt", "emails.txt"], "emails.txt")
    print('Done')


if __name__ == '__main__':
    main()
