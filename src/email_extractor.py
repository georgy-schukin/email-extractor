#!/usr/bin/env python

from crawlers.email_crawler import EmailCrawler
from crawlers.science_direct_crawler import ScienceDirectCrawler
from crawlers.springer_crawler import SpringerCrawler
from listeners.logger import Logger
from listeners.file_writer import FileWriter
from listeners.url_logger import URLLogger
from util import read_lines

import os.path
import random
import json


def get_crawler(url, options):
    if "www.sciencedirect.com" in url:
        return ScienceDirectCrawler(options)
    elif "springer.com" in url:
        return SpringerCrawler(options)
    else:
        return EmailCrawler(options)


def extract_emails(crawler, url, listeners, visited=()):
    crawler.add_skip_patterns([r'\.pdf\W*'])
    crawler.set_page_load_timeout(-1)
    crawler.crawl(url, listeners, visited)


def extract_emails_multiple(crawler, urls, listeners, visited=()):
    crawler.add_skip_patterns([r'\.pdf\W*'])
    crawler.set_page_load_timeout(-1)
    visited_urls = [v for v in visited]
    for url in urls:
        _, visited_urls = crawler.crawl(url, listeners, visited_urls)


def springer_journal(journal_id, volumes, issues, pages=range(1, 2)):
    urls = []
    for vol in volumes:
        for issue in issues:
            for page in pages:
                urls.append("https://link.springer.com/journal/{0}/volumes-and-issues/{1}-{2}?page={3}".
                            format(journal_id, vol, issue, page))
    return urls


def sd_journal(crawler, journal_name, journal_id, volumes, issues=None, parts=None):
    crawler.add_pattern(r'/science/article/.*pii/{0}'.format(journal_id), terminal=True)
    urls = []
    for vol in volumes:
        if issues:
            for issue in issues:
                urls.append("https://www.sciencedirect.com/journal/{0}/vol/{1}/issue/{2}".
                            format(journal_name, vol, issue))
        elif parts:
            for part in parts:
                urls.append("https://www.sciencedirect.com/journal/{0}/vol/{1}/part/{2}".
                            format(journal_name, vol, part))
        else:
            urls.append("https://www.sciencedirect.com/journal/{0}/vol/{1}/suppl/C".
                        format(journal_name, vol))
    return urls


def load_options(filename):
    if not os.path.exists(filename):
        return {}
    with open(filename, "r") as f:
        return json.load(f)


def crawl_springer(listeners, options, visited=()):
    urls = []
    # Communications in Computer and Information Science
    for page in range(1, 33):
        urls.append("https://link.springer.com/search/page/{0}?facet-content-type=%22Book%22&date-facet-mode=between&facet-series=%227899%22&facet-language=%22En%22&facet-end-year=2020&facet-discipline=%22Computer+Science%22&facet-start-year=2017".format(page))

    # LNCS
    for page in range(1, 14):
        urls.append("https://link.springer.com/search/page/{0}?facet-language=%22En%22&facet-content-type=%22ConferenceProceedings%22&facet-sub-discipline=%22Information+Systems+Applications+%28incl.+Internet%29%22&facet-sub-discipline=%22Computer+Communication+Networks%22&facet-series=%22558%22&facet-discipline=%22Computer+Science%22&sortOrder=newestFirst&facet-content-type=%22Book%22&date-facet-mode=between&facet-start-year=2017&facet-end-year=2020".format(page))

    # The Journal of Supercomputing
    urls += springer_journal(11227, range(73, 77), range(1, 13))

    # International Journal of Parallel Programming
    urls += springer_journal(10766, range(45, 49), range(1, 7))

    # Distributed Computing
    urls += springer_journal(446, range(30, 34), range(1, 7))

    # Cluster Computing
    urls += springer_journal(10586, range(20, 24), range(1, 5), range(1, 5))

    # Computing
    urls += springer_journal(607, range(99, 103), range(1, 13))

    # Journal of Grid Computing
    urls += springer_journal(10723, range(15, 19), range(1, 5))

    # Journal of Big Data
    urls += springer_journal(40537, range(4, 9), range(1, 2))

    # Distributed and Parallel Databases
    urls += springer_journal(10619, range(35, 39), range(1, 5))

    # Knowledge and Information Systems
    urls += springer_journal(10115, range(44, 60), range(1, 4))

    # Journal of Cloud Computing
    urls += springer_journal(13677, range(6, 10), range(1, 2))

    # Journal of Ambient Intelligence and Humanized Computing
    urls += springer_journal(12652, range(8, 12), range(1, 7))

    # New Generation Computing
    urls += springer_journal(354, range(35, 39), range(1, 5))

    # Journal of Applied Mathematics and Computing
    urls += springer_journal(12190, range(49, 61), range(1, 2))

    # Applicable Algebra in Engineering, Communication and Computing
    urls += springer_journal(200, range(28, 32), range(1, 7))

    # Computing and Visualization in Science
    urls += springer_journal(791, range(19, 22), range(1, 7))

    # Theory of Computing Systems
    # urls += springer_journal(224, range(56, 62), range(1, 5))
    urls += springer_journal(224, range(62, 65), range(1, 9))

    # Formal Aspects of Computing
    urls += springer_journal(165, range(29, 33), range(1, 7))

    # Soft Computing
    urls += springer_journal(500, range(21, 25), range(1, 25))

    extract_emails_multiple(SpringerCrawler(options), urls, listeners, visited)


