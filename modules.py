from selenium.common.exceptions import InvalidArgumentException, NoSuchElementException, StaleElementReferenceException
from urllib.parse import quote
from datetime import datetime
from readability import Document
from bs4 import BeautifulSoup
import json


# TODO: Instead of writing to files, can you return the results directly for the next block to use?
class SearchModule:
    def __init__(self, browser, prefix, block_css, link_css, next_page_css, limit=50, file_name="links.txt"):
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
                                log.write(datetime.now().strftime("%Y%m%d%H%M%S"))
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
                    result_f.write(result.encode("utf8").decode("ascii", "ignore"))
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
    def __init__(self, browser, url=None, index=0):
        self.browser = browser
        self.url = url
        self.index = index

    def parse_text(self):
        self.browser.get(self.url)
        source = self.browser.execute_script("return Array.from(document.getElementsByTagName('html'))[0].innerHTML")
        doc = Document(source)
        title = doc.title().encode("utf-8").decode("ascii", "ignore")
        body = doc.summary()
        soup = BeautifulSoup(body, "html.parser")
        text = soup.get_text().encode("utf-8").decode("ascii", "ignore")
        # time_str = datetime.now().strftime("%Y%m%d%H%M%S")
        # title_str = quote(title, safe="")
        # with open("{}-{}.txt".format(time_str, title_str), "w+") as file:
        #     file.write(title.encode("utf8").decode("ascii", "ignore"))
        #     file.write("\n")
        #     file.write(text.encode("utf8").decode("ascii", "ignore"))
        document = dict(title=title, url=self.url, reliability=0, title_obj=0, text_obj=0, text=text)
        with open("{}.json".format(self.index + 120), "w+") as file:
            json.dump(obj=document, fp=file)


class NELAModule:
    def __init__(self, browser, title, text):
        self.browser = browser
        self.title = title
        self.text = text

    def assess(self):
        show_btn = self.browser.find_elements_by_css_selector("input#manual_entry_button")[0]
        textareas = self.browser.find_elements_by_css_selector("#manual_entry textarea")
        title_box = textareas[0]
        text_box = textareas[1]
        submit_btn = self.browser.find_elements_by_css_selector("#manual_entry input[type='submit']")[0]

        show_btn.click()
        title_box.send_keys(self.title)
        text_box.send_keys(self.text)
        submit_btn.click()
