from selenium.common.exceptions import InvalidArgumentException, NoSuchElementException
from urllib.parse import quote
import json
from datetime import datetime


class SearchModule:
    def __init__(self, browser, prefix, block_css, title_css, link_css, next_page_css, limit=50, file_name="links.json"):
        self.prefix = prefix
        self.browser = browser
        self.block_css = block_css
        self.title_css = title_css
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
                        title = r.find_element_by_css_selector(self.title_css).text
                        url = r.find_element_by_css_selector(self.link_css).get_attribute("href")
                        self.results.append(SearchResult(title, url))
                    except NoSuchElementException as e:
                        if len(self.results) > 0:
                            continue
                        else:
                            with open("log.txt", "a+") as log:
                                log.write(datetime.isoformat(datetime.now()))
                                for res in self.results:
                                    res.export(log)
                                log.write(e.msg)
                                log.close()
                            print(e.stacktrace)
                            raise SystemExit
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                browser.find_element_by_css_selector(self.next_page_css).click()
            result_f = open(self.file_name, "w+")
            result_f.write("[")
            for (index, result) in enumerate(self.results):
                if index < self.limit - 1:
                    result.export(result_f)
                    result_f.write(", ")
                else:
                    break
            self.results[self.limit - 1].export(result_f)
            result_f.write("]")
            result_f.close()
            self.browser.close()
        except InvalidArgumentException as e:
            with open("log.txt", "a+") as log:
                log.write(datetime.isoformat(datetime.now()))
                log.write(e.msg)
                log.close()
            print(e.stacktrace)
            raise SystemExit


class SearchResult:
    def __init__(self, title, link):
        self.title = title
        self.link = link

    def export(self, file):
        result_object = dict(title=self.title, link=self.link)
        file.write(json.dumps(result_object))
