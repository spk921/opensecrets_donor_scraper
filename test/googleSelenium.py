from selenium import webdriver
import urllib.parse as urlparse

driver = webdriver.PhantomJS()
query = 'test'
driver.get("https://www.google.com/search?q="+query)
#div.g means <div class='g'> <div>
results = driver.find_elements_by_css_selector('div.g')
print(len(results))
link = results[0].find_element_by_tag_name("a")
href = link.get_attribute("href")
print(href)
print(type(href))
print(urlparse.parse_qs(urlparse.urlparse(href).query)["q"])
