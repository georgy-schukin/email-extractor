from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time


class SeleniumWebWalker(object):
    def __init__(self):
        super().__init__()
        self.driver = self._init_driver()

    def _init_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument("--test-type")
        #options.add_argument('--headless')
        options.add_argument("--disable-infobars")
        #options.add_argument("--incognito")
        options.add_argument("--no-sandbox")

        caps = DesiredCapabilities.CHROME
        caps["pageLoadStrategy"] = "normal"

        prefs = {"profile.managed_default_content_settings.images": 2, 'disk-cache-size': 4096}
        options.add_experimental_option("prefs", prefs)

        adblock_path = "/home/georgy/.config/google-chrome/Default/Extensions/cfhdojbkjhnklbpkdaibdccddilifddb/3.4.1_1/"
        options.add_argument("load-extension=" + adblock_path)

        return webdriver.Chrome(chrome_options=options, desired_capabilities=caps)

    def set_page_load_timeout(self, page_load_timeout):
        self.driver.set_page_load_timeout(page_load_timeout)
        self.page_load_timeout = page_load_timeout

    def close(self):
        if self.driver:
            self.driver.close()

    def open(self, url):
        try:
            self.driver.get(url)
            #element_present = expected_conditions.presence_of_element_located((By.TAG_NAME, 'body'))
            #WebDriverWait(self.driver, timeout=5).until(element_present)
            #self.driver.implicitly_wait(self.page_load_timeout)
            #time.sleep(2)
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

