import string
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


def scrape(city: string):
    driver = webdriver.Chrome()
    driver.get(f"https://www.google.com/maps/search/{city}+restaurant/@50.4892342,30.3836585,11.02z/data=!4m2!2m1!6e5?entry=ttu&g_ep=EgoyMDI1MDkxNS4wIKXMDSoASAFQAw%3D%3D")
    accept_cookies = driver.find_element(By.CLASS_NAME, "lssxud")
    accept_cookies.click()

    container = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]')))
    search_results = container.find_elements(by=By.CSS_SELECTOR, value="*")

    for i in range(3, len(search_results), 2):
        if search_results[i].get_attribute("class") != "TFQHme ":
            print(search_results[i].text)

        driver.execute_script("window.scrollTo(0, 100)")


    time.sleep(5000)

