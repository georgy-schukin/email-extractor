#!/usr/bin/env python

from email_crawler import EmailCrawler
from science_direct_crawler import ScienceDirectCrawler
from springer_crawler import SprigerCrawler


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
    return crawler.crawl(url)


def write_result(emails, filename):
    with open(filename, "w+") as f:
        f.writelines(emails)


def main():
    url = input("Input url: ")
    #url = "https://link.springer.com/book/10.1007/978-3-319-67035-5"
    emails = extract_emails(url)
    write_result(emails, "output.txt")
    print('Done')


if __name__ == '__main__':
    main()
