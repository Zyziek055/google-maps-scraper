import time

from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver.support.expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import json
import re


chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = "/usr/bin/google-chrome"

service = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=service, options=chrome_options)

keyword  = "kiev restaurant"
driver.get(f"https://www.google.com/maps/search/{keyword}")

try:
    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "form:nth-child(2)"))).click()
except:
    pass

scrollable_div = driver.find_element(By.CSS_SELECTOR, "div[role='feed']")
driver.execute_script("""
          var scrollableDiv = arguments[0];
          function scrollWithinElement(scrollableDiv) {
              return new Promise((resolve, reject) => {
                  var totalHeight = 0;
                  var distance = 1000;
                  var scrollDelay = 3000;

                  var timer = setInterval(() => {
                      var scrollHeightBefore = scrollableDiv.scrollHeight;
                      scrollableDiv.scrollBy(0, distance);
                      totalHeight += distance;

                      if (totalHeight >= scrollHeightBefore) {
                          totalHeight = 0;
                          setTimeout(() => {
                              var scrollHeightAfter = scrollableDiv.scrollHeight;
                              if (scrollHeightAfter > scrollHeightBefore) {
                                  return;
                              } else {
                                  clearInterval(timer);
                                  resolve();
                              }
                          }, scrollDelay);
                      }
                  }, 200);
              });
          }
          return scrollWithinElement(scrollableDiv);
  """, scrollable_div)

items = driver.find_elements(By.CSS_SELECTOR, "div[role='feed'] > div > div[jsaction] > a")
print(items)
google_maps_links = []
for item in items:
    links = {}
    try:
        links['link'] = item.get_attribute('href')
    except:
        pass

    if (links.get('link')):
        google_maps_links.append(links)

data = []
i = 0

for link in google_maps_links:
    i += 1
    driver.get(link['link'])

    authority_elem = driver.find_elements(By.CSS_SELECTOR, "a[data-item-id='authority']")
    if authority_elem:
        href = authority_elem[0].get_attribute("href")
        website = href
    else:
        website = ""


    entry_data = {
        "name": driver.title.strip("– Mapy Google"),
        "google_maps_link": link['link'],
        "website": website
    }
    data.append(entry_data)

    if( i > 5):
        break

with open('results.json', 'w') as f:
    json.dump(data, f, indent=2)

driver.quit()

