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

city = "kiev"
driver.get(f"https://www.google.com/maps/search/{city}+restaurant")

time.sleep(10)

