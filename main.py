from modules import SearchModule
from selenium.webdriver import Chrome

browser = Chrome()
search_term = "naval seizure tactics"
search_module = SearchModule(browser=browser, prefix="https://www.google.com/search?q=",
                             block_css="div[class=g]", link_css=".rc .r a",
                             next_page_css="td.navend a#pnnext", limit=120,
                             file_name="be.txt")
search_module.search(search_term)
