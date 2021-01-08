#!/usr/bin/env python

from crawlers.email_crawler import EmailCrawler
from crawlers.science_direct_crawler import ScienceDirectCrawler
from crawlers.springer_crawler import SpringerCrawler
from listeners.logger import Logger
from listeners.file_writer import FileWriter

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


def extract_emails(crawler, url, listeners):
    crawler.add_skip_patterns([r'\.pdf\W*'])
    crawler.set_page_load_timeout(-1)
    crawler.crawl(url, listeners)


def extract_emails_multiple(crawler, urls, listeners):
    crawler.add_skip_patterns([r'\.pdf\W*'])
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
        for line in sorted(lines):
            f.write(line + "\n")


def springer_journal(journal_id, volumes, issues, pages=range(1, 2)):
    urls = []
    for vol in volumes:
        for issue in issues:
            for page in pages:
                urls.append("https://link.springer.com/journal/{0}/{1}/{2}/page/{3}".
                            format(journal_id, vol, issue, page))
    return urls


def sd_journal(crawler, journal_name, journal_id, volumes, issues=None, parts=None):
    crawler.add_pattern('/science/article/pii/{0}'.format(journal_id), terminal=True)
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


def crawl_springer(listeners, options):
    urls = []
    # Communications in Computer and Information Science
    for page in range(1, 8):
        urls.append("https://link.springer.com/search/page/{0}?facet-content-type=%22Book%22&date-facet-mode=between&previous-end-year=2019&previous-start-year=2015&facet-series=%227899%22&facet-end-year=2018&facet-sub-discipline=%22Information+Systems+Applications+%28incl.+Internet%29%22&facet-discipline=%22Computer+Science%22&facet-start-year=2015".format(page))

    # LNCS
    for page in range(1, 18):
        urls.append("https://link.springer.com/search/page/{0}?facet-sub-discipline=%22Computer+Communication+Networks%22&facet-content-type=%22Book%22&date-facet-mode=between&facet-content-type=%22ConferenceProceedings%22&facet-series=%22558%22&facet-language=%22En%22&sortOrder=newestFirst&facet-end-year=2018&facet-sub-discipline=%22Information+Systems+Applications+%28incl.+Internet%29%22&facet-discipline=%22Computer+Science%22&facet-start-year=2015".format(page))

    # The Journal of Supercomputing
    urls += springer_journal(11227, range(71, 75), range(1, 13))

    # International Journal of Parallel Programming
    urls += springer_journal(10766, range(43, 47), range(1, 7))

    # Distributed Computing
    urls += springer_journal(446, range(28, 32), range(1, 7))

    # Cluster Computing
    urls += springer_journal(10586, range(18, 22), range(1, 5), range(1, 5))

    # Computing
    urls += springer_journal(607, range(97, 101), range(1, 13))

    # Journal of Grid Computing
    urls += springer_journal(10723, range(13, 17), range(1, 5))

    # Journal of Big Data
    urls += springer_journal(40537, range(1, 6), range(1, 2))

    # Distributed and Parallel Databases
    urls += springer_journal(10619, range(33, 37), range(1, 5))

    # Knowledge and Information Systems
    urls += springer_journal(10115, range(42, 58), range(1, 4))

    # Journal of Cloud Computing
    urls += springer_journal(13677, range(1, 8), range(1, 2))

    # Journal of Ambient Intelligence and Humanized Computing
    urls += springer_journal(12652, range(6, 10), range(1, 7))

    # New Generation Computing
    urls += springer_journal(354, range(33, 37), range(1, 5))

    # Journal of Applied Mathematics and Computing
    urls += springer_journal(12190, range(47, 59), range(1, 2))

    # Applicable Algebra in Engineering, Communication and Computing
    urls += springer_journal(200, range(26, 30), range(1, 7))

    # Computing and Visualization in Science
    urls += springer_journal(791, range(17, 20), range(1, 7))

    # Theory of Computing Systems
    urls += springer_journal(224, range(56, 62), range(1, 5))
    urls += springer_journal(224, range(62, 63), range(1, 9))

    # Formal Aspects of Computing
    urls += springer_journal(165, range(27, 31), range(1, 7))

    # Soft Computing
    urls += springer_journal(500, range(19, 23), range(1, 25))

    extract_emails_multiple(SpringerCrawler(options), urls, listeners)


def crawl_sd(listeners, options):
    crawler = ScienceDirectCrawler(options)
    crawler.clear_patterns()

    urls = []

    # Parallel Computing
    urls += sd_journal(crawler, "parallel-computing", "S01678191", range(41, 82))

    # Journal of Parallel and Distributed Computing
    urls += sd_journal(crawler, "journal-of-parallel-and-distributed-computing", "S07437315", range(70, 126))

    # Big Data Research
    urls += sd_journal(crawler, "big-data-research", "S22145796", range(1, 2))
    urls += sd_journal(crawler, "big-data-research", "S22145796", range(2, 3), issues=range(1, 5))
    urls += sd_journal(crawler, "big-data-research", "S22145796", range(3, 14))

    # Future Generation Computer Systems
    urls += sd_journal(crawler, "future-generation-computer-systems", "S0167739X", range(42, 78))
    urls += sd_journal(crawler, "future-generation-computer-systems", "S0167739X", range(78, 80), parts=['P1', 'P2', 'P3'])
    urls += sd_journal(crawler, "future-generation-computer-systems", "S0167739X", range(80, 95))

    # Theoretical Computer Science
    urls += sd_journal(crawler, "theoretical-computer-science", "S03043975", range(561, 562), parts=['PA', 'PB'])
    urls += sd_journal(crawler, "theoretical-computer-science", "S03043975", range(562, 607))
    urls += sd_journal(crawler, "theoretical-computer-science", "S03043975", range(607, 610), parts=['P1', 'P2', 'P3'])
    urls += sd_journal(crawler, "theoretical-computer-science", "S03043975", range(610, 611), parts=['PA', 'PB'])
    urls += sd_journal(crawler, "theoretical-computer-science", "S03043975", range(611, 654))
    urls += sd_journal(crawler, "theoretical-computer-science", "S03043975", range(654, 659), parts=['PA', 'PB'])
    urls += sd_journal(crawler, "theoretical-computer-science", "S03043975", range(659, 754))

    # Electronic Notes in Theoretical Computer Science
    urls += sd_journal(crawler, "electronic-notes-in-theoretical-computer-science", "S15710661", range(310, 341))

    # Data & Knowledge Engineering
    urls += sd_journal(crawler, "data-and-knowledge-engineering", "S0169023X", range(95, 100))
    urls += sd_journal(crawler, "data-and-knowledge-engineering", "S0169023X", range(100, 101), parts=['PA', 'PB'])
    urls += sd_journal(crawler, "data-and-knowledge-engineering", "S0169023X", range(101, 119))

    extract_emails_multiple(crawler, urls, listeners)


def main():
    listeners = [Logger(), FileWriter("output.txt")]

    options = load_options("config.txt")
    options["wait"] = lambda: random.randint(0, options.get("delay")) if "delay" in options else None

    url = input("Input url: ")
    extract_emails(get_crawler(url, options), url, listeners)

    # crawl_springer(listeners, options)
    # crawl_sd(listeners, options)

    merge_results(["output.txt", "emails.txt"], "emails.txt")

    print('Done')


if __name__ == '__main__':
    main()
