from selenium import webdriver
import urllib.parse as urlparse

driver = webdriver.PhantomJS()
driver.get("https://www.google.com/search?q=test")

results = driver.find_elements_by_css_selector('div.g')
print(len(results))
link = results[0].find_element_by_tag_name("a")
href = link.get_attribute("href")

print(urlparse.parse_qs(urlparse.urlparse(href).query)["q"])
