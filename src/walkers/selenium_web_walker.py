from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
import random


class SeleniumWebWalker(object):
    def __init__(self, options):
        super().__init__()
        self.driver = self._init_driver(options)
        self.wait = options.get("wait")

    def _init_driver(self, options):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument("--test-type")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--no-sandbox")
        # chrome_options.add_argument("--incognito")

        caps = DesiredCapabilities.CHROME
        caps["pageLoadStrategy"] = "normal"

        prefs = {'disk-cache-size': 4096}

        if options.get("no-images"):
            prefs["profile.managed_default_content_settings.images"] = 2

        for ext_path in options.get("extensions", []):
            chrome_options.add_argument("load-extension=" + ext_path)

        if options.get("proxy"):
            proxy_addr = options.get("proxy")
            proxy = {"proxyType": "MANUAL",
                     "httpProxy": proxy_addr,
                     "ftpProxy": proxy_addr,
                     "sslProxy": proxy_addr
                     }
            caps["proxy"] = proxy

        if options.get("headless"):
            chrome_options.add_argument('--headless')

        chrome_options.add_experimental_option("prefs", prefs)

        return webdriver.Chrome(chrome_options=chrome_options, desired_capabilities=caps)

    def set_page_load_timeout(self, page_load_timeout):
        self.driver.set_page_load_timeout(page_load_timeout)
        self.page_load_timeout = page_load_timeout

    def close(self):
        if self.driver:
            self.driver.close()

    def open(self, url):
        try:
            self.driver.get(url)
            if self.wait:
                time.sleep(self.wait())
            #element_present = expected_conditions.presence_of_element_located((By.TAG_NAME, 'body'))
            #WebDriverWait(self.driver, timeout=5).until(element_present)
            #self.driver.implicitly_wait(self.page_load_timeout)
            #time.sleep(random.randint(0, 2))
        except TimeoutException:
            pass
            #raise Exception("Page load timeout: " + url)

    def get_current_page_url(self):
        return self.driver.current_url

    def get_current_page_source(self):
        return self.driver.page_source

    def get_urls(self):
        links = self.driver.find_elements_by_tag_name("a")
        urls = []
        for link in links:
            try:
                urls.append(link.get_attribute("href"))
            except Exception:
                pass
        return [url for url in urls if url]

