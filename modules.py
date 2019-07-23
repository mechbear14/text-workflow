from selenium.common.exceptions import InvalidArgumentException, NoSuchElementException,StaleElementReferenceException
from urllib.parse import quote
from datetime import datetime
from readability import Document
from bs4 import BeautifulSoup


# TODO: Instead of writing to files, can you return the results directly for the next block to use?
class SearchModule:
    def __init__(self, browser, prefix, block_css, link_css, next_page_css, limit=50, file_name="links.json"):
        self.prefix = prefix
        self.browser = browser
        self.block_css = block_css
        self.link_css = link_css
        self.next_page_css = next_page_css
        self.limit = limit
        self.file_name = file_name
        self.results = []

    def search(self, query):
        browser = self.browser
        addr = "{}{}".format(self.prefix, quote(query, safe=""))

        try:
            browser.get(addr)
            while len(self.results) < self.limit:
                rs = browser.find_elements_by_css_selector(self.block_css)
                for r in rs:
                    try:
                        url = r.find_element_by_css_selector(self.link_css).get_attribute("href")
                        self.results.append(url)
                    except NoSuchElementException as e:
                        if len(self.results) > 0:
                            continue
                        else:
                            with open("log.txt", "a+") as log:
                                log.write(datetime.now().strftime("%Y-%m-%d-%h-%m-%s"))
                                for res in self.results:
                                    res.export(log)
                                log.write(e.msg)
                                log.close()
                            print(e.stacktrace)
                            raise SystemExit
                    except StaleElementReferenceException as e:
                        if len(self.results) > 0:
                            continue
                try:
                    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                    browser.find_element_by_css_selector(self.next_page_css).click()
                except NoSuchElementException as e:
                    print(e)
                    break
            result_f = open(self.file_name, "w+")
            for (index, result) in enumerate(self.results):
                if index < self.limit:
                    result_f.write(result)
                    result_f.write("\n")
                else:
                    break
            result_f.close()
            self.browser.close()
        except InvalidArgumentException as e:
            with open("log.txt", "a+") as log:
                log.write(datetime.isoformat(datetime.now()))
                log.write(e.msg)
                log.close()
            print(e.stacktrace)
            raise SystemExit


class TextModule:
    def __init__(self, browser, url=None):
        self.browser = browser
        self.url = url

    def parse_text(self):
        self.browser.get(self.url)
        source = self.browser.execute_script("return Array.from(document.getElementsByTagName('html'))[0].innerHTML")
        doc = Document(source)
        title = doc.title()
        body = doc.summary()
        soup = BeautifulSoup(body, "html.parser")
