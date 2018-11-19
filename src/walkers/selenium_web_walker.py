from selenium import webdriver
from selenium.common.exceptions import TimeoutException
import time


class SeleniumWebWalker(object):
    def __init__(self, page_load_timeout=5):
        super().__init__()
        self.driver = self._init_driver()
        self.driver.set_page_load_timeout(page_load_timeout)
        self.page_load_timeout = page_load_timeout

    def _init_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--test-type")
        #options.add_argument('--headless')
        options.add_argument("--disable-infobars")
        return webdriver.Chrome(chrome_options=options)

    def open(self, url):
        try:
            self.driver.get(url)
            #self.driver.implicitly_wait(self.page_load_timeout)
            time.sleep(5)
        except TimeoutException:
            raise Exception("Page load timeout: " + url)

    def get_current_page_url(self):
        return self.driver.current_url

    def get_current_page_source(self):
        return self.driver.page_source

    def get_urls(self):
        links = self.driver.find_elements_by_tag_name("a")
        urls = [link.get_attribute("href") for link in links]
        return [url for url in urls if url]

