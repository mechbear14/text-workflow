from modules import SearchModule, TextModule
from selenium.webdriver import Chrome

# browser = Chrome()
# search_term = "music artificial intelligence tutorial"
# search_module = SearchModule(browser=browser, prefix="https://www.google.com/search?q=",
#                              block_css="div[class=g]", link_css=".rc .r a",
#                              next_page_css="td.navend a#pnnext", limit=120,
#                              file_name="links.txt")
# search_module.search(search_term)

file = open("links.txt")

browser = Chrome()
for line in file:
    text_module = TextModule(browser=browser, url=line)
    text_module.parse_text()

browser.close()
