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
    crawler.set_skip_patterns(["\.pdf"])
    return crawler.crawl(url)


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
    emails = extract_emails(url)
    write_result(emails, "output.txt")
    merge_results(["output.txt", "emails.txt"], "emails.txt")
    print('Done')


if __name__ == '__main__':
    main()
