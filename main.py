from modules import SearchModule, TextModule
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.webdriver import Chrome
from os import listdir
from os.path import isfile, join
import re

# TODO: Check Internet connection
browser = Chrome()
search_term = "music artificial intelligence tutorial"
search_module = SearchModule(browser=browser, prefix="https://www.google.com/search?q=",
                             block_css="div[class=g]", link_css=".rc .r a",
                             next_page_css="td.navend a#pnnext", limit=120,
                             file_name="links.txt")
search_module.search(search_term)

file = open("links.txt")

browser = Chrome()
for index, line in enumerate(file):
    text_module = TextModule(browser=browser, url=line, index=index)
    text_module.parse_text()

browser.close()


# browser = Chrome()
# browser.get("http://nelatoolkit.science/credibilitytoolkit")
# clear_btn = browser.find_elements_by_css_selector(".panel-body input[type='button']")[1]
# clear_btn.click()
# browser.switch_to.alert.accept()
# files = [f for f in listdir("./") if isfile(join("./", f)) and re.search(r"20\d{12}-.+\.txt", f)]
# for file in files:
#     with open(file) as f:
#         title = f.readline()
#         text = ""
#         line = f.readline()
#         while line:
#             text += line
#             text += "\n"
#             line = f.readline()
#         nela = NELAModule(browser, title, text)
#         try:
#             nela.assess()
#         except UnexpectedAlertPresentException:
#             # browser.switch_to.alert.accept()
#             with open("nela_problems.txt", "a+") as erf:
#                 erf.write(f.name)
#                 erf.write("\n")
#             continue
#         except IndexError:
#             browser.back()
#             with open("nela_problems.txt", "a+") as erf:
#                 erf.write(f.name)
#                 erf.write("\n")
#             continue
