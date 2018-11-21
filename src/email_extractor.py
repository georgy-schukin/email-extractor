#!/usr/bin/env python

from crawlers.email_crawler import EmailCrawler
from crawlers.science_direct_crawler import ScienceDirectCrawler
from crawlers.springer_crawler import SpringerCrawler
from listeners.logger import Logger
from listeners.file_writer import FileWriter

import os.path


def get_crawler(url):
    if "www.sciencedirect.com" in url:
        return ScienceDirectCrawler()
    elif "springer.com" in url:
        return SpringerCrawler()
    else:
        return EmailCrawler()


def extract_emails(crawler, url, listeners):
    crawler.set_skip_patterns([r'\.pdf\W*'])
    crawler.set_page_load_timeout(-1)
    crawler.crawl(url, listeners)


def extract_emails_multiple(crawler, urls, listeners):
    crawler.set_skip_patterns([r'\.pdf\W*'])
    crawler.set_page_load_timeout(-1)
    for url in urls:
        crawler.crawl(url, listeners)


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
    listeners = [Logger(), FileWriter("output.txt")]
    #url = input("Input url: ")
    #url = "https://link.springer.com/book/10.1007/978-3-319-67035-5"
    urls = []
    # Comm. in Computer
    #for page in range(1, 8):
    #    urls.append("https://link.springer.com/search/page/{0}?facet-content-type=%22Book%22&date-facet-mode=between&previous-end-year=2019&previous-start-year=2015&facet-series=%227899%22&facet-end-year=2018&facet-sub-discipline=%22Information+Systems+Applications+%28incl.+Internet%29%22&facet-discipline=%22Computer+Science%22&facet-start-year=2015".format(page))
    # LNCS
    #for page in range(1, 18):
    #    urls.append("https://link.springer.com/search/page/{0}?facet-sub-discipline=%22Computer+Communication+Networks%22&facet-content-type=%22Book%22&date-facet-mode=between&facet-content-type=%22ConferenceProceedings%22&facet-series=%22558%22&facet-language=%22En%22&sortOrder=newestFirst&facet-end-year=2018&facet-sub-discipline=%22Information+Systems+Applications+%28incl.+Internet%29%22&facet-discipline=%22Computer+Science%22&facet-start-year=2015".format(page))
    # Journal of Supercomp
    #for page in range(1, 72):
    #    urls.append("https://link.springer.com/search/page/{0}?date-facet-mode=between&facet-journal-id=11227&facet-end-year=2018&query=&facet-discipline=%22Computer+Science%22&facet-start-year=2015".format(page))
    for vol in range(70, 126):
        urls.append("https://www.sciencedirect.com/journal/journal-of-parallel-and-distributed-computing/vol/{0}/suppl/C".format(vol))
    extract_emails_multiple(ScienceDirectCrawler(), urls, listeners)
    #extract_emails(get_crawler(url), url, listeners)
    merge_results(["output.txt", "emails.txt"], "emails.txt")
    print('Done')


if __name__ == '__main__':
    main()