def crawl_sd(listeners, options, visited=()):
    crawler = ScienceDirectCrawler(options)
    crawler.clear_patterns()

    urls = []

    # Parallel Computing
    urls += sd_journal(crawler, "parallel-computing", "S01678191", range(81, 102))

    # Journal of Parallel and Distributed Computing
    urls += sd_journal(crawler, "journal-of-parallel-and-distributed-computing", "S07437315", range(123, 151))

    # Big Data Research
    # urls += sd_journal(crawler, "big-data-research", "S22145796", range(1, 2))
    # urls += sd_journal(crawler, "big-data-research", "S22145796", range(2, 3), issues=range(1, 5))
    urls += sd_journal(crawler, "big-data-research", "S22145796", range(14, 24))

    # Future Generation Computer Systems
    # urls += sd_journal(crawler, "future-generation-computer-systems", "S0167739X", range(42, 78))
    # urls += sd_journal(crawler, "future-generation-computer-systems", "S0167739X", range(78, 80), parts=['P1', 'P2', 'P3'])
    urls += sd_journal(crawler, "future-generation-computer-systems", "S0167739X", range(90, 119))

    # Theoretical Computer Science
    # urls += sd_journal(crawler, "theoretical-computer-science", "S03043975", range(561, 562), parts=['PA', 'PB'])
    # urls += sd_journal(crawler, "theoretical-computer-science", "S03043975", range(562, 607))
    # urls += sd_journal(crawler, "theoretical-computer-science", "S03043975", range(607, 610), parts=['P1', 'P2', 'P3'])
    # urls += sd_journal(crawler, "theoretical-computer-science", "S03043975", range(610, 611), parts=['PA', 'PB'])
    # urls += sd_journal(crawler, "theoretical-computer-science", "S03043975", range(611, 654))
    # urls += sd_journal(crawler, "theoretical-computer-science", "S03043975", range(654, 659), parts=['PA', 'PB'])
    urls += sd_journal(crawler, "theoretical-computer-science", "S03043975", range(753, 856))

    # Electronic Notes in Theoretical Computer Science
    urls += sd_journal(crawler, "electronic-notes-in-theoretical-computer-science", "S15710661", range(341, 355))

    # Data & Knowledge Engineering
    # urls += sd_journal(crawler, "data-and-knowledge-engineering", "S0169023X", range(95, 100))
    # urls += sd_journal(crawler, "data-and-knowledge-engineering", "S0169023X", range(100, 101), parts=['PA', 'PB'])
    urls += sd_journal(crawler, "data-and-knowledge-engineering", "S0169023X", range(119, 131))

    extract_emails_multiple(crawler, urls, listeners, visited)


def main():
    listeners = [Logger(), FileWriter("output.txt"), URLLogger("urls.txt")]

    options = load_options("config.txt")
    delay = options.get("delay")
    if delay:
        options["wait"] = lambda: random.randint(0, delay)

    visited_urls = read_lines("urls.txt")

    #url = input("Input url: ")
    #extract_emails(get_crawler(url, options), url, listeners, visited_urls)

    # crawl_springer(listeners, options, visited_urls)
    crawl_sd(listeners, options, visited_urls)

    #merge_results(["output.txt", "emails.txt"], "emails.txt")

    print('Done')


if __name__ == '__main__':
    main()
