from modules import SearchModule
from selenium.webdriver import Chrome

browser = Chrome()
search_term = "music artificial intelligence tutorial"
search_module = SearchModule(browser=browser, prefix="https://www.google.com/search?q=",
                             block_css="div[class=g]", link_css=".rc .r a",
                             title_css=".rc .r a h3", next_page_css="td.navend a#pnnext", limit=120,
                             file_name="music artificial intelligence tutorial.json")
search_module.search(search_term)
